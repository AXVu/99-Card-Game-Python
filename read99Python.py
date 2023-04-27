import csv
import player99Python as pp
import advBot99 as ab

def writePlayer(player):
    playerName = input("Input player name: ")
    if playerName == "end":
        exit()
    filename = f"{playerName}playerData.csv"
    with open(filename, mode="w",newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player.defaultPriorities[i] for i in ['a','2','3','4','5','6','7','8','9','10','j','q','k','oj']])
        writer.writerow([player.priorityCoefficients[i][0] for i in ['a','2','3','4','5','6','7','8','9','10','j','q','k','oj']])
        writer.writerow([player.priorityCoefficients[i][1] for i in ['a','2','3','4','5','6','7','8','9','10','j','q','k','oj']])
    print(f"Data saved under filename: {filename}")

def readPlayer():
    playerName = input("Input player name: ")
    if playerName in ["god","advbot","ab"]:
        return ab.advBot
    filename = f"{playerName}playerData.csv"
    player = pp.Player(False)
    with open(filename,mode="r") as file:
        reader = csv.reader(file)
        cardList = ['a','2','3','4','5','6','7','8','9','10','j','q','k','oj']
        readRow = []
        for row in reader:
            readRow.append({card:num for card,num in zip(cardList,row)})
        player.defaultPriorities = readRow[0]
        temp = list(readRow[1].values())
        player.priorityCoefficients = {card:(num1,num2) for card,num2,num1 in zip(cardList,list(readRow[2].values()),temp)}
        player.updatePriorities(0)
    return player