# map_data.py - Scene data for CG100 raycaster
# Uses AABB walls and spheres instead of a tile grid
# for fastest ray intersection performance.

# --- AABB walls ---
# Each: (x0, y0, x1, y1, wall_type)
# Thin boxes represent wall segments.
T = 0.2  # wall thickness

BOXES = [
  # Outer boundary
  (0, 0, 16, T, 1),        # north
  (0, 16-T, 16, 16, 1),    # south
  (0, 0, T, 16, 1),        # west
  (16-T, 0, 16, 16, 1),    # east
  # Inner room divider (horizontal)
  (3, 5, 7, 5+T, 2),
  (9, 5, 13, 5+T, 2),
  # Inner room divider (vertical)
  (7, 5, 7+T, 9, 2),
  # L-shaped wall
  (10, 9, 13, 9+T, 3),
  (10, 9, 10+T, 12, 3),
  # Small room box
  (3, 10, 6, 10+T, 2),
  (3, 12-T, 6, 12, 2),
  (3, 10, 3+T, 12, 2),
  (6-T, 10, 6, 11, 2),
]

# --- Sphere pillars ---
# Each: (cx, cy, radius, wall_type)
SPHERES = [
  (8, 8, 0.4, 4),    # center pillar
  (4, 3, 0.3, 5),    # small pillar
  (12, 3, 0.3, 5),   # small pillar
  (12, 13, 0.5, 4),  # large pillar
]

# Player start position
START_X = 2.0
START_Y = 2.0
START_A = 0.0  # radians, facing east

# Wall colors (R,G,B) per wall_type and side
# side: 0 = X-face (E/W, lit), 1 = Y-face (N/S, dark)
COLORS = {
  (1, 0): (180, 180, 180),
  (1, 1): (120, 120, 120),
  (2, 0): (200, 60, 60),
  (2, 1): (140, 40, 40),
  (3, 0): (60, 60, 200),
  (3, 1): (40, 40, 140),
  (4, 0): (60, 180, 60),
  (4, 1): (40, 130, 40),
  (5, 0): (200, 180, 50),
  (5, 1): (150, 130, 30),
}

# Ceiling and floor
C_CEIL = (40, 40, 50)
C_FLOOR = (80, 80, 80)
