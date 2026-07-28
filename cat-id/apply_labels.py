#!/usr/bin/env python3
"""Sort data_v2/unlabeled into cat_a / cat_b / not_cat using labels.json."""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_v2")
SRC = os.path.join(DATA, "unlabeled")

labels = json.load(open(os.path.join(HERE, "labels.json")))
counts = {}
for eid, kind in labels.items():
    src = os.path.join(SRC, eid + ".jpg")
    if not os.path.exists(src):
        continue
    dst_dir = os.path.join(DATA, kind)
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, os.path.join(dst_dir, eid + ".jpg"))
    counts[kind] = counts.get(kind, 0) + 1

for kind in sorted(counts):
    print(f"{kind:8s} {counts[kind]}")
print(f"unlabelled left: {len(os.listdir(SRC)) - sum(counts.values())}")
