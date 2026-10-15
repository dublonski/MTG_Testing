import random
from collections import Counter

class MTGDeckSimulator:
    def __init__(self, decklist_text):
        self.mainboard = self.parse_decklist(decklist_text)
        self.library = []
        self.hand = []
        self.battlefield = []
        self.graveyard = []
        self.build_library()

    def parse_decklist(self, text):
        """Parses an MTGO format decklist (e.g., '4 Lightning Bolt')"""
        deck = {}
        for line in text.strip().split('\n'):
            if not line.strip() or line.startswith('Sideboard'):
                break
            parts = line.strip().split(' ', 1)
            if len(parts) == 2 and parts[0].isdigit():
                count = int(parts[0])
                card_name = parts[1]
                deck[card_name] = count
        return deck

    def build_library(self):
        """Flattens the deck dictionary into an individual card list and shuffles."""
        self.library = []
        for card, count in self.mainboard.items():
            # For simplicity, classify lands by name keyword or external database mapping
            is_land = any(land_keyword in card.lower() for land_keyword in ['island', 'mountain', 'swamp', 'forest', 'plain', 'gate', 'bridge', 'evolving wild'])
            card_obj = {"name": card, "is_land": is_land}
            self.library.extend([card_obj] * count)
        
        # Ensure strict Pauper format minimums (60 cards)
        if len(self.library) < 60:
            print(f"Warning: Deck has {len(self.library)} cards. Standard Pauper requires at least 60.")
        random.shuffle(self.library)

    def draw_card(self, count=1):
        for _ in range(count):
            if self.library:
                self.hand.append(self.library.pop(0))

    def simulate_opening_hand(self, mulligans=0):
        """Draws an opening 7 and accounts for London Mulligan bottoming."""
        self.build_library()
        self.hand = []
        self.draw_card(7)
        
        # Basic London Mulligan heuristic: bottom N cards if mulliganed
        if mulligans > 0:
            for _ in range(mulligans):
                # Simple rule: drop the highest cost or extra lands randomly
                card_to_bottom = random.choice(self.hand)
                self.hand.remove(card_to_bottom)
                self.library.append(card_to_bottom)
            random.shuffle(self.library)

    get_metrics(self):
        """Evaluates metrics of the current hand."""
        lands = sum(1 for card in self.hand if card["is_land"])
        spells = len(self.hand) - lands
        return {"lands": lands, "spells": spells}

# --- Example Usage ---
sample_pauper_burn = """
4 Lightning Bolt
4 Chain Lightning
4 Lava Spike
4 Great Furnace
12 Mountain
4 Thermo-Alchemist
4 Keldon Marauders
4 Needle Drop
4 Galvanic Blast
4 Skewer the Critics
4 Vault Skirge
4 Experimental Synthesizer
"""

simulator = MTGDeckSimulator(sample_pauper_burn)
simulator.simulate_opening_hand(mulligans=0)
print("Opening Hand Metrics:", simulator.get_metrics())
print("Cards in Hand:", [c["name"] for c in simulator.hand])
