import casioplot
import random

WIDTH, HEIGHT, CELL_SIZE = 384, 192, 8
BLACK, WHITE, YELLOW, RED, PINK, CYAN, ORANGE, BLUE, GREEN = (0,0,0), (255,255,255), (255,255,0), (255,0,0), (255,192,203), (0,255,255), (255,165,0), (0,0,255), (0,255,0)
UP, DOWN, LEFT, RIGHT = (0,-1), (0,1), (-1,0), (1,0)
PACMAN_SPEED, GHOST_SPEED, POWER_DURATION, COMBO_BASE, INVINCIBLE_FRAMES = 4, 8, 60, 200, 30

MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,0,0,0,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,0,0,0,0,2,1,0,0,0,1,2,0,0,0,0,0,0,0,0,0,2,1,0,0,0,1,2,0,0,0,0,1,2,1,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,2,1,1,1,2,1,2,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1,2,0,2,1,2,1,1,1,2,1,2,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,2,0,0,0,2,0,2,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,2,0,2,0,0,0,2,0,2,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,2,1,1,1,2,1,2,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,2,0,2,1,2,1,1,1,2,1,2,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,2,0,0,0,2,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,1,2,0,0,0,2,1,2,1,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,2,1,1,1,2,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,2,1,2,1,1,1,2,1,2,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MW, MH = len(MAZE[0]), len(MAZE)
PELLETS = sum(1 for row in MAZE for cell in row if cell in [2, 3])

class PacMan:
    def __init__(self):
        self.x, self.y, self.direction, self.next_direction = 24, 17, LEFT, LEFT
        self.mouth_open, self.mouth_counter, self.invincible, self.invincible_timer = True, 0, False, 0
    
    def move(self, maze):
        for d in [self.next_direction, self.direction]:
            nx, ny = self.x + d[0], self.y + d[1]
            if 0 <= nx < MW and 0 <= ny < MH and maze[ny][nx] != 1:
                self.x, self.y, self.direction = nx, ny, d
                return True
        return False
    
    def animate(self):
        self.mouth_counter = (self.mouth_counter + 1) % 6
        if self.mouth_counter == 0: self.mouth_open = not self.mouth_open
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0: self.invincible = False
    
    def reset(self):
        self.x, self.y, self.direction, self.next_direction = 24, 17, LEFT, LEFT
        self.invincible, self.invincible_timer = True, INVINCIBLE_FRAMES

class Ghost:
    def __init__(self, x, y, color, sx, sy):
        self.x, self.y, self.sx, self.sy, self.color = x, y, sx, sy, color
        self.direction, self.frightened, self.timer, self.eaten = random.choice([UP, DOWN, LEFT, RIGHT]), False, 0, False
    
    def move(self, maze, px, py):
        if self.frightened and not self.eaten:
            self.timer -= 1
            if self.timer <= 0: self.frightened = False
        
        if self.eaten and self.x == self.sx and self.y == self.sy:
            self.eaten = False
        
        # AI direction selection
        if self.eaten:
            dx, dy = self.sx - self.x, self.sy - self.y
        elif self.frightened and random.random() < 0.5:
            dx, dy = self.x - px, self.y - py
        elif not self.frightened and random.random() < 0.4:
            dx, dy = px - self.x, py - self.y
        else:
            dx = dy = 0
        
        if dx or dy:
            self.direction = (RIGHT if dx > 0 else LEFT) if abs(dx) > abs(dy) else (DOWN if dy > 0 else UP)
        
        moves = [d for d in [UP, DOWN, LEFT, RIGHT] 
                 if 0 <= self.x + d[0] < MW and 0 <= self.y + d[1] < MH and maze[self.y + d[1]][self.x + d[0]] != 1]
        
        if self.direction in moves or not moves:
            d = self.direction if self.direction in moves else random.choice(moves) if moves else (0, 0)
            self.x, self.y = self.x + d[0], self.y + d[1]
    
    def reset(self):
        self.x, self.y, self.frightened, self.eaten, self.timer = self.sx, self.sy, False, False, 0

def draw_cell(x, y, color):
    sx, sy = x * CELL_SIZE, y * CELL_SIZE
    for i in range(CELL_SIZE):
        for j in range(CELL_SIZE):
            casioplot.set_pixel(sx + i, sy + j, color)

def draw_maze_cell(x, y, cell_type):
    if cell_type == 1:
        draw_cell(x, y, BLUE)
    elif cell_type in [2, 3]:
        cx, cy = x * CELL_SIZE + 4, y * CELL_SIZE + 4
        r = 2 if cell_type == 3 else 0
        for dx in range(-r, r + 2):
            for dy in range(-r, r + 2):
                if (cell_type == 2 and dx in [0, 1] and dy in [0, 1]) or (cell_type == 3 and dx*dx + dy*dy <= 4):
                    casioplot.set_pixel(cx + dx, cy + dy, WHITE)

def draw_pacman(x, y, d, mouth):
    cx, cy = x * CELL_SIZE + 4, y * CELL_SIZE + 4
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 9:
                if mouth and ((d == RIGHT and dx > 0 and abs(dy) < abs(dx)) or \
                   (d == LEFT and dx < 0 and abs(dy) < abs(dx)) or \
                   (d == UP and dy < 0 and abs(dx) < abs(dy)) or \
                   (d == DOWN and dy > 0 and abs(dx) < abs(dy))):
                    continue
                casioplot.set_pixel(cx + dx, cy + dy, YELLOW)

