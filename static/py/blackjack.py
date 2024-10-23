from pprint import pprint
from typing import List

from itertools import product
from random import shuffle


class Card:
    def __init__(self, suit, name):
        match suit:
            case 'Т':
                self.suit = '♣ трефы'
            case 'Б':
                self.suit = '♦ бубны'
            case 'Ч':
                self.suit = '♥ черви'
            case 'П':
                self.suit = '♠ пики'
            case _:
                self.suit = suit
        match name:
            case '2':
                self.name = '2'
            case '3':
                self.name = '3'
            case '4':
                self.name = '4'
            case '5':
                self.name = '5'
            case '6':
                self.name = '6'
            case '7':
                self.name = '7'
            case '8':
                self.name = '8'
            case '9':
                self.name = '9'
            case 'В':
                self.name = 'Валет'
            case 'Д':
                self.name = 'Дама'
            case 'К':
                self.name = 'Король'
            case 'Т':
                self.name = 'Туз'
            case _:
                self.name = name

    def __str__(self):
        return f'{self.name} {self.suit}'

    def __repr__(self):
        return f'{self.name} {self.suit}'

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return CardManager.value(self) < CardManager.value(other)


class Deck:
    def __init__(self, decks_count=8):
        self.cards = [Card(suit, name) for suit, name in
                      product(['Т', 'Б', 'Ч', 'П'],
                              ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т'])] * decks_count
        shuffle(self.cards)

    def __iter__(self):
        return self

    def __next__(self):
        if self.cards:
            return self.cards.pop()
        else:
            raise StopIteration

    def __str__(self):
        return str([str(card) for card in self.cards])

    def __repr__(self):
        return str([str(card) for card in self.cards])


class CardManager:
    @staticmethod
    def value(card: Card) -> int:
        if card.name in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            return int(card.name)
        elif card.name in ['Валет', 'Дама', 'Король']:
            return 10
        else:
            return 11

    @staticmethod
    def from_str(card_str: str) -> Card:
        name, suit = card_str.split(' ', 1)
        return Card(suit, name)


class BlackJackGame:
    def __init__(self):
        self.bet = 0
        self.deck = Deck()
        self.dealer_cards: List[Card] = []
        self.player_hands: List[List[Card]] = [[]]
        self.dealer_score = 0
        self.dealer_aces_count = 0
        self.player_scores = [0]
        self.player_aces_count = [0, 0]
        self.double_check = False
        self.game_over = False
        self.first_hand_bust = False
        self.second_hand_bust = False
        self.first_hand_stand = False
        self.second_hand_stand = False
        self.move_count = 0

    def start(self, decks_count=8, bet=0):
        self.bet = bet
        self.move_count = 0
        self.deck = Deck(decks_count)
        self.dealer_cards = [next(self.deck), next(self.deck)]
        self.player_hands = [[next(self.deck), next(self.deck)]]
        self.dealer_score = sum([CardManager.value(card) for card in self.dealer_cards])
        self.dealer_aces_count = 0
        self.player_scores = [CardManager.value(card) for card in self.player_hands[0]]
        self.player_scores = [sum(self.player_scores)]
        self.player_aces_count = [sum(1 for card in self.player_hands[0] if card.name == 'Туз'), 0]
        self.adjust_for_aces(0)
        self.adjust_dealer_for_aces()
        self.game_over = False
        self.check_game_over()

    def hit(self, hand_index=0):
        self.move_count += 1
        if not self.game_over:
            if hand_index >= len(self.player_hands):
                raise IndexError(f"Invalid hand_index: {hand_index}")
            tmp = next(self.deck)
            self.player_hands[hand_index].append(tmp)
            self.player_scores[hand_index] += CardManager.value(tmp)
            if tmp.name == 'Туз':
                self.player_aces_count[hand_index] += 1
            self.adjust_for_aces(hand_index)
            if self.player_scores[hand_index] > 21:
                if hand_index == 0 and len(self.player_hands) > 1:
                    self.first_hand_bust = True
                elif hand_index == 1 and len(self.player_hands) > 1:
                    self.second_hand_bust = True
            self.check_game_over()

    def stand(self, hand_index=0):
        self.move_count += 1
        if not self.game_over:
            if hand_index == 0:
                self.first_hand_stand = True
            if hand_index == 1:
                self.second_hand_stand = True

            if len(self.player_hands) > 1:
                if self.first_hand_stand and self.second_hand_stand:
                    self.dealer_turn()
                else:
                    self.check_game_over()
            else:
                self.dealer_turn()

    def dealer_turn(self):
        while self.dealer_score < 17:
            tmp = next(self.deck)
            self.dealer_cards.append(tmp)
            if tmp.name == 'Туз':
                self.dealer_aces_count += 1
            self.dealer_score += CardManager.value(tmp)
            self.adjust_dealer_for_aces()
        self.game_over = True

    def adjust_for_aces(self, hand_index):
        while self.player_scores[hand_index] > 21 and self.player_aces_count[hand_index] > 0:
            self.player_scores[hand_index] -= 10
            self.player_aces_count[hand_index] -= 1

    def adjust_dealer_for_aces(self):
        while self.dealer_score > 21 and self.dealer_aces_count > 0:
            self.dealer_score -= 10
            self.dealer_aces_count -= 1

    def double(self, hand_index=0):
        self.move_count += 1
        if not self.game_over:
            self.hit(hand_index)
            self.double_check = True
            self.dealer_turn()

    def split(self):
        self.move_count += 1
        if not self.game_over and len(self.player_hands) == 1 and CardManager.value(
                self.player_hands[0][0]) == CardManager.value(self.player_hands[0][1]):
            self.player_hands = [[self.player_hands[0][0]], [self.player_hands[0][1]]]
            self.player_scores = [CardManager.value(self.player_hands[0][0]),
                                  CardManager.value(self.player_hands[1][0])]
            self.hit(0)
            self.hit(1)

    def check_game_over(self):
        if all(score == 21 for score in self.player_scores):
            self.game_over = True
        if len(self.player_hands) > 1:
            if self.first_hand_bust and self.second_hand_bust:
                self.game_over = True

            if self.first_hand_stand and self.second_hand_stand:
                self.dealer_turn()

            if self.first_hand_bust and self.second_hand_stand:
                self.dealer_turn()

            if self.second_hand_bust and self.first_hand_stand:
                self.dealer_turn()

            if self.player_scores[0] == 21 and self.second_hand_bust:
                self.game_over = True

            if self.player_scores[1] == 21 and self.first_hand_bust:
                self.game_over = True

            if self.player_scores[0] == 21 and self.second_hand_stand:
                self.dealer_turn()

            if self.player_scores[1] == 21 and self.first_hand_stand:
                self.dealer_turn()

            if self.player_scores[0] == 21 and self.player_scores[1] == 21:
                self.game_over = True

        elif self.player_scores[0] > 21:
            self.game_over = True

    def get_result(self):
        results = []
        win = 0
        for score in self.player_scores:
            if score > 21:
                results.append('Дилер')
                win += 0
            elif self.dealer_score > 21:
                results.append('Игрок')
                win += self.bet * 2
            elif score == self.dealer_score:
                results.append('Ничья')
                win += self.bet
            elif score == 21:
                results.append('Блэкджэк у игрока')
                win += self.bet * 2.5
            elif self.dealer_score == 21:
                results.append('Блэкджэк у дилера')
                win += 0
            elif score > self.dealer_score:
                results.append('Игрок')
                win += self.bet * 2
            else:
                results.append('Дилер')
                win += 0
        return results, win

    def can_split(self):
        return (not self.game_over and len(self.player_hands) == 1 and
                CardManager.value(self.player_hands[0][0]) == CardManager.value(self.player_hands[0][1]))

    def to_dict(self):
        return {
            'bet': self.bet,
            'dealer_cards': [str(card) for card in self.dealer_cards],
            'player_hands': [[str(card) for card in hand] for hand in self.player_hands],
            'dealer_score': self.dealer_score,
            'player_scores': self.player_scores,
            'double_check': self.double_check,
            'game_over': self.game_over,
            'first_hand_bust': self.first_hand_bust,
            'second_hand_bust': self.second_hand_bust,
            'first_hand_stand': self.first_hand_stand,
            'second_hand_stand': self.second_hand_stand,
            'result': self.get_result()[0] if self.game_over else None,
            'win': self.get_result()[1] if self.game_over else None,
            'can_split': self.can_split(),
            'move_count': self.move_count
        }

    @classmethod
    def from_dict(cls, data):
        game = cls()
        game.bet = data['bet']
        game.dealer_cards = [CardManager.from_str(card) for card in data['dealer_cards']]
        game.player_hands = [[CardManager.from_str(card) for card in hand] for hand in data['player_hands']]
        game.dealer_score = data['dealer_score']
        game.player_scores = data['player_scores']
        game.double_check = data['double_check']
        game.game_over = data['game_over']
        game.first_hand_bust = data['first_hand_bust']
        game.second_hand_bust = data['second_hand_bust']
        game.first_hand_stand = data['first_hand_stand']
        game.second_hand_stand = data['second_hand_stand']
        game.move_count = data['move_count']
        return game
