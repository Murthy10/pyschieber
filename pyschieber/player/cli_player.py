from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf


class CliPlayer(BasePlayer):
    def choose_trumpf(self):
        trumpfs = list(Trumpf)
        self._print_cards()
        print('Trumpf:')
        for i, trumpf in enumerate(trumpfs):
            print('{0} : {1}'.format(i, trumpf))
        while True:
            try:
                trumpf_index = int(
                    input("Please chose the trumpf by the number from 0 to {0}: ".format(len(trumpfs) - 1)))
                if trumpf_index in range(0, len(trumpfs)):
                    return trumpfs[trumpf_index]
                else:
                    print("Sorry, no valid trumpf number.")
                    continue
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

    def choose_card(self):
        self._print_cards()
        while not self.card_allowed:
            card = self._handle_input()
            yield card
            print("Card not allowed!")

    def _handle_input(self):
        while True:
            try:
                card_index = int(
                    input("Please chose the card by the number from 0 to {0}: ".format(len(self.cards) - 1)))
                if card_index in range(0, len(self.cards)):
                    return self.cards[card_index]
                else:
                    print("Sorry, no valid trumpf number")
                    continue
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

    def _print_cards(self):
        print('Cards')
        for i, card in enumerate(self.cards):
            print('{0} : {1}'.format(i, card))