def draw_ghost(x, y, color, frightened, eaten, blink=False):
    cx, cy = x * CELL_SIZE + 4, y * CELL_SIZE + 4
    if not eaten:
        c = (WHITE if blink else BLUE) if frightened else color
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if (dy <= 0 and dx*dx + dy*dy <= 9) or dy > 0:
                    casioplot.set_pixel(cx + dx, cy + dy, c)
    if eaten or not frightened or blink:
        for ex in [-2, -1, 1, 2]:
            casioplot.set_pixel(cx + ex, cy - 1, WHITE)

high_score = 0

def draw_ui(score, lives):
    for x in range(60):
        for y in range(10):
            casioplot.set_pixel(x, y, BLACK)
    casioplot.draw_string(2, 2, str(score), WHITE, "small")
    for i in range(lives):
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx*dx + dy*dy <= 4:
                    casioplot.set_pixel(WIDTH - 30 + i * 8 + dx, 5 + dy, YELLOW)

def main():
    global high_score
    casioplot.clear_screen()
    maze = [row[:] for row in MAZE]
    for y in range(MH):
        for x in range(MW):
            if maze[y][x]: draw_maze_cell(x, y, maze[y][x])
    
    pacman = PacMan()
    ghosts = [Ghost(22, 9, RED, 22, 9), Ghost(24, 9, PINK, 24, 9), Ghost(26, 9, CYAN, 26, 9), Ghost(24, 11, ORANGE, 24, 11)]
    score, lives, pellets_eaten, iteration, ghost_combo = 0, 3, 0, 0, 0
    old_pos = [(pacman.x, pacman.y)] + [(g.x, g.y) for g in ghosts]
    
    draw_ui(score, lives)
    draw_pacman(pacman.x, pacman.y, pacman.direction, pacman.mouth_open)
    for g in ghosts: draw_ghost(g.x, g.y, g.color, g.frightened, g.eaten)
    casioplot.show_screen()
    
    while lives > 0 and pellets_eaten < PELLETS:
        iteration += 1
        key = str(casioplot.getkey())
        
        if key == "14": pacman.next_direction = UP
        elif key == "34": pacman.next_direction = DOWN
        elif key == "23": pacman.next_direction = LEFT
        elif key == "25": pacman.next_direction = RIGHT
        elif key == "9":
            casioplot.draw_string(WIDTH // 2 - 30, HEIGHT // 2, "PAUSED", YELLOW, "large")
            casioplot.show_screen()
            while str(casioplot.getkey()) != "9": pass
        
        moved = False
        if iteration % PACMAN_SPEED == 0:
            old_pos[0] = (pacman.x, pacman.y)
            moved = pacman.move(maze)
            pacman.animate()
            cell = maze[pacman.y][pacman.x]
            if cell in [2, 3]:
                maze[pacman.y][pacman.x] = 0
                score += 10 if cell == 2 else 50
                pellets_eaten += 1
                if cell == 3:
                    ghost_combo = 0
                    for g in ghosts:
                        if not g.eaten: g.frightened, g.timer = True, POWER_DURATION
        
        if iteration % GHOST_SPEED == 0:
            for i in range(len(ghosts)):
                g = ghosts[i]
                old_pos[i+1] = (g.x, g.y)
                g.move(maze, pacman.x, pacman.y)
                
                if g.x == pacman.x and g.y == pacman.y and not pacman.invincible:
                    if g.frightened and not g.eaten:
                        ghost_combo += 1
                        score += COMBO_BASE * ghost_combo
                        g.eaten, g.frightened = True, False
                    elif not g.eaten:
                        lives -= 1
                        if lives > 0:
                            pacman.reset()
                            for gh in ghosts: gh.reset()
                            for y in range(MH):
                                for x in range(MW):
                                    if maze[y][x]: draw_maze_cell(x, y, maze[y][x])
                            moved = True
            moved = True
        
        if moved or iteration % PACMAN_SPEED == 0:
            for ox, oy in old_pos:
                draw_cell(ox, oy, BLACK)
                if maze[oy][ox]: draw_maze_cell(ox, oy, maze[oy][ox])
            
            if not pacman.invincible or iteration % 4 < 2:
                draw_pacman(pacman.x, pacman.y, pacman.direction, pacman.mouth_open)
            
            for g in ghosts:
                blink = g.frightened and g.timer < 20 and iteration % 4 < 2
                draw_ghost(g.x, g.y, g.color, g.frightened, g.eaten, blink)
            
            draw_ui(score, lives)
            casioplot.show_screen()
            old_pos = [(pacman.x, pacman.y)] + [(g.x, g.y) for g in ghosts]
    
    if score > high_score: high_score = score
    
    casioplot.clear_screen()
    result = "YOU WIN!" if pellets_eaten >= PELLETS else "GAME OVER"
    color = YELLOW if pellets_eaten >= PELLETS else RED
    casioplot.draw_string(WIDTH // 2 - 40, HEIGHT // 2 - 30, result, color, "large")
    casioplot.draw_string(WIDTH // 2 - 40, HEIGHT // 2 - 5, "Score: " + str(score), WHITE, "medium")
    casioplot.draw_string(WIDTH // 2 - 40, HEIGHT // 2 + 15, "High: " + str(high_score), GREEN, "medium")
    casioplot.draw_string(WIDTH // 2 - 60, HEIGHT // 2 + 35, "Press EXE to restart", WHITE, "small")
    casioplot.show_screen()
    while str(casioplot.getkey()) != "9": pass
    main()

main()

