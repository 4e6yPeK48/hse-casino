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

    @staticmethod
    def identify_card_by_number(number):
        suits = ['Т', 'Б', 'Ч', 'П']
        names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']
        cards = [Card(suit, name) for suit, name in product(suits, names)]
        return cards[number]


class Deck:
    """
    написать класс Deck, который хранит случайным образом перемешанную колоду кард list[Card] и возвращает каждый раз очередную, пока не кончатся
    """

    def __init__(self):
        self.cards = [Card(suit, name) for suit, name in
                      product(['Т', 'Б', 'Ч', 'П'], ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т'])]
        shuffle(self.cards)

    def __iter__(self):
        return self

    def __next__(self):
        if self.cards:
            return self.cards.pop()
        else:
            raise StopIteration


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

    def start(self):
        self.dealer_cards = [next(self.deck), next(self.deck)]
        self.player_hands = [[next(self.deck), next(self.deck)]]
        self.dealer_score = sum([CardManager.value(card) for card in self.dealer_cards])
        self.player_scores = [CardManager.value(card) for card in self.player_hands[0]]
        self.player_scores = [sum(self.player_scores)]

    def hit(self, hand_index=0):
        tmp = next(self.deck)
        self.player_hands[hand_index].append(tmp)
        print(f'Игрок взял карту "{tmp}" стоимостью: {CardManager.value(tmp)}')
        if tmp.name == 'Туз':
            if self.player_scores[hand_index] + 11 > 21:
                self.player_scores[hand_index] += 1
            else:
                self.player_scores[hand_index] += 11
        else:
            self.player_scores[hand_index] += CardManager.value(tmp)

    def stand(self):
        while self.dealer_score < 17:
            tmp = next(self.deck)
            self.dealer_cards.append(tmp)
            print(f'Дилер взял карту "{tmp}" стоимостью: {CardManager.value(tmp)}')
            if tmp.name == 'Туз':
                if self.dealer_score + 11 > 21:
                    self.dealer_score += 1
                else:
                    self.dealer_score += 11
            else:
                self.dealer_score += CardManager.value(tmp)

    def double(self, hand_index=0):
        self.hit(hand_index)

    def split(self):
        if len(self.player_hands) == 1 and self.player_hands[0][0] == self.player_hands[0][1]:
            self.player_hands = [[self.player_hands[0][0]], [self.player_hands[0][1]]]
            self.player_scores = [CardManager.value(self.player_hands[0][0]),
                                  CardManager.value(self.player_hands[1][0])]
            self.hit(0)
            self.hit(1)
        else:
            print('Нельзя разделить')

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

    def __repr__(self):
        return (f'Игрок: {self.player_hands}, суммы: {self.player_scores}\n'
                f'Дилер: {self.dealer_cards}, сумма: {self.dealer_score}')

    def __str__(self):
        return (f'Игрок: {self.player_hands}, суммы: {self.player_scores}\n'
                f'Дилер: {self.dealer_cards}, сумма: {self.dealer_score}')

    def play(self):
        self.start()
        print(self)
        while True:

            take = input('Взять или остановиться (взять/стоп/дабл/сплит): ')
            match take.lower():
                case 'взять' | 'take' | 'hit':
                    self.hit()
                    if all(score < 21 for score in self.player_scores):
                        print(self)
                        continue
                case 'взять обе' | 'take both':
                    self.hit(0)
                    self.hit(1)
                    if all(score < 21 for score in self.player_scores):
                        print(self)
                        continue
                case 'взять 1':
                    self.hit(0)
                    if self.player_scores[0]:
                        print(self)
                        continue

                case 'взять 2':
                    self.hit(1)
                    if self.player_scores[1] < 21:
                        print(self)
                        continue

                case 'стоп' | 'остановиться' | 'stop' | 'stand':
                    self.stand()
                case 'удвоить' | 'double' | 'дабл':
                    self.double()
                    self.double_check = True
                case 'сплит' | 'split':
                    self.split()
                    if all(score < 21 for score in self.player_scores):
                        print(self)
                        continue
                case _:
                    print('Неверная команда')
                    continue

            if all(score < 21 for score in self.player_scores):
                self.stand()
            elif all(score == 21 for score in self.player_scores):
                print(f'- Блэкджэк! -')
                break
            res = self.get_result()
            print(self)

            if len(res) == 2:
                match res:
                    case ['Игрок', 'Игрок']:
                        print(f'- Победил игрок в обеих -')
                        break
                    case ['Игрок', 'Дилер']:
                        print('- Победил дилер для второй-')
                        continue
                    case ['Дилер', 'Игрок']:
                        print('- Победил дилер для первой-')
                        continue
                    case ['Дилер', 'Дилер']:
                        print('- Победил дилер в обеих -')
                        break
                    case ['Ничья', 'Дилер']:
                        print('- Победил дилер для второй, ничья для первой -')
                        break
                    case ['Ничья', 'Игрок']:
                        print('- Победил игрок для второй, ничья для первой -')
                        break
                    case ['Игрок', 'Ничья']:
                        print('- Победил игрок для первой, ничья для второй -')
                        break
                    case ['Дилер', 'Ничья']:
                        print('- Победил дилер для первой, ничья для второй -')
                        break
                    case ['Ничья', 'Ничья']:
                        print('- Ничья в обеих -')
                        break

            else:
                if 'Игрок' in res:
                    print(f'- Победил игрок -\nДабл: {"да" if self.double_check else "нет"}')
                    break
                elif 'Дилер' in res:
                    print(f'- Победил дилер -\nДабл: {"да" if self.double_check else "нет"}')
                    break
                elif 'Ничья' in res:
                    print(f'- Ничья -\nДабл: {"да" if self.double_check else "нет"}')
                    break
                elif 'Блэкджэк' in res:
                    print(f'- Блэкджэк -\nДабл: {"да" if self.double_check else "нет"}')
                    break
                elif 'Блэкджэк у дилера' in res:
                    print(f'- Блэкджэк у дилера -\nДабл: {"да" if self.double_check else "нет"}')
                    break
                else:
                    continue


game = BlackJackGame()
game.play()
