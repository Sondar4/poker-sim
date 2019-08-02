import poker as pk
import PySimpleGUI as sg
from sys import exit
from copy import deepcopy

"""This is a module that simulates a poker game in order to make simulations
and see the probabilities that a sigle user has to win on a specific scenario.
"""

ranks = ('Not Defined', 'Ace', '2', '3', '4', '5', '6', '7',
         '8', '9', '10', 'Jack', 'Queen', 'King')

suits = ('Not Defined', 'Clubs', 'Diamonds', 'Hearts', 'Spades')
    

def get_suit(suit_name):
    return suits.index(suit_name)-1


def get_rank(rank_name):
    if rank_name == 'Ace':
        return 14
    return ranks.index(rank_name)


def simulate_games(your_hand, table, number_of_players, deck, n):
    """Simulates n poker games with the scenario and returns the number of won games.

    input: Hand, Hand, int, Deck, int
    output: int
    """
    veiled_cards = 5-len(table.cards)
    wins = 0

    for i in range(n):
   
        progress = sg.OneLineProgressMeter('Simulations in process...', i+1, n, 'key')   
        if i < n-1 and not progress:
            return 0
        #Restart all variables for each simulation
        new_deck = deepcopy(deck)
        new_deck.shuffle()
        other_players = []
        new_table = deepcopy(table)

        j = 0
        while j < int(number_of_players)-1:
            other_players.append(pk.Hand('Player '+str(i)))
            new_deck.move_cards(other_players[-1], 2)
            j += 1

        j = 0
        while j < veiled_cards:
            new_deck.pop_card()
            new_deck.move_cards(new_table, 1)
            j += 1

        your_score = pk.rate(*your_hand.best_hand(table))
        other_scores = []
        for player in other_players:
            other_scores.append(pk.rate(*player.best_hand(table)))
        if your_score > max(other_scores):
            wins += 1

    return wins


def second_display(your_hand, table, number_of_players, deck):
    """This functions creates the second display window, where there is the
    option to simulate rounds.

    input: Hand, Hand, int, Deck
    """
    winrate = 'not defined'
    option = ''
    while option != 'Exit':
        veiled_cards = 5-len(table.cards)
        second_layout = [
                [sg.Frame(layout=[  
                    [sg.Text(str(your_hand))]], 
                    title='Your Hand'),
                sg.Frame(layout=[  
                    [sg.Text(str(table)+'\nUnknown card'*veiled_cards)]], 
                    title='Table'),
                    ],
                [sg.Text('Number of simulations'), sg.InputCombo((10, 100, 1000, 10000, 100000,
                                                                  1000000, 10000000))],
                [sg.Text('Number of players:\t'+str(number_of_players))],
                [sg.Text('Winrate:\t'+str(winrate)+'%')],
                [sg.Button('Start simulation'), sg.Button('Unveil another card'), sg.Button('Exit')]
                ]

        second_window = sg.Window('Poker Simulator').Layout(second_layout)
        option, value = second_window.Read()

        if option == 'Unveil another card':
            if veiled_cards > 0:
                deck.pop_card() #Burn one card, then take a card
                deck.move_cards(table, 1)
                veiled_cards = 5-len(table.cards)
            else:
                sg.Popup('All table cards are already unveiled')

        if option == 'Start simulation':
            winrate = simulate_games(your_hand, table, number_of_players, deck, int(value[0]))
            winrate /= int(value[0])
            winrate *= 100

        second_window.Close()


if __name__ == '__main__':
    sg.SetOptions(icon='icon_card.ico')
    first_layout = [
                [sg.Frame(layout=[  
                    [sg.Text('Card 1'), sg.InputCombo(ranks), sg.InputCombo((suits))],
                    [sg.Text('Card 2'), sg.InputCombo(ranks), sg.InputCombo((suits))]], 
                    title='Your Hand'),
                sg.Frame(layout=[  
                    [sg.Text('Card 1'), sg.InputCombo(ranks), sg.InputCombo((suits))],
                    [sg.Text('Card 2'), sg.InputCombo(ranks), sg.InputCombo((suits))],
                    [sg.Text('Card 3'), sg.InputCombo(ranks), sg.InputCombo((suits))],
                    [sg.Text('Card 4'), sg.InputCombo(ranks), sg.InputCombo((suits))],
                    [sg.Text('Card 5'), sg.InputCombo(ranks), sg.InputCombo((suits))]], 
                    title='Table'),
                    ],
                [sg.Text('Number of players:'), sg.InputCombo((2,3,4,5,6,7,8,9,10,11))],
                [sg.Button('Ok'),
                sg.Button('Cancel'),
                sg.Button('Generate random scenario')]
              ]

    your_hand = pk.Hand('You')
    table = pk.Hand('table')

    first_window = sg.Window('Poker Simulator').Layout(first_layout)
    option, value = first_window.Read()
    first_window.Close()

    if option == 'Ok':
        if 'Not Defined' in value[:10]:
            #Not enough cards defined
            sg.Popup('Not enough cards defined')
            exit()
        cards = []
        i = 0
        while i < 14:
            if 'Not Defined' not in (value[i+1], value[i]):
                cards.append(pk.Card(get_suit(value[i+1]), get_rank(value[i])))
                i += 2
            else:
                break
        your_hand.cards.append(cards[0]) 
        your_hand.cards.append(cards[1])
        for i in range(len(cards)-2):
            table.cards.append(cards[i+2])
        unvelied_cards = len(table.cards)
        deck = pk.Deck(used_cards=your_hand.cards+table.cards)
        deck.shuffle()

    elif option == 'Generate random scenario':
        deck = pk.Deck()
        deck.shuffle()
        deck.move_cards(your_hand, 2)
        deck.move_cards(table, 3)
    else:
        exit()

    number_of_players = value[-1]
    other_players = []
    i = 0

    second_display(your_hand, table, number_of_players, deck)