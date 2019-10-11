"""This script uses de poker.py module and the Montecarlo methods to calculate
the probability of the different hands of poker.
"""
import poker
from tqdm import tqdm
hands = ['highest card', 'pair', 'two pair', 'three of a kind', 'straight',
         'flush', 'full house', 'four of a kind', 'straight flush']

n = input('Number of simulations?\t')
try:
    n=int(n)
except:
    print('Value not valid')
    exit(1)

with open('montecarlo-results.txt', 'w') as fout:
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    print('Running simulations')
    for i in tqdm(range(n)):
        deck = poker.Deck()
        deck.shuffle()
        player = poker.Hand('Player')
        table = poker.Hand('Table')
        deck.move_cards(player, 2)
        deck.move_cards(table, 5)
        results[player.best_hand(table)[0]] += 1
    for i in range(9):
        if i == 1 or i == 5:
            fout.write(hands[i] + '\t\t' + '{0:.7f}'.format(results[i]/n) + '\n')
        else:
            fout.write(hands[i] + '\t' + '{0:.7f}'.format(results[i]/n) + '\n')