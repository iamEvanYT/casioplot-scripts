from casioplot import getkey, show_screen
from casioplot import clear_screen
from bj_ui import *
import random

K_R = "25"; K_L = "23"
K_U = "14"; K_D = "34"
K_OK = "24"; K_BK = "22"

def card_val(c):
  r = c[0]
  if r in ('J', 'Q', 'K'):
    return 10
  if r == 'A':
    return 11
  return int(r)

def hand_val(h):
  v = 0; a = 0
  for c in h:
    v += card_val(c)
    if c[0] == 'A':
      a += 1
  while v > 21 and a > 0:
    v -= 10; a -= 1
  return v

def new_deck():
  d = []
  for s in ['H', 'D', 'S', 'C']:
    for r in ['2','3','4','5','6','7','8',
              '9','10','J','Q','K','A']:
      d.append((r, s))
  return d

def wait_key():
  while True:
    k = str(getkey())
    if k != "0" and k != "None":
      while True:
        r = str(getkey())
        if r == "0" or r == "None":
          break
      return k

def shuffle(d):
  for i in range(len(d) - 1, 0, -1):
    j = random.randint(0, i)
    d[i], d[j] = d[j], d[i]

def tbl(cash, bet, dh, ph, hd, lbl="YOU"):
  """Draw game table (no show_screen)."""
  clear_screen()
  draw_hud(cash, bet)
  if hd:
    draw_string(10, 22, "DEALER", BLK, "small")
  else:
    draw_string(10, 22,
      "DEALER: "+str(hand_val(dh)), BLK, "small")
  draw_hand(dh, 33, hd)
  draw_string(10, 78,
    lbl+": "+str(hand_val(ph)), BLK, "small")
  draw_hand(ph, 89)

def bsel(opts, init=0):
  """Button selector overlay. Returns index."""
  sel = init
  draw_btns(opts, sel)
  show_screen()
  while True:
    k = wait_key()
    if k == K_R:
      sel = min(sel+1, len(opts)-1)
      draw_btns(opts, sel); show_screen()
    elif k == K_L:
      sel = max(sel-1, 0)
      draw_btns(opts, sel); show_screen()
    elif k == K_OK:
      return sel

def get_bet(cash):
  bet = 100; mn = 10
  while True:
    clear_screen()
    draw_hud(cash, 0)
    draw_string(80, 40, "PLACE YOUR BET",
                BLK, "large")
    draw_string(155, 80, "$"+str(bet),
                GRN, "large")
    draw_string(50, 120,
      "L/R: +/-10   U/D: +/-100", LGRY, "small")
    draw_string(85, 150,
      "OK: Deal   BACK: Quit", LGRY, "small")
    show_screen()
    k = wait_key()
    if k == K_R:
      bet = min(bet+10, cash)
    elif k == K_L:
      bet = max(bet-10, mn)
    elif k == K_U:
      bet = min(bet+100, cash)
    elif k == K_D:
      bet = max(bet-100, mn)
    elif k == K_OK:
      if bet <= cash:
        return bet
    elif k == K_BK:
      return 0

