# engine.py - Bounding box/sphere raycaster for CG100
# Uses slab method for AABB and analytic test for
# spheres. No grid traversal — direct intersection.
from casioplot import set_pixel, clear_screen, show_screen
from math import sin, cos, pi, sqrt

# Screen constants
W = 384
H = 192
HALF_H = 96

# Raycasting config
STRIP = 6           # px per column (384/6 = 64 rays)
NUM_RAYS = 64
FOV = 1.0472        # ~60 degrees
HALF_FOV = FOV / 2
ANGLE_STEP = FOV / NUM_RAYS
MAX_DIST = 20.0

# Pre-computed per-ray data (filled by init_tables)
_ray_a = []   # angle offset from player
_ray_c = []   # cos of offset (fishbowl fix)

def init_tables():
  global _ray_a, _ray_c
  _ray_a = []
  _ray_c = []
  for i in range(NUM_RAYS):
    a = -HALF_FOV + (i + 0.5) * ANGLE_STEP
    _ray_a.append(a)
    _ray_c.append(cos(a))

def ray_box(ox, oy, dx, dy, box):
  """Ray-AABB slab intersection.
  box = (x0, y0, x1, y1, wtype).
  Returns (t, side, wtype) or None.
  side: 0=X-face, 1=Y-face."""
  x0 = box[0]; y0 = box[1]
  x1 = box[2]; y1 = box[3]

  # X slabs
  if abs(dx) < 1e-9:
    if ox < x0 or ox > x1:
      return None
    txn = -999999.0
    txf = 999999.0
  else:
    inv = 1.0 / dx
    txn = (x0 - ox) * inv
    txf = (x1 - ox) * inv
    if txn > txf:
      txn, txf = txf, txn

  # Y slabs
  if abs(dy) < 1e-9:
    if oy < y0 or oy > y1:
      return None
    tyn = -999999.0
    tyf = 999999.0
  else:
    inv = 1.0 / dy
    tyn = (y0 - oy) * inv
    tyf = (y1 - oy) * inv
    if tyn > tyf:
      tyn, tyf = tyf, tyn

  # Find overlap
  if txn > tyn:
    t_enter = txn
    side = 0
  else:
    t_enter = tyn
    side = 1
  t_exit = txf if txf < tyf else tyf

  if t_enter > t_exit or t_exit < 0:
    return None

  t = t_enter
  if t < 0:
    t = t_exit
    if t < 0:
      return None
    # Flip side for interior hit
    if t_exit == txf:
      side = 0
    else:
      side = 1

  return (t, side, box[4])

def ray_sphere(ox, oy, dx, dy, sph):
  """Ray-circle intersection (2D sphere slice).
  sph = (cx, cy, r, wtype).
  Returns (t, side, wtype) or None."""
  cx = sph[0]; cy = sph[1]; r = sph[2]
  lx = cx - ox
  ly = cy - oy
  # Project center onto ray (dir is unit length)
  tca = lx * dx + ly * dy
  d2 = lx * lx + ly * ly - tca * tca
  r2 = r * r
  if d2 > r2:
    return None
  thc = sqrt(r2 - d2)
  t = tca - thc
  if t < 0.01:
    t = tca + thc
  if t < 0.01:
    return None
  # Determine side from hit normal
  hx = ox + dx * t - cx
  hy = oy + dy * t - cy
  if abs(hx) > abs(hy):
    side = 0
  else:
    side = 1
  return (t, side, sph[3])

def cast_ray(ox, oy, dx, dy, boxes, spheres):
  """Test ray against all objects. Returns
  (dist, wtype, side) of closest hit."""
  best_t = MAX_DIST
  best_w = 0
  best_s = 0

  for b in boxes:
    hit = ray_box(ox, oy, dx, dy, b)
    if hit is not None and hit[0] < best_t:
      best_t = hit[0]
      best_s = hit[1]
      best_w = hit[2]

  for s in spheres:
    hit = ray_sphere(ox, oy, dx, dy, s)
    if hit is not None and hit[0] < best_t:
      best_t = hit[0]
      best_s = hit[1]
      best_w = hit[2]

  return (best_t, best_w, best_s)

def _shade(color, dist):
  """Darken RGB by distance (fog)."""
  f = 1.0 - dist / MAX_DIST
  if f < 0.12:
    f = 0.12
  return (int(color[0]*f), int(color[1]*f),
          int(color[2]*f))

def render(px, py, pa, boxes, spheres, colors,
           c_ceil, c_floor):
  """Render one frame using bbox/sphere tests."""
  clear_screen()

  for i in range(NUM_RAYS):
    ra = pa + _ray_a[i]
    dx = cos(ra)
    dy = sin(ra)

    dist, wtype, side = cast_ray(
      px, py, dx, dy, boxes, spheres)

    # Fishbowl correction
    dist *= _ray_c[i]
    if dist < 0.1:
      dist = 0.1

    # Wall strip height
    wh = int(H / dist)
    if wh > H:
      wh = H
    y0 = HALF_H - wh // 2
    y1 = y0 + wh - 1

    x = i * STRIP
    x1 = x + STRIP

    # Ceiling
    if y0 > 0:
      row = 0
      while row < y0:
        col = x
        while col < x1:
          set_pixel(col, row, c_ceil)
          col += 1
        row += 1

    # Wall strip
    if wtype > 0:
      key = (wtype, side)
      if key in colors:
        c = _shade(colors[key], dist)
      else:
        c = _shade((200, 200, 200), dist)
      row = y0
      ey = y1 + 1
      while row < ey:
        col = x
        while col < x1:
          set_pixel(col, row, c)
          col += 1
        row += 1

    # Floor
    if y1 < H - 1:
      row = y1 + 1
      while row < H:
        col = x
        while col < x1:
          set_pixel(col, row, c_floor)
          col += 1
        row += 1

  show_screen()
