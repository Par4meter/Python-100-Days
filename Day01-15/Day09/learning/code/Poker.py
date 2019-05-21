import random


class Card:
    __slots__ = ['_suit', '_face']

    def __init__(self, suit, face):
        """
        :param suit: 花色
        :param face: 牌面
        """
        self._suit = suit
        self._face = face

    @property
    def suit(self):
        return self._suit

    @property
    def face(self):
        return self._face

    def __str__(self):

        face_str = str(self._face)

        if self.face == 1:
            face_str = 'A'
        elif self._face == 11:
            face_str = 'J'
        elif self._face == 12:
            face_str = 'Q'
        elif self._face == 13:
            face_str = 'K'
        return '%s%s' % (self._suit, face_str)


class Poker:

    def __init__(self):
        self._cards = [Card(suit, face)
                       for suit in '♠♥♣♦'
                       for face in range(1, 14)]
        self._current = 0

    def has_next(self):
        return self._current < len(self._cards)

    def next(self):
        card = self._cards[self._current]
        self._current += 1
        return card

    def shuffle(self):
        self._current = 0
        random.shuffle(self._cards)

    @property
    def cards(self):
        return self._cards


class Player:
    __slots__ = ['_name', '_hands']

    def __init__(self, name):
        self._name = name
        self._hands = []

    def draw_a_card(self, card):
        """抓一张牌"""
        self._hands.append(card)

    @property
    def name(self):
        return self._name

    @property
    def hands(self):
        return self._hands

    @hands.setter
    def hands(self, hands):
        self._hands = hands

    def __str__(self):
        hands_str = [str(card) for card in self._hands]

        return '玩家：%s' % self._name \
               + '手牌：%s\n' % hands_str


def main():
    poker = Poker()
    poker.shuffle()
    p1 = Player('东邪')
    p2 = Player('西毒')
    p3 = Player('南帝')
    p4 = Player('北丐')

    while poker.has_next():
        p1.draw_a_card(poker.next())
        p2.draw_a_card(poker.next())
        p3.draw_a_card(poker.next())
        p4.draw_a_card(poker.next())

    print(p1)
    print(p2)
    print(p3)
    print(p4)


if __name__ == '__main__':
    main()
