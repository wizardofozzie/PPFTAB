# Blackjack
# From 1-7 players compete against the dealer

import games, cards

class BJ_Card(cards.Card):
    """ A Blackjack Card. """
    ACE_VALUE = 1

    @property
    def value(self):
        """ For face-up cards, returns point value of a card (based on rank's index). Otherwise returns None."""
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Deck(cards.Deck):
    """ Creates a Deck of Blackjack cards. """
    def populate(self):     # Overrides parent populate method using Blackjack Card objects
        """ Populate  """
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))


class BJ_Hand(cards.Hand):
    """ A Blackjack Hand. """
    def __init__(self, name):       # Overrides method to add a name attribute representing player name
        super(BJ_Hand, self).__init__()
        self.name = name
    def __str__(self):
        rep = self.name + ':\t' + super(BJ_Hand, self).__str__()
        if self.total:
            rep += '(' + str(self.total) + ')'
        return rep

    @property
    def total(self):
        # if a card in the hand has a value of None (ie face-down), then total is None
        for card in self.cards:
            if not card.value:
                return None

        # add up card values, treat each Ace as 1
        t = 0
        for card in self.cards:
            t += card.value

        # determine if card contains an Ace
        contains_Ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_Ace = True

        # should Ace value be 1 or 11?
        if contains_Ace and t < 11: # <= 11  ?????
                                    # if hand contains an Ace, and total is low enough, treat Ace as 11
            # add only 10 since we've already added 1 for the Ace
            t += 10

        return t

    def is_busted(self):
        return self.total > 21

    class BJ_Player(BJ_Hand):
        """ A Blackjack Player. """
        def is_hitting(self):
            """ Returns True if player wants another card. """
            response = games.ask_yes_or_no('\n' + self.name + ', do you want to hit? (Y/N): ')
            return response == 'y'
        # return response.lower().startswith('y')

    # next 4 functions are integral to allowing betting
    def bust(self):
        print(self.name, 'busts.')
        self.lose()

    def lose(self):
        print(self.name, 'loses.')

    def win(self):
        print(self.name, 'wins.')

    def push(self):
        print(self.name, 'pushes.')


class BJ_Dealer(BJ_Hand):
    """ A Blackjack Dealer. """
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, 'busts')

    def flip_first_card(self):
        """ Turns over the dealer's first card. """
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """ A Blackjack Game. """
    def __init__(self, names):
        self.players = []
        for name in names:  # for each element of list containing players
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer('Dealer')

        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        """ Deals addition cards to player/dealer while player is not busted and is requesting to hit. """
        while not player.is_busted and player.is_hitting():
            self.deck.deal([player])    # needs to be a list object for deal method
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):     # very similar to pseudo-code
        # deal 2 initial cards to everyone
        self.deck.deal(self.players + [self.dealer], per_hand = 2)
        self.dealer.flip_first_card()       # hide dealer first card
        for player in self.players:
            print(player)
        print(self.dealer)

        # deal additional cards to players
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()       # reveal dealer's first card

        if not self.still_playing:          # ie all players not playing
            print(self.dealer)
        else:                               # deal additional cards to dealer
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # everyone still playing wins
                for player in self.still_playing:
                    player.win()
            else:
                # compare each player still playing to the dealer
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
                    # elif player.total == self.dealer.total:
                    # #     player.push()
                    # else:
                    #     raise ValueError

        # remove everyone's cards
        for player in self.players:
            player.clear()
        self.dealer.clear()

def main():
    """ Gets player names (as a list) and creates a BJ_Game object. Plays Blackjack until player opts out. """

    print("\t\twelcome to blackjack".title())

    names = []
    numbers_of_players = games.ask_number("How many players? (1-7): ", low=1, high=8)
    for i in range(numbers_of_players):
        name = input('Player name?: ')
        names.append(name)

    print()

    game = BJ_Game(names)

    again = None
    while again != 'n':
        game.play()
        again = games.ask_yes_or_no('Do you want to play again? (Y/N): ')

main()
input('Press ENTER to EXIT.')


