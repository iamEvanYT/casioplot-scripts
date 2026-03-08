# bj_ui.py - Card UI for CG100 Blackjack
from casioplot import set_pixel, draw_string
# Suit 5x5 bitmaps (MSB = left pixel)
# H=heart D=diamond S=spade C=club
SB = {'H': [10,31,31,14,4], 'D': [4,14,31,14,4],
      'S': [4,14,31,4,14], 'C': [10,31,14,4,14]}
RED = (200, 30, 30)
BLK = (0, 0, 0)
WHT = (255, 255, 255)
GRN = (30, 110, 50)
DGRY = (50, 50, 50)
LGRY = (170, 170, 170)
BLUE = (35, 45, 110)
GOLD = (200, 180, 30)
WGRN = (30, 160, 30)
SCOL = {'H': RED, 'D': RED, 'S': BLK, 'C': BLK}
CW = 28
CH = 40
CG = 3

def fill_rect(x, y, w, h, c):
  sp = set_pixel
  ye = y + h; xe = x + w
  r = y
  while r < ye:
    co = x
    while co < xe:
      sp(co, r, c)
      co += 1
    r += 1

def _bdr(x, y, w, h):
  sp = set_pixel; c = BLK
  for i in range(w):
    sp(x+i, y, c); sp(x+i, y+h-1, c)
  for i in range(1, h-1):
    sp(x, y+i, c); sp(x+w-1, y+i, c)

def draw_suit(x, y, s, sc):
  sp = set_pixel; c = SCOL[s]; bm = SB[s]
  for r in range(5):
    bits = bm[r]
    for co in range(5):
      if bits & (16 >> co):
        if sc == 1:
          sp(x+co, y+r, c)
        else:
          px = x+co*2; py = y+r*2
          sp(px, py, c); sp(px+1, py, c)
          sp(px, py+1, c); sp(px+1, py+1, c)

def draw_card(x, y, rank, suit):
  _bdr(x, y, CW, CH)
  fill_rect(x+1, y+1, CW-2, CH-2, WHT)
  draw_string(x+2, y+2, rank, SCOL[suit], "small")
  draw_suit(x+3, y+13, suit, 1)
  draw_suit(x+9, y+24, suit, 2)

def draw_back(x, y):
  _bdr(x, y, CW, CH)
  fill_rect(x+1, y+1, CW-2, CH-2, BLUE)

def draw_hand(cards, cy, hide=False, sx=10):
  x = sx
  for i in range(len(cards)):
    if i == 1 and hide:
      draw_back(x, cy)
    else:
      draw_card(x, cy, cards[i][0], cards[i][1])
    x += CW + CG

def draw_hud(cash, bet):
  fill_rect(0, 0, 384, 18, GRN)
  draw_string(5, 3, "Cash: $"+str(cash), WHT, "small")
  if bet > 0:
    draw_string(200, 3, "Bet: $"+str(bet), WHT, "small")

def draw_btn(x, y, w, text, sel):
  c = BLK if sel else DGRY
  tc = WHT if sel else LGRY
  _bdr(x, y, w, 20)
  fill_rect(x+1, y+1, w-2, 18, c)
  draw_string(x+8, y+5, text, tc, "small")

def draw_btns(opts, sel, y=160):
  n = len(opts); bw = 80; gap = 8
  total = n * bw + (n-1) * gap
  sx = (384 - total) // 2
  for i in range(n):
    draw_btn(sx + i*(bw+gap), y, bw, opts[i], i==sel)