def play():
  cash = 1000
  while cash >= 10:
    bet = get_bet(cash)
    if bet == 0:
      clear_screen()
      draw_string(50, 80, "Final: $"+str(cash),
                  BLK, "large")
      show_screen(); wait_key()
      return
    cash -= bet
    deck = new_deck(); shuffle(deck)
    ph = [deck.pop(), deck.pop()]
    dh = [deck.pop(), deck.pop()]
    tbl(cash, bet, dh, ph, True)
    show_screen()
    # Insurance
    ins = 0
    if dh[0][0] == 'A':
      tbl(cash, bet, dh, ph, True)
      draw_string(10, 140, "Insurance?",
                  BLK, "small")
      sel = bsel(["Yes", "No"], 1)
      if sel == 0:
        ib = bet // 2
        if cash >= ib:
          ins = ib; cash -= ib
    # Dealer blackjack
    if hand_val(dh) == 21:
      tbl(cash, bet, dh, ph, False)
      if ins > 0:
        cash += ins * 2
      if hand_val(ph) == 21:
        cash += bet
        draw_string(100, 140, "PUSH",
                    LGRY, "large")
      else:
        draw_string(30, 140, "Dealer BJ!",
                    RED, "large")
      show_screen(); wait_key(); continue
    # Player blackjack
    if hand_val(ph) == 21:
      cash += int(bet * 2.5)
      tbl(cash, bet, dh, ph, False)
      draw_string(10, 140,
        "BLACKJACK! +$"+str(int(bet*1.5)),
        GOLD, "large")
      show_screen(); wait_key(); continue
    # Split
    hands = [ph]; bets = [bet]
    if card_val(ph[0]) == card_val(ph[1]):
      if cash >= bet:
        tbl(cash, bet, dh, ph, True)
        draw_string(10, 140, "Split?",
                    BLK, "small")
        sel = bsel(["Split", "No"], 1)
        if sel == 0:
          cash -= bet
          hands = [[ph[0], deck.pop()],
                   [ph[1], deck.pop()]]
          bets = [bet, bet]
    # Play each hand
    for hi in range(len(hands)):
      h = hands[hi]; b = bets[hi]
      while hand_val(h) < 21:
        if len(hands) > 1:
          lbl = "H" + str(hi+1)
        else:
          lbl = "YOU"
        tbl(cash, b, dh, h, True, lbl)
        opts = ["Hit", "Stand"]
        if len(h) == 2 and cash >= b:
          opts.insert(1, "Double")
        sel = bsel(opts)
        if opts[sel] == "Hit":
          h.append(deck.pop())
        elif opts[sel] == "Double":
          cash -= b; bets[hi] = b * 2
          h.append(deck.pop()); break
        else:
          break
      if hand_val(h) > 21:
        if len(hands) > 1:
          lbl = "H" + str(hi+1)
        else:
          lbl = "YOU"
        tbl(cash, bets[hi], dh, h, True, lbl)
        draw_string(140, 140, "BUST!",
                    RED, "large")
        show_screen(); wait_key()
    # Dealer turn
    while hand_val(dh) < 17:
      dh.append(deck.pop())
    # Resolve
    tr = 0
    for i in range(len(hands)):
      hv = hand_val(hands[i])
      dv = hand_val(dh)
      st = bets[i]
      if hv > 21:
        pass
      elif dv > 21 or hv > dv:
        tr += st * 2
      elif hv == dv:
        tr += st
    cash += tr
    # Result screen
    clear_screen()
    draw_hud(cash, 0)
    draw_string(10, 22,
      "DEALER: "+str(hand_val(dh)), BLK, "small")
    draw_hand(dh, 33)
    if len(hands) == 1:
      draw_string(10, 78,
        "YOU: "+str(hand_val(hands[0])),
        BLK, "small")
      draw_hand(hands[0], 89)
    else:
      draw_string(10, 78,
        "H1: "+str(hand_val(hands[0])),
        BLK, "small")
      draw_hand(hands[0], 89, False, 10)
      draw_string(200, 78,
        "H2: "+str(hand_val(hands[1])),
        BLK, "small")
      draw_hand(hands[1], 89, False, 200)
    net = tr - sum(bets)
    if net > 0:
      draw_string(20, 140, "WIN +$"+str(net),
                  WGRN, "large")
    elif net < 0:
      draw_string(20, 140, "LOSE -$"+str(-net),
                  RED, "large")
    else:
      draw_string(100, 140, "PUSH",
                  LGRY, "large")
    show_screen(); wait_key()
  # Game over
  clear_screen()
  draw_string(80, 70, "GAME OVER", RED, "large")
  draw_string(60, 100, "Final: $"+str(cash),
              BLK, "large")
  show_screen(); wait_key()

play()
