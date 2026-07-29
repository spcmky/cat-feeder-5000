#!/usr/bin/env python3
"""Sort data_v2/unlabeled into cat_a / cat_b / not_cat using labels.json."""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_v2")
SRC = os.path.join(DATA, "unlabeled")

CLASSES = ["cat_a", "cat_b", "not_cat"]

labels = json.load(open(os.path.join(HERE, "labels.json")))

# Rebuild the class dirs from scratch. This script is re-run after every
# correction pass, and copying without clearing would leave a crop sitting
# in the folder it was moved out of - the old label would silently survive.
for kind in CLASSES:
    dst_dir = os.path.join(DATA, kind)
    if os.path.isdir(dst_dir):
        shutil.rmtree(dst_dir)
    os.makedirs(dst_dir)

counts = {}
for eid, kind in labels.items():
    if kind not in CLASSES:
        print(f"skipping {eid}: unknown label {kind!r}")
        continue
    src = os.path.join(SRC, eid + ".jpg")
    if not os.path.exists(src):
        continue
    shutil.copy2(src, os.path.join(DATA, kind, eid + ".jpg"))
    counts[kind] = counts.get(kind, 0) + 1

for kind in CLASSES:
    print(f"{kind:8s} {counts.get(kind, 0)}")
print(f"unlabelled left: {len(os.listdir(SRC)) - sum(counts.values())}")
