# A fotóból vektoros rajzot készít az ábrához (karosszéria, árnyalat, sötét felületek, vonalak).
# Használat: pip install opencv-python-headless potracer
#            python3 tools/trace.py foto.png jazz.json
import sys, numpy as np, cv2, potrace
src, out = sys.argv[1], sys.argv[2]
S = 4
img = cv2.imread(src)
img = cv2.resize(img, None, fx=S, fy=S, interpolation=cv2.INTER_LANCZOS4)
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# háttér: a szélekhez kapcsolódó közel-fehér terület
white = (img.min(axis=2) > 232).astype(np.uint8)
n, lab = cv2.connectedComponents(white)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
bg = np.isin(lab, [l for l in border if l != 0]) & (white > 0)
car = (~bg).astype(np.uint8)
car = cv2.morphologyEx(car, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(car)
big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
car = (lab == big).astype(np.uint8)
car = cv2.morphologyEx(car, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
# lyukak kitöltése
ff = car.copy(); mask = np.zeros((h + 2, w + 2), np.uint8); cv2.floodFill(ff, mask, (0, 0), 1)
car = car | (1 - ff)

# sötét felületek: üveg, gumi, rács
blur = cv2.GaussianBlur(gray, (0, 0), 3)
dark = ((blur < 78) & (car > 0)).astype(np.uint8)
dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))

# középtónus: árnyékos felületek (enyhe tónus)
mid = ((blur < 150) & (blur >= 78) & (car > 0)).astype(np.uint8)
mid = cv2.morphologyEx(mid, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))

# vonalak: XDoG-szerű rajzolat
g = gray.astype(np.float32) / 255
g1 = cv2.GaussianBlur(g, (0, 0), 2.2); g2 = cv2.GaussianBlur(g, (0, 0), 2.2 * 1.6)
d = g1 - 0.985 * g2
lines = (d < -0.012).astype(np.uint8)
edge = cv2.morphologyEx(car, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8))
lines = (lines | edge) & cv2.dilate(car, np.ones((7, 7), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(lines)
keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] > 60
lines = keep[lab].astype(np.uint8)

def to_path(bm, turd=40, tol=0.4):
    p = potrace.Bitmap(~bm.astype(bool)).trace(turdsize=turd, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=tol)
    f = lambda q: f"{q.x:.1f} {q.y:.1f}"
    parts = []
    for c in p:
        parts.append("M" + f(c.start_point))
        for seg in c.segments:
            if seg.is_corner: parts.append("L" + f(seg.c) + "L" + f(seg.end_point))
            else: parts.append("C" + f(seg.c1) + " " + f(seg.c2) + " " + f(seg.end_point))
        parts.append("Z")
    return "".join(parts)

res = {"w": w, "h": h, "car": to_path(car, 200), "mid": to_path(mid, 300, 0.6), "dark": to_path(dark, 120), "lines": to_path(lines, 20, 0.3)}
import json; json.dump(res, open(out, "w"))
print(w, h, {k: len(v) for k, v in res.items() if isinstance(v, str)})
# előnézet
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w//2}" height="{h//2}"><rect width="100%" height="100%" fill="#fff"/><path d="{res["car"]}" fill="#aebdd3" fill-opacity=".55"/><path d="{res["mid"]}" fill="#17202a" fill-opacity=".12"/><path d="{res["dark"]}" fill="#17202a" fill-opacity=".8"/><path d="{res["lines"]}" fill="#17202a"/></svg>'
open(out.replace('.json', '.svg'), 'w').write(svg)
