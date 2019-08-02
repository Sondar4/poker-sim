"""Description of the module:
"""
from random import shuffle
from pdb import set_trace

class Card:
    """Represents a card of a standard poker deck.
    The rank is an integer from 2 to 14. It starts at 2 to be more intuitive.
    The suit is an integer from 0 to 3 as follows:
        0 -> Clubs
        1 -> Hearts
        2 -> Spades
        3 -> Diamonds
    """
    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, None, '2', '3', '4', '5', '6', '7',
                    '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit=0, rank=2):
        if type(rank) != int or type(suit) != int:
            print('Card atributes must be int type')
            raise TypeError
        else:
            self.suit = suit
            self.rank = rank

    def __str__(self):
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __lt__(self, other):
        return self.rank < other.rank


class Deck:
    """Represents a poker Deck.
    A list of cards can be given to generate the Deck.
    The Deck is a list of Cards.
    """
    def __init__(self, used_cards=[]):
        used_pairs = [(card.suit, card.rank) for card in used_cards]
        self.cards = [Card(x, y+2) for x in range(4) for y in range(13) if (x,y) not in used_pairs]
    
    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def shuffle(self):
        shuffle(self.cards)

    def pop_card(self):
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)

    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):
    """Represents a hand of playing cards.
    """
    def __init__(self, label=''):
        self.cards = []
        self.label = label

    def all_cards(self, table):
        """Returns a sorted tuple of the cards of the hand and the table.
        The tuple is sorted by rank and if ranks are equal by suit.
        """
        return tuple( sorted(self.cards + table.cards, key = lambda card: (card.rank, card.suit)) )

    def best_hand(self, table):
        """Returns a tuple with the best hand that can be built with the cards
        in the hand and the table.

        output: int, str, tuple
        """
        cards = self.all_cards(table)
        test = is_straight_flush(cards)
        if test[0]:
            return 8, 'straight flush', test[1]

        test = is_four(cards)
        if test[0]:
            return 7, 'four of a kind', test[1]
        
        test = is_full_house(cards)
        if test[0]:
            return 6, 'full house', test[1]

        test = is_flush(cards)
        if test[0]:
            return 5, 'flush', test[1]

        test = is_straight(cards)
        if test[0]:
            return 4, 'straight', test[1]

        test = is_three(cards)
        if test[0]:
            return 3, 'three of a kind', test[1]

        test = is_two_pair(cards)
        if test[0]:
            return 2, 'two pair', test[1]

        test = is_pair(cards)
        if test[0]:
            return 1, 'pair', test[1]

        return 0, 'highest card', is_highest_card(cards)[1]


def is_straight_flush(cards):
    """Returns a boolean and a tuple with the cards that make the straight flush.
    """
    straight_flush = False
    counter = 0
    for i in range( len(cards)-1 ):
        if cards[i].rank+1 == cards[i+1].rank and cards[i].suit == cards[i+1].suit:
            counter += 1
        else:
            counter = 0
        if counter > 3:
            straight_flush = True
            j = i+1
    if straight_flush:
        return True, tuple((cards[j-i] for i in range(5))) #Returns the highest card first
    return False, 0


def is_four(cards):
    """Returns a boolean and a tuple with the cards that make the four of a kind.
    """
    four = False
    ranks = tuple( (card.rank for card in cards) )
    counter = 0
    for i in range( len(ranks)-1 ):
        if ranks[i] == ranks[i+1]:
            counter += 1
        else:
            counter = 0
        if counter > 2:
            four = True
            j = i+1
    if four:
        four1 = tuple((cards[j-i] for i in range(4)))
        unused_cards = [card for card in cards if card not in four1]
        return True, four1 + (unused_cards[-1],)
    return False, 0


def is_full_house(cards):
    """Returns a boolean and a tuple with the cards that make the full house.
    """
    pair = False
    three = False
    ranks = tuple( (card.rank for card in cards) )
    i = 0
    while i < (len(cards)-1):
        if ranks[i] == ranks[i+1]:
            if i < (len(cards)-2):
                if ranks[i+1] == ranks[i+2]:
                    three = True
                    j = i+2
                    i += 2
            else:
                pair = True
                k = i+1
                i += 1
        i += 1
    if pair and three:
        pair1 = tuple((cards[k-i] for i in range(2)))
        three1 = tuple((cards[j-i] for i in range(3)))
        return True, pair1 + three1
    return False, 0


