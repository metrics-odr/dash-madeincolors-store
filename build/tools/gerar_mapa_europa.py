#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera build/mapa-europa.js (EU_MAP) a partir do world-atlas (Natural Earth 50m, TopoJSON público).
Uso: python build/tools/gerar_mapa_europa.py countries-50m.json build/mapa-europa.js
Projeção Lambert azimutal de áreas iguais centrada na Europa; só polígonos dentro do recorte."""
import json, math, sys

LON0, LAT0 = math.radians(12), math.radians(53)
BBOX = (-25, 33.5, 42, 71.5)           # lon min, lat min, lon max, lat max (recorte da Europa)
W = 600


def proj(lon, lat):
    l, p = math.radians(lon), math.radians(lat)
    k = math.sqrt(2 / (1 + math.sin(LAT0) * math.sin(p) + math.cos(LAT0) * math.cos(p) * math.cos(l - LON0)))
    return (k * math.cos(p) * math.sin(l - LON0),
            -k * (math.cos(LAT0) * math.sin(p) - math.sin(LAT0) * math.cos(p) * math.cos(l - LON0)))


def decode(topo):
    sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]
    arcs = []
    for a in topo["arcs"]:
        x = y = 0; pts = []
        for dx, dy in a:
            x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def ring(arcs, idxs):
    out = []
    for i in idxs:
        pts = arcs[i] if i >= 0 else arcs[~i][::-1]
        out += pts if not out else pts[1:]
    return out


def dp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]; dm, di = 0, 0
    d = math.hypot(x2 - x1, y2 - y1) or 1e-9
    for i in range(1, len(pts) - 1):
        x, y = pts[i]; dist = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / d
        if dist > dm: dm, di = dist, i
    if dm > eps: return dp(pts[:di + 1], eps)[:-1] + dp(pts[di:], eps)
    return [pts[0], pts[-1]]


def inside(pts):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    return BBOX[0] <= cx <= BBOX[2] and BBOX[1] <= cy <= BBOX[3]


def main(src, dst):
    topo = json.load(open(src)); arcs = decode(topo); shapes = {}
    for g in topo["objects"]["countries"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]] if g["type"] == "Polygon" else []
        keep = []
        for poly in polys:
            r = ring(arcs, poly[0])
            if len(r) > 3 and inside(r): keep.append([ring(arcs, x) for x in poly])
        if keep: shapes[g["properties"]["name"]] = keep
    allp = [proj(*pt) for ps in shapes.values() for poly in ps for rg in poly for pt in rg]
    # recorte por lon/lat aplicado nos pontos (clamp) para Rússia/Turquia não estourarem o quadro
    minx = min(p[0] for p in allp); maxx = max(p[0] for p in allp); miny = min(p[1] for p in allp); maxy = max(p[1] for p in allp)
    pts_in = [proj(lo, la) for lo in (BBOX[0], BBOX[2]) for la in (BBOX[1], BBOX[3])] + [proj(12, BBOX[3]), proj(12, BBOX[1])]
    minx = min(p[0] for p in pts_in); maxx = max(p[0] for p in pts_in); miny = min(p[1] for p in pts_in); maxy = max(p[1] for p in pts_in)
    sc = W / (maxx - minx); H = (maxy - miny) * sc
    def xy(pt):
        x, y = proj(min(max(pt[0], BBOX[0] - 2), BBOX[2] + 2), min(max(pt[1], BBOX[1] - 2), BBOX[3] + 2))
        return ((x - minx) * sc, (y - miny) * sc)
    paths = {}
    for name, polys in shapes.items():
        d = []
        for poly in polys:
            for rg in poly:
                q = [xy(p) for p in rg]; h = len(q) // 2
                pts = dp(q[:h + 1], 0.5)[:-1] + dp(q[h:], 0.5)   # anel fechado: divide ao meio p/ a corda não ser nula
                if len(pts) < 4: continue
                d.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
        if d: paths[name] = "".join(d)
    js = ("/* Mapa da Europa (países) — paths SVG simplificados, viewBox 0 0 %d %d. Gerado por build/tools/gerar_mapa_europa.py "
          "a partir do Natural Earth (world-atlas); não editar à mão. */\nconst EU_MAP=" % (W, round(H)))
    js += json.dumps({"vb": [W, round(H)], "paths": paths}, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(dst, "w", encoding="utf-8").write(js)
    print(len(paths), "países,", len(js) // 1024, "KB, vb", W, round(H))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
