import sys
def playCard(num,card,active):
    if card in ['2','3','4','5','6','7']:
        return (num + int(card), False, card)
    elif card in ['j','q','k']:
        return (num + 10,False, card)
    elif card == 'a':
        return (num + 1,False, card)
    elif card == 'oj':
        return (99,False, card)
    elif card == '8':
        if active:
            return num,True,card
        return (num,False, card)
    elif card == '9':
        return (num,False, card)
    elif card == '10':
        return (num -10,False, card)
    else:
        print("FATAL ERROR: INVALID CARD PLAYED")
        exit()

def checkDeath(number, card):
    if card in ['2','3','4','5','6','7']:
        if (number + int(card)) > 99:
            return 1
        return 0
    elif card in ['j','q','k']:
        if (number + 10) > 99:
            return 1
        return 0
    elif card in ['a']:
        if (number + 1) > 99:
            return 1
        return 0
    else:
        return 0
    
def newNumber(number,card):
    if card in ['2','3','4','5','6','7']:
        return number + int(card)
    elif card in ['j','q','k']:
        return number + 10
    elif card in ['a']:
        return number + 1
    elif card in ['8','9']:
        return number
    elif card in ['oj']:
        return 99
    elif card in ['10']:
        return number - 10

class advBot:

    # Init self, with possible cards and 
    def __init__(self):
        self.priorities = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'oj']
        self.cards = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'oj']
        self.hand = []
        self.losses = 0
        self.depth = int(input("Adv bot depth: "))

    # Builds what a possible deck looks like
    def buildDeck(self,discard):
        deck = ['a','2','3','4','5','6','7','8','9','10','j','q','k','a','2','3','4','5','6','7','8','9','10','j','q','k','a','2','3','4','5','6','7','8','9','10','q','k','oj','a','2','3','4','5','6','7','8','9','10','q','k','oj']
        for card in discard:
            if card in deck:
                deck.remove(card)
        for card in self.hand:
            if card in deck:
                deck.remove(card)
        return deck

    # Returns a list describing the chances of what the next card will be
    def cardChance(self, discard, deck):
        chances = [deck.count(card) / len(deck) for card in self.cards]
        return chances
    
    def chanceInThree(self,discard,deck,card):
        chances = [(len(deck) - deck.count(card) - i) / len(deck) for i in range(3) if deck.count(card) - i >= 0 ]
        for i in range(3 - len(chances)):
            chances.append(1)
        return 1 - (chances[0] * chances [1] * chances[2])

    # Returns a list describing the chance that a player has each given card in their hand
    def handChance(self, discard):
        deck = self.buildDeck(discard)
        chances = [self.chanceInThree(discard,deck,card) for card in self.cards]
        return chances


    # Will return a tuple in the form (survivability, lethality)
    def analyseTurn(self, number, discard, players, depth, currentPlayer, depthLim, direction):


        
        # Base case: If back on bot, if at depthLim: return bedrock lethality
        if currentPlayer == 0 or currentPlayer == players:
            depth += 1
            if depthLim <= depth:
                doom = [checkDeath(number,card) for card in self.hand]
                if 0 in doom:
                    survivability = 0.6 + sum([0.3 for card in self.hand if checkDeath(99,card) == 0])
                    return (survivability, 0)
                else:
                    survivability = 0
                    return (survivability, 0)
            else:
                pass

        # Create a theoretical hand for future calculations
        handChances = self.handChance(discard)
        lethalList = []
        survivalList = []
        for card in range(len(handChances)):
            # if the card is 8, find its special snowflake lethality. Otherwise, check if a card is directly lethal, and then analyse
            if handChances[card] != 0:
                if card != 7:
                    if checkDeath(number, self.cards[card]):
                        survival, futureLethal = self.analyseTurn(newNumber(number, self.cards[card]), discard + [self.cards[card]], players, depth, currentPlayer + direction, depthLim, direction)
                        lethalList.append(handChances[card] * futureLethal)
                        survivalList.append(survival * handChances[card])
                    else:
                        lethalList.append(1 * handChances[card])
                        survivalList.append(1 * handChances[card])
                else:
#                    if currentPlayer == 1:
                    survival, futureLethal = self.analyseTurn(newNumber(number, self.cards[card]), discard + [self.cards[card]], players, depth, currentPlayer + direction, depthLim, direction * -1)
                    lethalList.append(handChances[card] * futureLethal)
                    survivalList.append(handChances[card] * survival)
#                    else:
#                        survival, futureLethal = self.analyseTurn(newNumber(number, self.cards[card]), discard + [self.cards[card]], players, depth, currentPlayer + direction, depthLim, direction)
#                        lethalList.append(handChances[card] * futureLethal)
#                        survivalList.append(handChances[card] * survival)
            else:
                lethalList.append(0)
                survivalList.append(0)

        lethal = sum(lethalList)
        surv = sum(survivalList)
        
        # print(f"Lethality: {lethal}\nSurvivability: {surv}")

        return (surv,lethal)
        
    def playCard(self,num,card,active):
        if card in ['2','3','4','5','6','7']:
            return (num + int(card),False)
        elif card in ['j','q','k']:
            return (num + 10,False)
        elif card == 'a':
            return (num + 1,False)
        elif card == 'oj':
            return (99,False)
        elif card == '8':
            if active:
                return num,True
            return (num,False)
        elif card == '9':
            return (num,False)
        elif card == '10':
            return (num -10,False)
        else:
            print("FATAL ERROR: INVALID CARD PLAYED")
            exit()
        
    # Take turn for advBot    
    def takeTurn(self, num, numPlayers, discard, direction):
        #Initialize a dictionary, a surv,leth tuple for each number
        priorities = {card:[0,0] for card in self.cards}
        # for each card, analyse the turn on
        for card in self.hand:
            nextplayer = 1
            if nextplayer == -1:
                nextplayer = numPlayers - 1
            if checkDeath(num, card) == 0:
                priorities[card][0], priorities[card][1] = self.analyseTurn(newNumber(num, card), discard + [card], numPlayers, 0, nextplayer, self.depth, 1)
        # Calculate the best card to play and return it in the form: (newNumber, directionChange, playedCard)

        priorityList = list(priorities.items())
        priorityList.sort(key = lambda x: x[1][0])
        if priorityList[-1][1][0] == 0:
            return (100, False, priorityList[-1][0])
        self.hand.remove(priorityList[-1][0])
        return playCard(num, priorityList[-1][0], True)
    
