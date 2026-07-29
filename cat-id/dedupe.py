#!/usr/bin/env python3
"""Collapse near-duplicate crops down to one representative each.

Frigate re-acquires a stationary cat every second or so, so a single long
sit produces dozens of near-identical frames - one 82-minute visit alone
contributed 55, a fifth of the cat_a class. They cost training capacity
and skew the class balance without adding information.

Groups crops by perceptual hash (dHash, Hamming <= THRESH), keeps the
sharpest frame in each group, and moves the rest to data_v2/_dupes/<class>/.
Nothing is deleted, and _dupes/ sits outside the three class dirs that
train_v2.py reads, so the move is enough to take them out of training.

    python3 dedupe.py            # report only
    python3 dedupe.py --apply    # actually move
"""
import os
import shutil
import sys
from collections import defaultdict

from PIL import Image, ImageFilter, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_v2")
CLASSES = ["cat_a", "cat_b", "not_cat"]
DUPES = os.path.join(DATA, "_dupes")
THRESH = 5


def dhash(path, size=8):
    px = list(Image.open(path).convert("L").resize((size + 1, size)).getdata())
    bits = 0
    for r in range(size):
        for c in range(size):
            bits = (bits << 1) | (1 if px[r * (size + 1) + c]
                                  > px[r * (size + 1) + c + 1] else 0)
    return bits


def sharpness(path):
    """Edge energy - picks the least motion-blurred frame of a group."""
    im = Image.open(path).convert("L").resize((160, 160))
    return ImageStat.Stat(im.filter(ImageFilter.FIND_EDGES)).var[0]


def hamming(a, b):
    return bin(a ^ b).count("1")


def main():
    apply = "--apply" in sys.argv
    total_kept = total_moved = 0

    for kind in CLASSES:
        d = os.path.join(DATA, kind)
        files = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
        if not files:
            continue
        hashes = {f: dhash(os.path.join(d, f)) for f in files}

        parent = {f: f for f in files}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, a in enumerate(files):
            for b in files[i + 1:]:
                if hamming(hashes[a], hashes[b]) <= THRESH:
                    ra, rb = find(a), find(b)
                    if ra != rb:
                        parent[ra] = rb

        groups = defaultdict(list)
        for f in files:
            groups[find(f)].append(f)

        moved = []
        for members in groups.values():
            if len(members) == 1:
                continue
            best = max(members, key=lambda f: sharpness(os.path.join(d, f)))
            moved += [f for f in members if f != best]

        kept = len(files) - len(moved)
        total_kept += kept
        total_moved += len(moved)
        biggest = max((len(m) for m in groups.values()), default=0)
        print(f"{kind:8s} {len(files):4d} -> {kept:4d} keep, "
              f"{len(moved):4d} dup   (largest group {biggest})")

        if apply and moved:
            out = os.path.join(DUPES, kind)
            os.makedirs(out, exist_ok=True)
            for f in moved:
                shutil.move(os.path.join(d, f), os.path.join(out, f))

    print(f"\ntotal {total_kept + total_moved} -> {total_kept} kept, "
          f"{total_moved} moved to data_v2/_dupes/")
    if not apply:
        print("dry run - re-run with --apply to move them")
    else:
        print("now run: python3 sync_labels.py")


if __name__ == "__main__":
    main()
