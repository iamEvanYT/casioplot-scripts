from casioplot import *
import random

# --------------------------
# Key constants (STRINGS)
# --------------------------
KEY_RIGHT = "25"
KEY_LEFT  = "23"
KEY_UP    = "14"
KEY_DOWN  = "34"
KEY_OK    = "24"
KEY_BACK  = "22"

# --------------------------
# Card helpers
# --------------------------
def card_val(c):
    if c in ['J','Q','K']:
        return 10
    if c == 'A':
        return 11
    return int(c)

def hand_val(h):
    v = sum(card_val(c) for c in h)
    a = h.count('A')
    while v > 21 and a > 0:
        v -= 10
        a -= 1
    return v

def new_deck():
    return ['2','3','4','5','6','7','8','9','10','J','Q','K','A'] * 4

# --------------------------
# UI helpers
# --------------------------
def draw_button(x, text, selected):
    y = 170
    w = 90
    h = 20
    color = (255,255,255) if selected else (200,200,200)
    for i in range(h):
        for j in range(w):
            set_pixel(x+j, y+i, color)
    draw_string(x+5, y+5, text, (0,0,0), "small")

def draw_buttons(options, sel):
    x = 5
    for i in range(len(options)):
        draw_button(x, options[i], i == sel)
        x += 95

# --------------------------
# Robust string-based key reader with press+release
# --------------------------
def wait_key():
    """
    Wait for a real key press (getkey() returns string != "0" and != "None"),
    then wait for release (getkey() becomes "0" or "None") before returning.
    Returns the key code as a string.
    """
    while True:
        k = str(getkey())
        if k != "0" and k != "None":
            # wait for release
            while True:
                r = str(getkey())
                if r == "0" or r == "None":
                    break
            return k

# --------------------------
# BETTING SCREEN
# --------------------------
def get_bet(cash):
    bet = 100
    min_bet = 10
    while True:
        clear_screen()
        draw_string(10, 10, "Cash: $" + str(cash), (0,0,0), "medium")
        draw_string(10, 30, "Bet:  $" + str(bet),  (0,0,0), "medium")
        draw_string(10, 55, "L/R = +/-10", (0,0,0), "small")
        draw_string(10, 70, "U/D = +/-100", (0,0,0), "small")
        draw_string(10, 90, "OK = confirm", (0,0,0), "small")
        draw_string(10, 105, "BACK = quit", (0,0,0), "small")
        show_screen()

        k = wait_key()
        if k == KEY_RIGHT:
            bet = min(bet + 10, cash)
        elif k == KEY_LEFT:
            bet = max(bet - 10, min_bet)
        elif k == KEY_UP:
            bet = min(bet + 100, cash)
        elif k == KEY_DOWN:
            bet = max(bet - 100, min_bet)
        elif k == KEY_OK:
            if bet <= cash:
                return bet
        elif k == KEY_BACK:
            return 0

# --------------------------
# Display cards
# --------------------------
def show_hand(y, label, cards, hide_second=False):
    t = label + ": "
    for i in range(len(cards)):
        if i == 1 and hide_second:
            t += "? "
        else:
            t += cards[i] + " "
    if not hide_second:
        t += "= " + str(hand_val(cards))
    draw_string(10, y, t, (0,0,0), "medium")

