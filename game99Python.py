import random as rng
import player99Python as pp
import time
import read99Python as rp

#Reset deck to have 4 of each # except 2 jacks and 2 one-eye jacks
def resetDeck():
    deck = ['a','2','3','4','5','6','7','8','9','10','j','q','k','a','2','3','4','5','6','7','8','9','10','j','q','k','a','2','3','4','5','6','7','8','9','10','q','k','oj','a','2','3','4','5','6','7','8','9','10','q','k','oj']
    rng.shuffle(deck)
    return deck

#Generates a number of players equal to the game size
def generateInitCompetition(num):
    numPlayers = num
    players = []
    for player in range(numPlayers):
        players.append(pp.Player())
    return players
    
#Deals the top card of the deck to the specified player, removing the card from the deck, and resetting the deck if empty
def dealCard(deck,player):
    if len(deck) < 1:
        deck = resetDeck()
    card = deck[0]
    del deck[0]
    player.hand.append(card)

#Run a single game
def runGame(players,firstplayer):
    for player in players:
        player.hand = []
    deck = resetDeck()
    currentNumber = 0
    for i in range(3):
        for player in players:
            dealCard(deck,player)
    gameLost = 0
    turnDirection = 1
    turn = firstplayer
    while gameLost == 0:
        currentNumber,directionChange = players[turn].takeTurn(currentNumber)
        if currentNumber > 99:
            gameLost = 1
            return turn
        if directionChange:
            turnDirection = turnDirection * -1
        dealCard(deck,players[turn])
        if turn == len(players) - 1 and turnDirection == 1:
            turn = 0
        elif turn == 0 and turnDirection == -1:
            turn = len(players) - 1
        else:
            turn += turnDirection
        #print([person.hand for person in players])
        #print(f"Num: {currentNumber}\nturnDirection: {turnDirection}")

def runCompetition(numSets,players):
    for i in range(numSets):
        for j in range(len(players)):
            players[runGame(players,j)].losses += 1
    #print([player.losses for player in players])
    #print([player.priorities for player in players])

def createTournamentWinner(rank,numPlayers,gamesPerGeneration):

    playersRankDict = {i:[] for i in range(rank+1)}
    while len(playersRankDict[rank]) < 1:
        playersRankDict[0] = [pp.Player() for i in range(numPlayers)]
        
        for column in list(playersRankDict.keys()):
            if len(playersRankDict[column]) == numPlayers:
                print(f"Game rank: {column}")
                runCompetition(gamesPerGeneration,playersRankDict[column])
                playersRankDict[column+1].append(playersRankDict[column][[player.losses for player in playersRankDict[column]].index(min([player.losses for player in playersRankDict[column]]))])
                for player in playersRankDict[column+1]:
                    player.losses = 0
                playersRankDict[column] = []
    print(f"Winner has priorities:\n{playersRankDict[rank][0].priorities}")
    return playersRankDict[rank][0]
        
def createGauntletWinner(generations,numPlayers,gamesPerGeneration):
    players = [pp.Player() for player in range(numPlayers-1)]
    for run in range(generations):
        players.append(pp.Player())
        for player in players:
            player.losses = 0
        print(f"Generation {run}")
        runCompetition(gamesPerGeneration,players)
        del players[[player.losses for player in players].index(min([player.losses for player in players]))]
        
    winner = players[[player.losses for player in players].index(max([player.losses for player in players]))]
    print(f"Finalists have the priorities:\n {winner.priorities}")
    print(f"Finalists have the default priorities:\n{winner.defaultPriorities}")
    print(f"Finalists have the coefficients:\n {[winner.priorityCoefficients]}")
    return winner

if __name__ == "__main__":
    
    numPlayers = int(input("Input # of players: "))
    gamesPerGeneration = int(input("Input # of games per generation: "))
    cycles = int(input("Input number of generations: "))
    runType = int(input("1 for tournament style, 2 for gauntlet, 3 for specific set: "))
    mark = time.time()
    if runType == 1:
        winner = createTournamentWinner(cycles,numPlayers,gamesPerGeneration)
    elif runType == 2:
        winner = createGauntletWinner(cycles,numPlayers,gamesPerGeneration)
    
    elif runType == 3:
    #Forced competition between 2
        players = [rp.readPlayer() for i in range(numPlayers)]
        runCompetition(gamesPerGeneration,players)
        print([player.losses for player in players])
        winner = players[[player.losses for player in players].index(min([player.losses for player in players]))]

    elif runType == 4:
    #Run 1 player against random opponents until they lose
        pass
    end = time.time() - mark
    print(f"Time: {end}")
    rp.writePlayer(winner)