# engine.py - Optimized raycaster for CG100
# All intersections inlined into render loop.
# Local var caching + loop unrolling for speed.
# STRIP is hardcoded to 6 in unrolled pixel loops.
from casioplot import set_pixel, clear_screen
from casioplot import show_screen
from math import sin, cos, sqrt

# Screen
W = 384
H = 192
HALF_H = 96

# Ray config (STRIP=6 -> 64 rays)
STRIP = 6
NUM_RAYS = 64
FOV = 1.0472
HALF_FOV = FOV / 2
ANGLE_STEP = FOV / NUM_RAYS
MAX_DIST = 20.0

# Pre-computed tables
_ray_a = []
_ray_c = []

def init_tables():
  global _ray_a, _ray_c
  _ray_a = []
  _ray_c = []
  for i in range(NUM_RAYS):
    a = -HALF_FOV + (i + 0.5) * ANGLE_STEP
    _ray_a.append(a)
    _ray_c.append(cos(a))

def render(px, py, pa, boxes, spheres, colors,
           c_ceil, c_floor):
  # Cache globals/attrs as locals (big uPy win)
  sp = set_pixel
  _cos = cos
  _sin = sin
  _sqrt = sqrt
  _int = int
  _abs = abs
  ra_tbl = _ray_a
  rc_tbl = _ray_c
  md = MAX_DIST
  h = H
  hh = HALF_H
  st = STRIP

  clear_screen()

  for i in range(NUM_RAYS):
    ra = pa + ra_tbl[i]
    dx = _cos(ra)
    dy = _sin(ra)
    bt = md
    bw = 0
    bs = 0

    # -- Inline box intersection (slab method) --
    for b in boxes:
      bx0 = b[0]; by0 = b[1]
      bx1 = b[2]; by1 = b[3]
      if _abs(dx) < 1e-9:
        if px < bx0 or px > bx1:
          continue
        txn = -999999.0; txf = 999999.0
      else:
        inv = 1.0 / dx
        txn = (bx0 - px) * inv
        txf = (bx1 - px) * inv
        if txn > txf:
          txn, txf = txf, txn
      if _abs(dy) < 1e-9:
        if py < by0 or py > by1:
          continue
        tyn = -999999.0; tyf = 999999.0
      else:
        inv = 1.0 / dy
        tyn = (by0 - py) * inv
        tyf = (by1 - py) * inv
        if tyn > tyf:
          tyn, tyf = tyf, tyn
      if txn > tyn:
        te = txn; sd = 0
      else:
        te = tyn; sd = 1
      tx = txf if txf < tyf else tyf
      if te > tx or tx < 0:
        continue
      t = te
      if t < 0:
        t = tx
        if t < 0:
          continue
        sd = 0 if tx == txf else 1
      if t < bt:
        bt = t; bs = sd; bw = b[4]

    # -- Inline sphere intersection --
    for s in spheres:
      scx = s[0]; scy = s[1]; sr = s[2]
      lx = scx - px; ly = scy - py
      tca = lx * dx + ly * dy
      d2 = lx * lx + ly * ly - tca * tca
      r2 = sr * sr
      if d2 > r2:
        continue
      thc = _sqrt(r2 - d2)
      t = tca - thc
      if t < 0.01:
        t = tca + thc
      if t < 0.01:
        continue
      if t < bt:
        hx = px + dx * t - scx
        hy = py + dy * t - scy
        bt = t; bw = s[3]
        bs = 0 if _abs(hx) > _abs(hy) else 1

    # Fishbowl correction
    dist = bt * rc_tbl[i]
    if dist < 0.1:
      dist = 0.1

    # Wall height
    wh = _int(h / dist)
    if wh > h:
      wh = h
    y0 = hh - wh // 2
    y1 = y0 + wh - 1
    x = i * st

    # Ceiling (unrolled STRIP=6)
    if y0 > 0:
      row = 0
      while row < y0:
        sp(x, row, c_ceil)
        sp(x + 1, row, c_ceil)
        sp(x + 2, row, c_ceil)
        sp(x + 3, row, c_ceil)
        sp(x + 4, row, c_ceil)
        sp(x + 5, row, c_ceil)
        row += 1

    # Wall (unrolled STRIP=6, inline shade)
    if bw > 0:
      key = (bw, bs)
      if key in colors:
        bc = colors[key]
      else:
        bc = (200, 200, 200)
      f = 1.0 - dist / md
      if f < 0.12:
        f = 0.12
      c = (_int(bc[0] * f), _int(bc[1] * f),
           _int(bc[2] * f))
      row = y0
      ey = y1 + 1
      while row < ey:
        sp(x, row, c)
        sp(x + 1, row, c)
        sp(x + 2, row, c)
        sp(x + 3, row, c)
        sp(x + 4, row, c)
        sp(x + 5, row, c)
        row += 1

    # Floor (unrolled STRIP=6)
    if y1 < h - 1:
      row = y1 + 1
      while row < h:
        sp(x, row, c_floor)
        sp(x + 1, row, c_floor)
        sp(x + 2, row, c_floor)
        sp(x + 3, row, c_floor)
        sp(x + 4, row, c_floor)
        sp(x + 5, row, c_floor)
        row += 1

  show_screen()
