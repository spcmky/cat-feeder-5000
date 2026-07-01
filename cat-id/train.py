import torch, torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split

# M3 GPU if available, else CPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print("Training on:", device)

# --- Data ---
# Two transforms: training gets augmentation, testing does not.
train_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.3, contrast=0.3),
    transforms.ToTensor(),
])
test_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Expects a parent folder containing cat_a/ and cat_b/.
# We point ImageFolder at the current directory.
full = datasets.ImageFolder("./data", transform=train_tf)
print("Classes:", full.classes)   # should print ['cat_a', 'cat_b']

# 80/20 split, fixed seed so it's reproducible
n_test = int(0.2 * len(full))
n_train = len(full) - n_test
train_set, test_set = random_split(
    full, [n_train, n_test],
    generator=torch.Generator().manual_seed(42)
)
# test set shouldn't be augmented
test_set.dataset.transform = test_tf

train_loader = DataLoader(train_set, batch_size=16, shuffle=True)
test_loader = DataLoader(test_set, batch_size=16)

# --- Model (transfer learning) ---
# Pretrained ResNet18, replace the final layer with a 2-class head.
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, 2)
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

# --- Train ---
EPOCHS = 15
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
    train_acc = correct / total

    # check on held-back set
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            out = model(imgs)
            correct += (out.argmax(1) == labels).sum().item()
            total += labels.size(0)
    test_acc = correct / total

    print(f"Epoch {epoch+1:2d}  train {train_acc:.0%}  test {test_acc:.0%}")

torch.save(model.state_dict(), "cat_model.pth")
print("Saved cat_model.pth")