def is_flush(cards):
    """Returns a boolean and a tuple with the cards that make the flush.
    """
    flush = False
    suits_counter = [0,0,0,0]   # 0: Clubs, 1: Hearts, 2: Spades, 3: Diamonds
    for card in cards:
        suits_counter[card.suit] += 1
    for i in range(4):
        if suits_counter[i] > 4:
            flush = True
            flush_suit = i
    #If there's a flush let's get the best hand
    if flush == True:
        suit_ordered_cards = tuple( sorted(cards, key = lambda card: (card.suit, card.rank)) )
        for i in range(len(cards)):
            if suit_ordered_cards[-i-1].suit == flush_suit:
                return True, tuple( ( suit_ordered_cards[-i-1-j] for j in range(5) ) )
    return False, 0


def is_straight(cards):
    """Returns a boolean and a tuple with the cards that make the straight.
    """
    straight = False
    counter = 0
    for i in range( len(cards)-1 ):
        if cards[i].rank+1 == cards[i+1].rank:
            counter += 1
        else:
            counter = 0
        if counter > 3:
            straight = True
            j = i+1
    if straight:
        return True, tuple((cards[j-i] for i in range(5)))
    return False, 0


def is_three(cards):
    """Returns a boolean and a tuple with the cards that make the three of a kind.
    """
    three = False
    ranks = tuple( (card.rank for card in cards) )
    counter = 0
    for i in range( len(ranks)-1 ):
        if ranks[i] == ranks[i+1]:
            counter += 1
        else:
            counter = 0
        if counter > 1:
            three = True
            j = i+1
    if three:
        three1 = tuple((cards[j-i] for i in range(3)))
        unused_cards = [card for card in cards if card not in three1]
        return True, three1 + (unused_cards[-1], unused_cards[-2])
    return False, 0


def is_two_pair(cards):
    """Returns a boolean and a tuple with the cards that make the two pairs.
    """
    pair_counter = 0
    ranks = tuple( (card.rank for card in cards) )
    j = list()
    i = 0
    while i < (len(ranks)-1):
        if ranks[i] == ranks[i+1]:
            pair_counter += 1
            j.append(i+1)
            i += 1 #La pareja ya está cogida
        i += 1
    if pair_counter > 1:
        pair1 = tuple((cards[j[-1]-i] for i in range(2)))
        pair2 = tuple((cards[j[-2]-i] for i in range(2)))
        unused_cards = [card for card in cards if card not in pair1 + pair2]
        return True, pair1 + pair2 + (unused_cards[-1],)
    return False, 0


def is_pair(cards):
    """Returns a boolean and a tuple with the cards that make the pair.
    """
    pair = False
    ranks = tuple( (card.rank for card in cards) )
    i = 0
    while i < (len(ranks)-1):
        if ranks[i] == ranks[i+1]:
            pair = True
            j = i+1
            i += 1 #La pareja ya está cogida
        i += 1
    if pair:
        pair1 = tuple((cards[j-i] for i in range(2)))
        unused_cards = [card for card in cards if card not in pair1]
        return True, pair1 + (unused_cards[-1], unused_cards[-2], unused_cards[-3])
    return False, 0


def is_highest_card(cards):
    """Returns the hand with the highest cards.
    """
    return True, tuple((cards[-i-1] for i in range(5)))


def rate(result, name, cards):
    """Gives a score to a 5 cards hand. The score is a vector of 6 dimensions.
    The input of the function must be the output of the best_hand method.
    
    The function should be called something like this: score = rate(*player.best_hand(table))
    """
    score = [result, 0, 0, 0, 0, 0]
    #The other 5 dimensions depend on the kind of hand.
    #Straight flush
    if score[0] == 8:
        score[1] = cards[0].rank
    #Four of a kind
    elif score[0] == 7:
        score[1] = cards[0].rank
        score[2] = cards[-1].rank
    #Full house
    elif score[0] == 6:
        score[1] = cards[-1].rank
        score[2] = cards[0].rank
    #Flush
    elif score[0] == 5:
        for i in range(5):
            score[i+1] = cards[i].rank
    #Straight
    elif score[0] == 4:
        score[1] = cards[0].rank
    #Three of a kind
    elif score[0] == 3:
        score[1] = cards[0].rank
        score[2] = cards[-2].rank
        score[3] = cards[-1].rank
    #Two pair
    elif score[0] == 2:
        score[1] = max(cards[0].rank, cards[2].rank)
        score[2] = min(cards[0].rank, cards[2].rank)
        score[3] = cards[-1].rank
    #Pair
    elif score[0] == 1:
        score[1] = cards[0].rank
        for i in range(3):
            score[i+2] = cards[i+2].rank
    #Highest card
    else:
        for i in range(5):
            score[i+1] = cards[i].rank
    
    return tuple(score)


if __name__ == '__main__':
    set_trace()