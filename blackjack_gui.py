import tkinter as tk
from tkinter import font as tkfont
import random

class BlackjackGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a472a")
        self.root.resizable(False, False)

        # Game state
        self.balance = 1_000_000
        self.bet = 0
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.card_font = tkfont.Font(family="Courier", size=24, weight="bold")
        self.info_font = tkfont.Font(family="Helvetica", size=16)
        self.button_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.small_font = tkfont.Font(family="Helvetica", size=12)

        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(
            self.root, text="BLACKJACK",
            font=self.title_font, fg="#ffd700", bg="#1a472a"
        )
        self.title_label.pack(pady=10)

        # Balance & Multiplier info
        self.info_frame = tk.Frame(self.root, bg="#1a472a")
        self.info_frame.pack(pady=5)

        self.balance_label = tk.Label(
            self.info_frame, text=f"Balance: $1,000,000",
            font=self.info_font, fg="white", bg="#1a472a"
        )
        self.balance_label.pack(side=tk.LEFT, padx=20)

        self.multiplier_label = tk.Label(
            self.info_frame, text="",
            font=self.info_font, fg="#00ff00", bg="#1a472a"
        )
        self.multiplier_label.pack(side=tk.LEFT, padx=20)

        # Dealer area
        self.dealer_frame = tk.Frame(self.root, bg="#1a472a")
        self.dealer_frame.pack(pady=10)

        self.dealer_title = tk.Label(
            self.dealer_frame, text="Dealer",
            font=self.small_font, fg="#cccccc", bg="#1a472a"
        )
        self.dealer_title.pack()

        self.dealer_cards_frame = tk.Frame(self.dealer_frame, bg="#1a472a")
        self.dealer_cards_frame.pack(pady=5)

        self.dealer_value_label = tk.Label(
            self.dealer_frame, text="",
            font=self.small_font, fg="white", bg="#1a472a"
        )
        self.dealer_value_label.pack()

        # Divider
        tk.Frame(self.root, height=2, bg="#ffd700").pack(fill=tk.X, padx=100, pady=10)

        # Player area
        self.player_frame = tk.Frame(self.root, bg="#1a472a")
        self.player_frame.pack(pady=10)

        self.player_title = tk.Label(
            self.player_frame, text="Player",
            font=self.small_font, fg="#cccccc", bg="#1a472a"
        )
        self.player_title.pack()

        self.player_cards_frame = tk.Frame(self.player_frame, bg="#1a472a")
        self.player_cards_frame.pack(pady=5)

        self.player_value_label = tk.Label(
            self.player_frame, text="",
            font=self.small_font, fg="white", bg="#1a472a"
        )
        self.player_value_label.pack()

        # Bet input area
        self.bet_frame = tk.Frame(self.root, bg="#1a472a")
        self.bet_frame.pack(pady=20)

        self.bet_label = tk.Label(
            self.bet_frame, text="Enter Bet:",
            font=self.info_font, fg="white", bg="#1a472a"
        )
        self.bet_label.pack(side=tk.LEFT, padx=5)

        self.bet_entry = tk.Entry(
            self.bet_frame, font=self.info_font, width=12,
            justify="center", bg="#2d5a3d", fg="white",
            insertbackground="white", relief=tk.FLAT
        )
        self.bet_entry.pack(side=tk.LEFT, padx=5)
        self.bet_entry.insert(0, "100")

        # Buttons
        self.button_frame = tk.Frame(self.root, bg="#1a472a")
        self.button_frame.pack(pady=10)

        self.deal_button = tk.Button(
            self.button_frame, text="DEAL", font=self.button_font,
            width=10, bg="#ffd700", fg="#1a472a", relief=tk.FLAT,
            command=self.deal_cards
        )
        self.deal_button.pack(side=tk.LEFT, padx=10)

        self.hit_button = tk.Button(
            self.button_frame, text="HIT", font=self.button_font,
            width=10, bg="#4CAF50", fg="white", relief=tk.FLAT,
            command=self.hit, state=tk.DISABLED
        )
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(
            self.button_frame, text="STAND", font=self.button_font,
            width=10, bg="#f44336", fg="white", relief=tk.FLAT,
            command=self.stand, state=tk.DISABLED
        )
        self.stand_button.pack(side=tk.LEFT, padx=10)

        # Result label
        self.result_label = tk.Label(
            self.root, text="Place your bet and click DEAL",
            font=self.info_font, fg="#ffd700", bg="#1a472a"
        )
        self.result_label.pack(pady=10)

        # New game button
        self.new_game_button = tk.Button(
            self.root, text="NEW GAME", font=self.button_font,
            width=15, bg="#2196F3", fg="white", relief=tk.FLAT,
            command=self.reset_game
        )
        self.new_game_button.pack(pady=10)

    def create_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def card_value(self, card):
        rank = card[0]
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        return int(rank)

    def hand_value(self, hand):
        value = sum(self.card_value(c) for c in hand)
        aces = sum(1 for c in hand if c[0] == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def create_card_label(self, card, hidden=False):
        if hidden:
            text = "[? ?]"
            color = "#888888"
        else:
            text = f"{card[0]}{card[1]}"
            color = "#ffd700" if card[1] in ['♥', '♦'] else "white"

        label = tk.Label(
            self.dealer_cards_frame if card in self.dealer_hand else self.player_cards_frame,
            text=text, font=self.card_font, fg=color, bg="#2d5a3d",
            width=5, relief=tk.RAISED, bd=2, padx=10, pady=5
        )
        return label

    def display_cards(self):
        # Clear cards
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()

        # Show dealer cards (first hidden if game in progress)
        hidden = len(self.dealer_hand) > 1 and self.game_in_progress
        for i, card in enumerate(self.dealer_hand):
            if i == 0 and hidden:
                label = tk.Label(
                    self.dealer_cards_frame,
                    text="[? ?]", font=self.card_font, fg="#888888",
                    bg="#2d5a3d", width=5, relief=tk.RAISED, bd=2, padx=10, pady=5
                )
            else:
                color = "#ffd700" if card[1] in ['♥', '♦'] else "white"
                label = tk.Label(
                    self.dealer_cards_frame,
                    text=f"{card[0]}{card[1]}", font=self.card_font, fg=color,
                    bg="#2d5a3d", width=5, relief=tk.RAISED, bd=2, padx=10, pady=5
                )
            label.pack(side=tk.LEFT, padx=5)

        # Show player cards
        for card in self.player_hand:
            color = "#ffd700" if card[1] in ['♥', '♦'] else "white"
            label = tk.Label(
                self.player_cards_frame,
                text=f"{card[0]}{card[1]}", font=self.card_font, fg=color,
                bg="#2d5a3d", width=5, relief=tk.RAISED, bd=2, padx=10, pady=5
            )
            label.pack(side=tk.LEFT, padx=5)

        # Update values
        dealer_val = self.hand_value(self.dealer_hand[1:]) if hidden else self.hand_value(self.dealer_hand)
        self.dealer_value_label.config(
            text=f"Value: {dealer_val if not hidden else '?'}" + (" + ?)" if hidden else ")")
        )
        self.player_value_label.config(text=f"Value: {self.hand_value(self.player_hand)}")

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.balance:,}")

    def format_bet(self, *args):
        pass  # Keep simple - just strip commas when parsing

    def deal_cards(self):
        try:
            bet_text = self.bet_entry.get().replace(',', '')
            self.bet = int(bet_text)
        except ValueError:
            self.bet = 100

        if self.bet <= 0:
            self.result_label.config(text="Invalid bet! Enter a positive number.", fg="#f44336")
            return

        if self.bet > self.balance:
            self.result_label.config(text="Not enough balance!", fg="#f44336")
            return

        # Reset for new round
        self.deck = self.create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.game_in_progress = True
        self.multiplier_label.config(text="")

        # Update UI
        self.bet_entry.config(state=tk.DISABLED)
        self.deal_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.result_label.config(text="", fg="#ffd700")
        self.display_cards()

        # Check for blackjack
        if self.hand_value(self.player_hand) == 21:
            self.end_game()

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.display_cards()

        if self.hand_value(self.player_hand) > 21:
            self.end_game()
        elif self.hand_value(self.player_hand) == 21:
            self.stand()

    def stand(self):
        self.game_in_progress = False

        # Dealer draws
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        self.end_game()

    def end_game(self):
        self.game_in_progress = False
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_entry.config(state=tk.NORMAL)
        self.deal_button.config(state=tk.NORMAL)

        self.display_cards()

        player_val = self.hand_value(self.player_hand)
        dealer_val = self.hand_value(self.dealer_hand)

        bonus = 50
        result_text = ""
        result_color = "#ffd700"

        if player_val > 21:
            result_text = f"BUST! You lose ${self.bet:,}"
            self.balance -= self.bet
            self.multiplier_label.config(text="x-1.00", fg="#f44336")
            result_color = "#f44336"
        elif dealer_val > 21:
            winnings = self.bet + bonus
            result_text = f"Dealer busts! You win ${winnings:,} (+${bonus} bonus)"
            self.balance += winnings
            self.multiplier_label.config(text=f"x{(winnings/self.bet):.2f}", fg="#00ff00")
        elif player_val > dealer_val:
            winnings = self.bet + bonus
            result_text = f"You win ${winnings:,} (+${bonus} bonus)"
            self.balance += winnings
            self.multiplier_label.config(text=f"x{(winnings/self.bet):.2f}", fg="#00ff00")
        elif player_val < dealer_val:
            result_text = f"Dealer wins. You lose ${self.bet:,}"
            self.balance -= self.bet
            self.multiplier_label.config(text="x-1.00", fg="#f44336")
            result_color = "#f44336"
        else:
            result_text = "Push (tie)!"
            self.multiplier_label.config(text="x0.00", fg="#888888")

        self.result_label.config(text=result_text, fg=result_color)
        self.update_balance()

        if self.balance <= 0:
            self.result_label.config(text="Game Over! No more balance.", fg="#f44336")
            self.deal_button.config(state=tk.DISABLED)
        else:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(self.balance))

    def reset_game(self):
        self.player_hand = []
        self.dealer_hand = []
        self.bet = 0
        self.game_in_progress = False

        self.bet_entry.config(state=tk.NORMAL)
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.insert(0, str(self.balance))
        self.deal_button.config(state=tk.NORMAL)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()

        self.dealer_value_label.config(text="")
        self.player_value_label.config(text="")
        self.result_label.config(text="Place your bet and click DEAL", fg="#ffd700")
        self.multiplier_label.config(text="")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = BlackjackGUI()
    game.run()
