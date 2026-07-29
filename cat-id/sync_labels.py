#!/usr/bin/env python3
"""Rebuild labels.json from whatever is currently in the class folders.

The folders are the source of truth once you have moved files around by
hand. apply_labels.py goes the other way (labels.json -> folders) and
rebuilds the folders from scratch, so running it against a stale
labels.json silently discards manual corrections. Run this first to
capture them, then labels.json and the folders agree again.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_v2")
CLASSES = ["cat_a", "cat_b", "not_cat"]
OUT = os.path.join(HERE, "labels.json")

old = json.load(open(OUT)) if os.path.exists(OUT) else {}

labels = {}
for kind in CLASSES:
    d = os.path.join(DATA, kind)
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        if f.endswith(".jpg"):
            labels[os.path.splitext(f)[0]] = kind

moved = {k: (old[k], v) for k, v in labels.items()
         if k in old and old[k] != v}
added = [k for k in labels if k not in old]
dropped = [k for k in old if k not in labels]

with open(OUT, "w") as fh:
    json.dump(labels, fh, indent=2, sort_keys=True)

counts = {c: sum(1 for v in labels.values() if v == c) for c in CLASSES}
print(f"wrote {OUT}: " + "  ".join(f"{c} {counts[c]}" for c in CLASSES))
print(f"reclassified since last export: {len(moved)}")
for k, (a, b) in sorted(moved.items())[:20]:
    print(f"   {k}  {a} -> {b}")
if len(moved) > 20:
    print(f"   ... and {len(moved) - 20} more")
if added:
    print(f"newly labelled: {len(added)}")
if dropped:
    print(f"no longer in any class folder: {len(dropped)}")