# --------------------------
# MAIN GAME
# --------------------------
def play():
    cash = 1000
    min_bet = 10

    while cash >= min_bet:
        bet = get_bet(cash)
        if bet == 0:
            clear_screen()
            draw_string(10, 90, "Final Cash: $" + str(cash), (0,0,0), "large")
            show_screen()
            wait_key()
            return

        cash -= bet

        # Fisher-Yates shuffle using random.randint (no random.shuffle)
        deck = new_deck()
        for i in range(len(deck)-1, 0, -1):
            j = random.randint(0, i)
            deck[i], deck[j] = deck[j], deck[i]

        p_hand = [deck.pop(), deck.pop()]
        d_hand = [deck.pop(), deck.pop()]

        # Initial render
        clear_screen()
        draw_string(10, 5, "Cash: $" + str(cash), (0,0,0), "small")
        draw_string(10, 20, "Bet:  $" + str(bet), (0,0,0), "small")
        show_hand(40, "Dealer", d_hand, True)
        show_hand(60, "You", p_hand)
        show_screen()

        # Insurance
        ins = 0
        if d_hand[0] == "A":
            draw_buttons(["Yes","No"], 1)
            show_screen()
            sel = 1
            while True:
                k = wait_key()
                if k in (KEY_LEFT, KEY_RIGHT):
                    sel = 1 - sel
                    draw_buttons(["Yes","No"], sel)
                    show_screen()
                elif k == KEY_OK:
                    if sel == 0:
                        ib = bet // 2
                        if cash >= ib:
                            ins = ib
                            cash -= ib
                    break

        # Dealer blackjack check
        if hand_val(d_hand) == 21:
            clear_screen()
            show_hand(30, "Dealer", d_hand)
            show_hand(60, "You", p_hand)
            if ins > 0:
                cash += ins * 2
            if hand_val(p_hand) == 21:
                cash += bet
                draw_string(10, 120, "PUSH", (0,0,0), "large")
            else:
                draw_string(10, 120, "Dealer Blackjack!", (0,0,0), "large")
            show_screen()
            wait_key()
            continue

        # Player blackjack
        if hand_val(p_hand) == 21:
            cash += int(bet * 2.5)
            clear_screen()
            show_hand(30, "Dealer", d_hand)
            show_hand(60, "You", p_hand)
            draw_string(10, 120, "BLACKJACK +$" + str(int(bet * 1.5)), (0,0,0), "large")
            show_screen()
            wait_key()
            continue

        # Split check
        hands = [p_hand]
        bets = [bet]
        if card_val(p_hand[0]) == card_val(p_hand[1]) and cash >= bet:
            draw_buttons(["Split","No"], 1)
            show_screen()
            sel = 1
            while True:
                k = wait_key()
                if k in (KEY_LEFT, KEY_RIGHT):
                    sel = 1 - sel
                    draw_buttons(["Split","No"], sel)
                    show_screen()
                elif k == KEY_OK:
                    if sel == 0:
                        cash -= bet
                        hands = [[p_hand[0], deck.pop()], [p_hand[1], deck.pop()]]
                        bets = [bet, bet]
                    break

        # Play each hand
        for h_index in range(len(hands)):
            h = hands[h_index]
            b = bets[h_index]
            while hand_val(h) < 21:
                clear_screen()
                draw_string(10, 5, "Cash: $" + str(cash), (0,0,0), "small")
                show_hand(30, "Dealer", d_hand, True)
                show_hand(60, "You", h)
                options = ["Hit", "Stand"]
                if len(h) == 2 and cash >= b:
                    options.insert(1, "Double")
                draw_buttons(options, 0)
                show_screen()
                sel = 0
                while True:
                    k = wait_key()
                    if k == KEY_RIGHT:
                        sel = min(sel + 1, len(options) - 1)
                        draw_buttons(options, sel)
                        show_screen()
                    elif k == KEY_LEFT:
                        sel = max(sel - 1, 0)
                        draw_buttons(options, sel)
                        show_screen()
                    elif k == KEY_OK:
                        break
                if options[sel] == "Hit":
                    h.append(deck.pop())
                elif options[sel] == "Double":
                    cash -= b
                    bets[h_index] = b * 2
                    h.append(deck.pop())
                    break
                else:
                    break
        # Dealer turn
        while hand_val(d_hand) < 17:
            d_hand.append(deck.pop())
        # Resolve outcomes
        total_return = 0
        for i in range(len(hands)):
            hv = hand_val(hands[i])
            dv = hand_val(d_hand)
            stake = bets[i]
            if hv > 21:
                pass
            elif dv > 21 or hv > dv:
                total_return += stake * 2
            elif hv == dv:
                total_return += stake
        cash += total_return
        # Result screen
        clear_screen()
        show_hand(30, "Dealer", d_hand)
        if len(hands) == 1:
            show_hand(60, "You", hands[0])
        else:
            show_hand(60, "Hand1", hands[0])
            show_hand(80, "Hand2", hands[1])
        net = total_return - sum(bets)
        if net > 0:
            draw_string(10, 120, "WIN +$" + str(net), (0,0,0), "large")
        elif net < 0:
            draw_string(10, 120, "LOSE $" + str(-net), (0,0,0), "large")
        else:
            draw_string(10, 120, "PUSH", (0,0,0), "large")

        show_screen()
        wait_key()
    # Out of money
    clear_screen()
    draw_string(10, 100, "Out of money!", (0,0,0), "large")
    show_screen()
    wait_key()
# Start
play()