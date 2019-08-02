"""This script uses de poker.py module and the Montecarlo methods to calculate
the probability of the different hands of poker.
"""
import poker
n = 10000 #Number of simulations
hands = ['highest card', 'pair', 'two pair', 'three of a kind', 'straight',
         'flush', 'full house', 'four of a kind', 'straight flush']
results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
i = 0
while i < n:
    deck = poker.Deck()
    deck.shuffle()
    player = poker.Hand('Player')
    table = poker.Hand('Table')
    deck.move_cards(player, 2)
    deck.move_cards(table, 5)
    results[player.best_hand(table)[0]] += 1
    i += 1
for i in range(9):
    if i == 1 or i == 5:
        print(hands[i], '{0:.7f}'.format(results[i]/n), sep='\t\t')
    else:
        print(hands[i], '{0:.7f}'.format(results[i]/n), sep='\t')