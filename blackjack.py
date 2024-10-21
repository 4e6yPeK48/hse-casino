from pprint import pprint

from flask import Flask, render_template, jsonify, request
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
    def value(card: Card, ace=None) -> int:
        if card.name in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            return int(card.name)
        elif card.name in ['Валет', 'Дама', 'Король']:
            return 10
        else:
            return 11


class BlackJackGame:
    def __init__(self):
        self.deck = Deck()
        self.dealer_cards = []
        self.player_hands = [[]]
        self.dealer_score = 0
        self.player_scores = [0]
        self.double_check = False
        self.game_over = False
        self.first_hand_bust = False
        self.second_hand_bust = False
        self.first_hand_stand = False
        self.second_hand_stand = False
        self.move_count = 0

    def start(self):
        pprint(f'Количество колод: {len(list(sorted(self.deck))) / 52}')
        self.move_count = 0
        self.deck = Deck()
        self.dealer_cards = [next(self.deck), next(self.deck)]
        self.player_hands = [[next(self.deck), next(self.deck)]]
        self.dealer_score = sum([CardManager.value(card) for card in self.dealer_cards])
        self.player_scores = [CardManager.value(card) for card in self.player_hands[0]]
        self.player_scores = [sum(self.player_scores)]
        self.game_over = False
        self.check_game_over()

    def hit(self, hand_index=0):
        self.move_count += 1
        if not self.game_over:
            tmp = next(self.deck)
            self.player_hands[hand_index].append(tmp)
            if tmp.name == 'Туз':
                if self.player_scores[hand_index] + 11 > 21:
                    self.player_scores[hand_index] += 1
                else:
                    self.player_scores[hand_index] += 11
            else:
                self.player_scores[hand_index] += CardManager.value(tmp)
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
                if self.dealer_score + 11 > 21:
                    self.dealer_score += 1
                else:
                    self.dealer_score += 11
            else:
                self.dealer_score += CardManager.value(tmp)
        self.game_over = True

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
            if self.first_hand_bust and self.second_hand_stand:
                self.game_over = True
            if self.second_hand_bust and self.first_hand_stand:
                self.game_over = True
            if self.first_hand_stand and self.second_hand_stand:
                self.game_over = True
        elif self.player_scores[0] > 21:
            self.game_over = True

    def get_result(self):
        results = []
        for score in self.player_scores:
            if score > 21:
                results.append('Дилер')
            elif self.dealer_score > 21:
                results.append('Игрок')
            elif score == self.dealer_score:
                results.append('Ничья')
            elif score == 21:
                results.append('Блэкджэк')
            elif self.dealer_score == 21:
                results.append('Блэкджэк у дилера')
            elif score > self.dealer_score:
                results.append('Игрок')
            else:
                results.append('Дилер')
        return results

    def can_split(self):
        return (not self.game_over and len(self.player_hands) == 1 and
                CardManager.value(self.player_hands[0][0]) == CardManager.value(self.player_hands[0][1]))

    def to_dict(self):
        return {
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
            'result': self.get_result() if self.game_over else None,
            'can_split': self.can_split(),
            'move_count': self.move_count
        }
