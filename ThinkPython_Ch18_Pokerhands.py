
# coding: utf-8

# In[ ]:

import random


class Card:
    """Represents a standard playing card.
    
    Attributes:
      suit: integer 0-3
      rank: integer 1-13
    """

    suit_names = ["Diamonds", "Clubs", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", 
              "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation."""
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __eq__(self, other):
        """Checks whether self and other have the same rank and suit.

        returns: boolean
        """
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        """Compares this card to other, first by suit, then rank.

        returns: boolean
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2


class Deck:
    """Represents a deck of cards.

    Attributes:
      cards: list of Card objects.
    """
    
    def __init__(self):
        """Initializes the Deck with 52 cards.
        """
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        """Returns a string representation of the deck.
        """
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def add_card(self, card):
        """Adds a card to the deck.

        card: Card
        """
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck or raises exception if it is not there.
        
        card: Card
        """
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())

class Hand(Deck):
    """Represents a hand of playing cards."""
    
    def __init__(self, label=''):
        self.cards = []
        self.label = label


def find_defining_class(obj, method_name):
    """Finds and returns the class object that will provide 
    the definition of method_name (as a string) if it is
    invoked on obj.

    obj: any python object
    method_name: string method name
    """
    for ty in type(obj).mro():
        if method_name in ty.__dict__:
            return ty
    return None

    
class PokerHand(Hand):
    """Represents a poker hand."""

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False
    
    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.
        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
        return self.suits
    
    def ranks_hist(self):
        """histogram of card ranks"""
        self.ranks_hist = {}
        for card in self.cards:
            self.ranks_hist[card.rank] = self.ranks_hist.get(card.rank, 0) + 1
        return self.ranks_hist
    
    def has_pair(self):
        """If hand has a pair (two cards with the same rank)"""
        self.ranks_hist()
        for i in self.ranks_hist:
            if self.ranks_hist[i] == 2:
                return 'This hand has a pair.'
        return False
    
    def has_two_pair(self):
        """If hand has two pairs."""
        vals = self.ranks_hist.values()
        count = 0
        for i in vals:
            if i >= 2:
                count += 1
        if count > 1:
            return 'There are two pairs in this hand.'
        return False
    
    def has_three_of_a_kind(self):
        """If hand has three cards of the same rank."""
        vals = self.ranks_hist.values()
        for i in vals:
            if i >2:
                return 'There are three of a kind in this hand.'
    
    def has_straight(self):
        """returns True if hand has five cards with ranks in sequence""" 
        rank_list = []
        
        #Ace counts as 1 and 14
        for card in self.cards:
            if card.rank == 1:
                rank_list.append(1)
                rank_list.append(14)
            else:
                rank_list.append(card.rank)
                
        #Remove duplicate ranks:
        rank_list = list(set(rank_list))
        rank_list.sort()
        
        # See if they are consecutive
        cumulative_count = 0
        pos = 0
        while pos < len(rank_list)-1:
            if rank_list[pos] + 1 == rank_list[pos+1]:
                cumulative_count += 1
                pos += 1
                if cumulative_count >= 4:
                    return True
            else:
                cumulative_count = 0
                pos += 1
        return False
        
    def has_flush(self):
        """Returns True if hand has five cards with the same suit."""
        suit_hist = self.suit_hist()
        for count in suit_hist.values():
            if count >= 5:
                return True
        return False
    
    def has_full_house(self):
        """returns True if there are three cards in one rank, two cards in another"""
        vals = self.ranks_hist().values()
        if 3 in vals:
            for i in vals:
                if i >= 2:
                    return ('This hand has full house')
        return False
        
    def has_four_of_a_kind(self):
        """returns True if there are four cards with same rank."""
        vals = self.ranks_hist().values()
        if 4 in vals:
            return 'This hand has four of a kind.'
        return False
    
    def has_straightflush(self):
        """returns True if there are five or more cards of the same suit and are in consecutive order"""
        ranks_hist = self.ranks_hist()
        if self.has_flush() == True: 
            for i in ranks_hist:
                if ranks_hist[i] >= 5:
                    x = i
            
deck = Deck()
deck.shuffle()
for i in range(5):
    hand = PokerHand()
    deck.move_cards(hand, 7)
    hand.sort()
    print(hand)
    print('\n')

