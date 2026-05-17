import random

def create_deck():
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for rank in ranks for suit in suits]

def card_value(card):
    rank = card[0]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def hand_value(hand):
    value = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hand(hand, hide_first=False):
    if hide_first:
        return [hand[0], ('?', '?')] if len(hand) > 1 else hand
    return hand

def print_hand(hand, hide_first=False):
    shown = display_hand(hand, hide_first)
    cards = ' '.join(f"{r}{s}" for r, s in shown)
    print(f"  {cards}", end='')
    if hide_first:
        print(f"  ({card_value(hand[0])} + ?)")
    else:
        print(f"  ({hand_value(hand)})")

def play_blackjack(balance):
    print(f"\n--- Blackjack --- | Balance: ${balance:,}")

    try:
        bet = int(input("Enter your bet: "))
    except ValueError:
        bet = 100

    if bet <= 0:
        print("Invalid bet. Using $100.")
        bet = 100

    if balance < bet:
        print("Not enough balance to play!")
        return balance, False

    deck = create_deck()
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Player turn
    while True:
        print(f"\nYour hand:", end='')
        print_hand(player_hand)

        if hand_value(player_hand) == 21:
            print("  Blackjack!")
            break
        if hand_value(player_hand) > 21:
            print("  Bust! You lose.")
            balance -= bet
            multiplier = -1.0
            print(f"  Lost: ${bet:,} (x{multiplier:.2f} multiplier)")
            print(f"  Balance: ${balance:,}")
            return balance, True

        action = input("  Hit or Stand? (h/s): ").lower()
        if action == 's':
            break
        player_hand.append(deck.pop())

    # Dealer turn
    print(f"\nDealer hand:", end='')
    print_hand(dealer_hand)

    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print(f"  Dealer draws... ", end='')
        print_hand(dealer_hand)

    # Compare
    player_val = hand_value(player_hand)
    dealer_val = hand_value(dealer_hand)

    print(f"\nFinal: You={player_val}, Dealer={dealer_val}")

    bonus = 50  # Bonus for winning

    if dealer_val > 21:
        print("Dealer busts! You win!")
        winnings = bet + bonus
        balance += winnings
        multiplier = winnings / bet
        print(f"  Won: ${winnings:,} (x{multiplier:.2f} multiplier)")
    elif player_val > dealer_val:
        print("You win!")
        winnings = bet + bonus
        balance += winnings
        multiplier = winnings / bet
        print(f"  Won: ${winnings:,} (x{multiplier:.2f} multiplier)")
    elif player_val < dealer_val:
        print("Dealer wins.")
        balance -= bet
        multiplier = -1.0
        print(f"  Lost: ${bet:,} (x{multiplier:.2f} multiplier)")
    else:
        print("Push (tie).")
        multiplier = 0.0
        print(f"  No change (x{multiplier:.2f} multiplier)")

    print(f"Balance: ${balance:,}")
    return balance, True

if __name__ == "__main__":
    balance = 1_000_000

    while True:
        balance, can_play = play_blackjack(balance)

        if not can_play or balance <= 0:
            print("\nGame Over!")
            break

        again = input("\nPlay again? (y/n): ").lower()
        if again != 'y':
            print(f"\nThanks for playing! Final balance: ${balance:,}")
            break
