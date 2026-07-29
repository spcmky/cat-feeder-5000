#!/usr/bin/env python3
"""Retrain cat_id on real Frigate crops.

Changes from train.py:
  - 3 classes (cat_a, cat_b, not_cat) so the model can reject the false
    positives Frigate's COCO detector produces on dark objects
  - ImageNet normalisation (train and export must agree - the v1 model
    had none, which is why the export bakes /255 only)
  - class weighting, since the classes will not be balanced
  - grouped split: crops from the same visit never straddle train/val,
    otherwise near-duplicate burst frames inflate the score
"""
import json
import os
from collections import Counter, defaultdict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, models, transforms

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_v2")
CLASSES = ["cat_a", "cat_b", "not_cat"]
VISIT_GAP = 20 * 60
EPOCHS = 25

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print("Training on:", device)

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
train_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(12),
    transforms.ColorJitter(brightness=0.35, contrast=0.35, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])
val_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])

class LabelledFolder(datasets.ImageFolder):
    """ImageFolder over CLASSES only.

    data_v2/ also holds unlabelled/, which plain ImageFolder picks up as a
    class and then dies on because is_valid_file rejects every file in it.
    """

    def find_classes(self, directory):
        missing = [c for c in CLASSES
                   if not os.path.isdir(os.path.join(directory, c))]
        if missing:
            raise SystemExit(f"missing class dirs {missing} in {directory} - "
                             "run apply_labels.py first")
        return CLASSES, {c: i for i, c in enumerate(CLASSES)}


def load(tf):
    return LabelledFolder(DATA, transform=tf,
                          is_valid_file=lambda p: p.endswith(".jpg"))


full = load(train_tf)
print("Classes:", full.classes)

# --- grouped split: keep a whole visit on one side of the split ---
starts = {}
for path, _ in full.samples:
    eid = os.path.splitext(os.path.basename(path))[0]
    starts[path] = float(eid.split("-")[0])

visit_of = {}
vid = 0
prev = None
for path in sorted(starts, key=lambda p: starts[p]):
    if prev is not None and starts[path] - prev > VISIT_GAP:
        vid += 1
    visit_of[path] = vid
    prev = starts[path]

by_visit = defaultdict(list)
for i, (path, _) in enumerate(full.samples):
    by_visit[visit_of[path]].append(i)

visits = sorted(by_visit)
n_val_visits = max(1, int(0.25 * len(visits)))

# cat_b is rare and clustered into few visits, so a plain random split can
# leave zero of them in val (making val accuracy meaningless for Casper) or
# zero in train. Resample seeds until both sides hold every class.
val_visits = None
for seed in range(200):
    gen = torch.Generator().manual_seed(seed)
    order = torch.randperm(len(visits), generator=gen).tolist()
    cand = {visits[i] for i in order[:n_val_visits]}
    v_lab = {full.targets[i] for v in cand for i in by_visit[v]}
    t_lab = {full.targets[i] for v in visits if v not in cand
             for i in by_visit[v]}
    if len(v_lab) == len(CLASSES) and len(t_lab) == len(CLASSES):
        val_visits = cand
        print(f"visit split seed {seed}: all {len(CLASSES)} classes on both sides")
        break
if val_visits is None:
    raise SystemExit(
        "could not find a visit split with every class on both sides - "
        "some class is confined to too few visits; label more of it")

val_idx = [i for v in val_visits for i in by_visit[v]]
train_idx = [i for v in visits if v not in val_visits for i in by_visit[v]]
print(f"{len(visits)} visits -> train {len(train_idx)} crops / "
      f"val {len(val_idx)} crops ({len(val_visits)} held-out visits)")

val_base = load(val_tf)
train_loader = DataLoader(Subset(full, train_idx), batch_size=16, shuffle=True)
val_loader = DataLoader(Subset(val_base, val_idx), batch_size=16)

counts = Counter(full.targets[i] for i in train_idx)
print("train class counts:", {full.classes[k]: v for k, v in sorted(counts.items())})
weights = torch.tensor([len(train_idx) / (len(CLASSES) * counts.get(i, 1))
                        for i in range(len(CLASSES))], dtype=torch.float32).to(device)

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, len(CLASSES))
model = model.to(device)

criterion = nn.CrossEntropyLoss(weight=weights)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

best = 0.0
for epoch in range(EPOCHS):
    model.train()
    correct = total = 0
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        out = model(imgs)
        loss = criterion(out, labels)
        loss.backward()
        optimizer.step()
        correct += (out.argmax(1) == labels).sum().item()
        total += labels.size(0)
    train_acc = correct / max(total, 1)

    model.eval()
    correct = total = 0
    per_class = defaultdict(lambda: [0, 0])
    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            pred = model(imgs).argmax(1)
            for p, l in zip(pred.tolist(), labels.tolist()):
                per_class[l][1] += 1
                per_class[l][0] += int(p == l)
            correct += (pred == labels).sum().item()
            total += labels.size(0)
    val_acc = correct / max(total, 1)
    detail = "  ".join(f"{CLASSES[k]} {v[0]}/{v[1]}" for k, v in sorted(per_class.items()))
    print(f"Epoch {epoch + 1:2d}  train {train_acc:.0%}  val {val_acc:.0%}   {detail}")

    if val_acc >= best:
        best = val_acc
        torch.save(model.state_dict(), os.path.join(HERE, "cat_model_v2.pth"))

json.dump({"classes": CLASSES, "mean": MEAN, "std": STD, "best_val": best},
          open(os.path.join(HERE, "cat_model_v2.json"), "w"), indent=2)
print(f"Saved cat_model_v2.pth (best val {best:.0%})")
