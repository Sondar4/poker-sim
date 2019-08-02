import poker

names = ['Jack', 'Jessica', 'Jimmy', 'John']

if __name__ == '__main__':

    iteration = 0
    n = 100
    
    while iteration < n:
        iteration += 1
        deck1 = poker.Deck()
        deck1.shuffle()

        players = list()
        for name in names:
            players.append(poker.Hand(name))
        table = poker.Hand('Table')

        for player in players:
            deck1.move_cards(player, 2)
        deck1.move_cards(table, 5)

        results = list()
        for player in players:
            results.append(player.best_hand(table))

        scores = list()
        for i in range(len(results)):
            scores.append(poker.rate(*results[i]))

        winner = scores.index(max(scores))

        for player in players:
            print(player.label, player, sep='\n', end='\n\n')
        print(table.label, table, sep='\n', end='\n\n')
        
        for i in range(len(players)):
            print(players[i].label, 'has a', results[i][1], 'with score', scores[i], sep=' ', end='\n\n')
        print(players[winner].label, 'is the winner', sep=' ')
        input('----Next Round----\n')