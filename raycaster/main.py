# main.py - Raycaster demo for CG100
# Bounding box / sphere intersection approach.
# Run this file from the Python app.
from casioplot import getkey, draw_string
from casioplot import show_screen, clear_screen
from math import sin, cos
from map_data import BOXES, SPHERES
from map_data import START_X, START_Y, START_A
from map_data import COLORS, C_CEIL, C_FLOOR
from engine import init_tables, render

# --- Key codes (strings) for fx-CG100 ---
K_UP = "14"
K_DOWN = "34"
K_LEFT = "23"
K_RIGHT = "25"
K_BACK = "22"
K_OK = "24"
K_NONE = "0"

# Movement settings
MOVE_SPD = 0.18
ROT_SPD = 0.13
COL_R = 0.2  # collision radius

def blocked(nx, ny):
  """Check if (nx,ny) overlaps any AABB."""
  r = COL_R
  for b in BOXES:
    if (nx + r > b[0] and nx - r < b[2] and
        ny + r > b[1] and ny - r < b[3]):
      return True
  for s in SPHERES:
    dx = nx - s[0]
    dy = ny - s[1]
    if dx * dx + dy * dy < (s[2] + r) ** 2:
      return True
  return False

# Player state
px = START_X
py = START_Y
pa = START_A

def handle_input():
  global px, py, pa
  k = str(getkey())
  if k == K_NONE:
    return True
  if k == K_BACK:
    return False
  if k == K_UP:
    nx = px + cos(pa) * MOVE_SPD
    ny = py + sin(pa) * MOVE_SPD
    if not blocked(nx, ny):
      px = nx
      py = ny
  elif k == K_DOWN:
    nx = px - cos(pa) * MOVE_SPD
    ny = py - sin(pa) * MOVE_SPD
    if not blocked(nx, ny):
      px = nx
      py = ny
  elif k == K_LEFT:
    pa -= ROT_SPD
  elif k == K_RIGHT:
    pa += ROT_SPD
  return True

def splash():
  clear_screen()
  draw_string(80, 60, "RAYCASTER", (0,0,0), "large")
  draw_string(60, 90, "BBox/Sphere Engine",
              (80,80,80), "medium")
  draw_string(70, 120, "Press OK to start",
              (80,80,80), "medium")
  show_screen()
  while str(getkey()) != K_OK:
    pass

def run():
  splash()
  init_tables()
  while True:
    render(px, py, pa, BOXES, SPHERES,
           COLORS, C_CEIL, C_FLOOR)
    if not handle_input():
      break

run()
