import random as rng
import player99Python as pp
import time
import read99Python as rp
import advBot99 as ab

#Reset deck to have 4 of each # except 2 jacks and 2 one-eye jacks
def resetDeck(players):
    deck = ['a','2','3','4','5','6','7','8','9','10','j','q','k','a','2','3','4','5','6','7','8','9','10','j','q','k','a','2','3','4','5','6','7','8','9','10','q','k','oj','a','2','3','4','5','6','7','8','9','10','q','k','oj']
    rng.shuffle(deck)
    for player in players:
        for card in player.hand:
            deck.remove(card)
    return deck

#Generates a number of players equal to the game size
def generateInitCompetition(num):
    numPlayers = num
    players = []
    for player in range(numPlayers):
        players.append(pp.Player())
    return players
    
#Deals the top card of the deck to the specified player, removing the card from the deck, and resetting the deck if empty
def dealCard(deck, player, discard, players):
    if len(deck) < 1:
        deck = resetDeck(players)
        discard = []
    card = deck[0]
    del deck[0]
    player.hand.append(card)
    return discard

#Run a single game
def runGame(players,firstplayer,state):
    for player in players:
        player.hand = []
    deck = resetDeck(players)
    discard = []
    currentNumber = 0
    for i in range(3):
        for player in players:
            discard = dealCard(deck, player, discard, players)
    gameLost = 0
    turnDirection = 1
    turn = firstplayer
    while gameLost == 0:
        currentNumber,directionChange,playedCard = players[turn].takeTurn(currentNumber, len(players), discard, turnDirection)
        discard.append(playedCard)
        if state:
            print(f"The card {playedCard} was played")
            print(f"The current number is now {currentNumber}")
        if currentNumber > 99:
            gameLost = 1
            return turn
        if directionChange:
            turnDirection = turnDirection * -1
        discard = dealCard(deck,players[turn],discard,players)
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
            players[runGame(players,j,False)].losses += 1
    #print([player.losses for player in players])
    #print([player.priorities for player in players])

def createTournamentWinner(rank,numPlayers,gamesPerGeneration):
    playersRankDict = {i:[] for i in range(rank+1)}
    while len(playersRankDict[rank]) < 1:
        playersRankDict[0] = [pp.Player(False) for i in range(numPlayers)]
        
        for column in list(playersRankDict.keys()):
            if len(playersRankDict[column]) == numPlayers:
                #print(f"Game rank: {column}")
                runCompetition(gamesPerGeneration,playersRankDict[column])
                playersRankDict[column+1].append(playersRankDict[column][[player.losses for player in playersRankDict[column]].index(min([player.losses for player in playersRankDict[column]]))])
                for player in playersRankDict[column+1]:
                    player.losses = 0
                playersRankDict[column] = []
    print(f"Winner has priorities:\n{playersRankDict[rank][0].priorities}")
    print(f"Winner has the default priorities:\n{playersRankDict[rank][0].defaultPriorities}")
    print(f"Winner has the coefficients:\n {[playersRankDict[rank][0].priorityCoefficients]}")
    return playersRankDict[rank][0]
        
def createGauntletWinner(generations,numPlayers,gamesPerGeneration):
    simple = bool(input("Generate simple bots only? True or False"))

    players = [pp.Player(simple)]
    for run in range(generations):
        for j in range(numPlayers-1):
            players.append(pp.Player(simple))
        for player in players:
            player.losses = 0
        #print(f"Generation {run}")
        runCompetition(gamesPerGeneration,players)
        for i in range(numPlayers-1):
            del players[[player.losses for player in players].index(max([player.losses for player in players]))]
        
    winner = players[[player.losses for player in players].index(min([player.losses for player in players]))]
    print(f"Finalists have the priorities:\n {winner.priorities}")
    print(f"Finalists have the default priorities:\n{winner.defaultPriorities}")
    print(f"Finalists have the coefficients:\n {[winner.priorityCoefficients]}")
    return winner

if __name__ == "__main__":
    
    numPlayers = int(input("Input # of players: "))
    gamesPerGeneration = int(input("Input # of games per generation: "))
    cycles = int(input("Input number of generations: "))
    runType = int(input("1 for tournament style, 2 for gauntlet, 3 for specific set, 4 to challenge 1, 5 to play against a bot, 6 to combine advBot bot player: "))
    mark = time.time()
    if runType == 1:
        winner = createTournamentWinner(cycles,numPlayers,gamesPerGeneration)
    elif runType == 2:
        winner = createGauntletWinner(cycles,numPlayers,gamesPerGeneration)
    
    elif runType == 3:
    #Forced competition between bots
        players = [rp.readPlayer() for i in range(numPlayers)]
        runCompetition(gamesPerGeneration,players)
        print([player.losses for player in players])
        winner = players[[player.losses for player in players].index(min([player.losses for player in players]))]

    elif runType == 4:
    #Run 1 player against random opponents until they lose
        players =[]
        players.append(rp.readPlayer())
        for i in range(numPlayers-1):
            players.append(pp.Player(False))
        dethroned = False
        while dethroned == False:
            players[0].losses = 0
            runCompetition(gamesPerGeneration,players)
            if [player.losses for player in players].index(min([player.losses for player in players])) != 0:
                dethroned = True
                winner = players[[player.losses for player in players].index(min([player.losses for player in players]))]
            else:
                for i in range(numPlayers-1):
                    del players[i+1]
                for i in range(numPlayers-1):
                    players.append(pp.Player(False))
    elif runType == 5:
        # Play against a bot
        players = [pp.Person(),rp.readPlayer()]
        for i in range(gamesPerGeneration):
            print(f"game {i}")
            players[runGame(players,i % 2,True)].losses += 1
        print([player.losses for player in players])

    elif runType == 6:
        # Set up a game of bots, allowing for advBot and players
        players = []
        for i in range(numPlayers):
            playerType = int(input("1 for bot, 2 for advBot, 3 for player"))
            if playerType == 1:
                players.append(rp.readPlayer())
            elif playerType == 2:
                players.append(ab.advBot())
            elif playerType == 3:
                players.append(pp.Person())
        for i in range(gamesPerGeneration):
            players[runGame(players,i % numPlayers,True)].losses  += 1
            print(f"game: {i}")
        print([player.losses for player in players])


    end = time.time() - mark
    print(f"Time: {end}")
    rp.writePlayer(winner)
    