import random as rng
import game99Python as gp

class Player:
    def __init__(self, simple):
        self.priorities = ['a','2','3','4','5','6','7','8','9','10','j','q','k','oj']
        rng.shuffle(self.priorities)
        self.prioritiesNums = {num:pri for num,pri in zip(self.priorities,range(14))}
        self.defaultPriorities = self.prioritiesNums.copy()
        if simple:
            self.priorityCoefficients = {num:(0,0) for num in self.priorities}
        else:
            self.priorityCoefficients = {num:(rng.randrange(-1000,1000)/10000,rng.randrange(-1000,1000)/10000) for num in self.priorities}
        self.hand = []
        self.losses = 0


    def playCard(self,num,card,active):
        if card in ['2','3','4','5','6','7']:
            return (num + int(card), False, card)
        elif card in ['j','q','k']:
            return (num + 10, False, card)
        elif card == 'a':
            return (num + 1, False, card)
        elif card == 'oj':
            return (99, False, card)
        elif card == '8':
            if active:
                return (num, True, card)
            return (num, False, card)
        elif card == '9':
            return (num, False, card)
        elif card == '10':
            return (num -10, False, card)
        else:
            print("FATAL ERROR: INVALID CARD PLAYED")
            exit()

    def updatePriorities(self,num):
        self.prioritiesNums = {card:self.defaultPriorities[card]+self.priorityCoefficients[card][0]*num+self.priorityCoefficients[card][1]*num*num for card in self.priorities}
        self.tempPriorities = [i for i in self.prioritiesNums.items()]
        self.tempPriorities.sort(key = lambda x: x[1])
        self.priorities = [i[0] for i in self.tempPriorities]

    def takeTurn(self,num, numPlayers, discard, direction):
        self.updatePriorities(num)
        for select in range(len(self.priorities)):
            for check in range(3):
                if self.priorities[select] == self.hand[check] and self.playCard(num,self.priorities[select],False)[0] < 100:
                    del self.hand[check]
                    
                    return self.playCard(num,self.priorities[select],True)


        return (100,False,'k')

class Person:

    def __init__(self):
        self.hand = []
        self.losses = 0

    def takeTurn(self,num, numPlayers, discard, direction):
        print(self.hand)
        play = -1
        while not play in [0,1,2]:
            play = int(input("Pick card to play as an index (0,1,2)"))
        card = self.hand[play]
        
        del self.hand[play]
        return self.playCard(num,card,True)

    def playCard(self,num,card,active):
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