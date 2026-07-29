#!/usr/bin/env python3
"""Build a self-contained HTML labelling page for the data_v2 crops.

Reads data_v2/meta.json plus the crops in data_v2/unlabeled/ and writes
label.html with every image inlined, so the page works offline.

Open label.html in a browser, press 1/2/3 to label each crop, then click
Export to save labels.json next to this script and run apply_labels.py.
"""
import base64
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_v2")
SRC = os.path.join(DATA, "unlabeled")

HTML = """<!doctype html>
<meta charset="utf-8">
<title>cat_id labelling</title>
<style>
  body { font-family: -apple-system, sans-serif; margin: 0; background: #111; color: #eee; }
  /* z-index is load-bearing: the figures below are position:relative, so
     without it they paint over the sticky header once the page scrolls */
  header { position: sticky; top: 0; z-index: 10; background: #1b1b1b; padding: 10px 16px;
           display: flex; gap: 18px; align-items: center; border-bottom: 1px solid #333;
           flex-wrap: wrap; }
  header b { font-size: 15px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
          gap: 8px; padding: 12px; }
  figure { margin: 0; position: relative; border: 3px solid transparent; border-radius: 6px;
           overflow: hidden; cursor: pointer; background: #000; }
  figure img { width: 100%; height: 150px; object-fit: cover; display: block; }
  figcaption { font-size: 11px; padding: 3px 5px; color: #aaa; }
  .cat_a  { border-color: #4da3ff; }
  .cat_b  { border-color: #ffd24d; }
  .not_cat{ border-color: #ff5c5c; opacity: .55; }
  .sel    { outline: 3px solid #fff; outline-offset: -3px; }
  button  { padding: 7px 13px; border-radius: 6px; border: 1px solid #444;
            background: #262626; color: #eee; cursor: pointer; font-size: 13px; }
  .key { background:#333; padding:1px 6px; border-radius:4px; font-family: monospace; }
</style>
<header>
  <b>cat_id labelling</b>
  <span><span class="key">1</span> Tom (cat_a)</span>
  <span><span class="key">2</span> Casper (cat_b)</span>
  <span><span class="key">3</span> not a cat</span>
  <span><span class="key">&larr; &rarr;</span> move</span>
  <span id="count"></span>
  <button onclick="exportLabels()">Export labels.json</button>
</header>
<div class="grid" id="grid"></div>
<script>
const ROWS = __ROWS__;
let cur = 0;
const grid = document.getElementById('grid');
ROWS.forEach((r, i) => {
  const f = document.createElement('figure');
  f.id = 'f' + i;
  if (r.guess) f.className = r.guess;
  f.innerHTML = '<img src="' + r.src + '"><figcaption>' + r.t + '</figcaption>';
  f.onclick = () => { cur = i; render(); };
  grid.appendChild(f);
});
function label(kind) {
  ROWS[cur].guess = kind;
  document.getElementById('f' + cur).className = kind;
  if (cur < ROWS.length - 1) cur++;
  render();
}
function render() {
  ROWS.forEach((r, i) => {
    const el = document.getElementById('f' + i);
    el.className = (r.guess || '') + (i === cur ? ' sel' : '');
  });
  const done = ROWS.filter(r => r.guess).length;
  document.getElementById('count').textContent =
    done + ' / ' + ROWS.length + ' labelled';
  const el = document.getElementById('f' + cur);
  if (el) el.scrollIntoView({ block: 'nearest' });
}
addEventListener('keydown', e => {
  if (e.key === '1') label('cat_a');
  else if (e.key === '2') label('cat_b');
  else if (e.key === '3') label('not_cat');
  else if (e.key === 'ArrowRight') { cur = Math.min(cur + 1, ROWS.length - 1); render(); }
  else if (e.key === 'ArrowLeft')  { cur = Math.max(cur - 1, 0); render(); }
  else return;
  e.preventDefault();
});
function exportLabels() {
  const out = {};
  ROWS.forEach(r => { if (r.guess) out[r.id] = r.guess; });
  const blob = new Blob([JSON.stringify(out, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'labels.json';
  a.click();
}
render();
</script>
"""


def is_dark_object(m):
    """Frigate's false positives on the dark object by the window: a wide
    box hugging the left frame edge over a very dark crop. Pre-seeds the
    not_cat guess so those only need confirming, not classifying."""
    x, _, w, _ = m["box"]
    return m["mean"] < 45 and x < 0.02 and w > 0.30


def main():
    review = "--review" in sys.argv
    labels = {}
    labels_path = os.path.join(HERE, "labels.json")
    if review:
        if not os.path.exists(labels_path):
            raise SystemExit("--review needs labels.json next to this script")
        labels = json.load(open(labels_path))

    meta = json.load(open(os.path.join(DATA, "meta.json")))
    if review:
        # group by current label so a wrong one stands out against its
        # neighbours; within a group, darkest first
        order = {c: i for i, c in enumerate(["cat_a", "cat_b", "not_cat", ""])}
        meta.sort(key=lambda m: (order.get(labels.get(m["id"], ""), 9),
                                 m["mean"], m["t"]))
    else:
        # darkest first, so the false positives cluster at the top of the page
        meta.sort(key=lambda m: (m["mean"], m["t"]))

    rows = []
    for m in meta:
        path = os.path.join(SRC, m["id"] + ".jpg")
        if not os.path.exists(path):
            continue
        with open(path, "rb") as fh:
            src = base64.b64encode(fh.read()).decode()
        if review:
            guess = labels.get(m["id"], "")
        else:
            guess = "not_cat" if is_dark_object(m) else ""
        rows.append({
            "id": m["id"],
            "src": "data:image/jpeg;base64," + src,
            "t": datetime.datetime.fromtimestamp(m["t"]).strftime("%m-%d %H:%M:%S"),
            "guess": guess,
        })

    out = os.path.join(HERE, "label.html")
    with open(out, "w") as fh:
        fh.write(HTML.replace("__ROWS__", json.dumps(rows)))
    seeded = sum(1 for r in rows if r["guess"])
    mode = "review (grouped by current label)" if review else "fresh"
    print(f"wrote {out} with {len(rows)} crops - {mode}, {seeded} pre-set")
    if review:
        print("re-export when done, then re-run apply_labels.py")


if __name__ == "__main__":
    main()
