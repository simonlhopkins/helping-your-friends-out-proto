import random
import math
import time


asciiFaceStuff = open("./asciiFaceData.txt", "r", encoding="utf8").read().split('\n')


sceneryList =open("./sceneryStuff.txt", "r").read().split('\n')
currentItem = ""
sceneryDict = {}
for line in sceneryList:
    if(len(line.split(" "))>1):
        if(line.split(" ")[0] == "ITEM"):
            currentItem = line.split(" ")[1]
            sceneryDict[currentItem] = []
        else:
            if(currentItem!=""):
                sceneryDict[currentItem].append(line)
    else:
        if(currentItem!=""):
            sceneryDict[currentItem].append(line)
#face construction
asciiFace = []
noses = []
eyes = []
mouths = []
eyebrows = []
hairL = []
hairR = []





for line in asciiFaceStuff:
    lineData = line.split(" ")
    if(lineData[0] == "noses"):
        noses = lineData[2:]
    elif(lineData[0] == "eyes"):
        eyes = lineData[2:]
    elif(lineData[0] == "mouths"):
        mouths = lineData[2:]
    elif(lineData[0] == "eyebrows"):
        eyebrows = lineData[2:]
    elif(lineData[0] == "hairL"):
        hairL = lineData[2:]
    elif(lineData[0] == "hairR"):
        hairR = lineData[2:]
    else:
        asciiFace.append(line)

class Scene():

    def __init__(self, id, initRequest, itemToGive):
        self.id =id
        self.hasBeenHelped = False
        self.itemsRequested = []
        self.itemsRequested.append(initRequest)
        self.itemToGive = itemToGive
        self.faceArray = []
        self.width = 0
        self.height = 6
        self.eyebrowChar = random.choice(eyebrows)
        self.eyeChar = random.choice(eyes)
        self.noseChar = random.choice(noses)
        self.mouthChar = random.choice(mouths)
        self.hairLChar = random.choice(hairL)
        self.hairRChar = random.choice(hairR)
    def getWidth(self):
        self.width = 0
        for line in self.getAsciiFaceArray():
            if(len(line)>self.width):
                self.width = len(line)
        return self.width
    def getAsciiFaceArray(self):
        self.faceArray = []
        for line in asciiFace:
            if("blank" in line):
                line = line.replace("blank", str(self.itemsRequested) + " -> " + self.itemToGive)

            if("B" in line):
                line = line.replace("B", self.eyebrowChar)
            if("E" in line):
                line = line.replace("E", self.eyeChar)
            if("N" in line):
                line = line.replace("N", self.noseChar)
            if("M" in line):
                line = line.replace("M", self.mouthChar)
            if("L" in line):
                line = line.replace("L", self.hairLChar)
            if("R" in line):
                line = line.replace("R", self.hairRChar)

            if(len(line)>self.width):
                self.width = len(line)
            self.faceArray.append(line)
        return self.faceArray
class VendingMachine():
    def __init__(self, itemsForSale, id):
        self.id = id
        self.itemsForSale = itemsForSale
        self.vendingMachineArray = sceneryDict["vendingMachine"]
        pass

class TrashCan():
    def __init__(self, contents, id):
        self.id = id
        self.contents = contents
        self.hasBeenUsed = False
        self.unusedTrashArray = sceneryDict["trashcan"]
        self.usedTrashArray = sceneryDict["usedTrashcan"]

class ShapeFace():
    def __init__(self, scenesOnFace, trashCansOnFace, vendingMachinesOnFace):
        self.scenesOnFace = scenesOnFace
        self.trashCansOnFace = trashCansOnFace
        self.vendingMachinesOnFace = vendingMachinesOnFace
class Game():
    def __init__(self):

        self.items =open("./itemsInWorld.txt", "r").read().split('\n')
        self.peopleDict = {}
        #dict of faces
        self.shapeFaceDict = {}
        self.inventory = {}
        self.maxLineLength = 0
        self.trashcansInGame = 6
        #item spawning parameters vvv read these in from file
        self.maxInitApperance = 3
        self.coinSpawnProbibility = 0.7
        self.itemsInVendingMachine = 4
        self.faceThreshold = 2
        self.numVendingMachines = 8
        #item spawning parameters ^^^

        #self.generateGame()
        self.generateGameTrueRandom()
        self.peoplePerFace = 0
        self.assignFaces()
        self.currentFaces = [0,1,2]
        self.message = ""

    def generateGameTrueRandom(self):
        #initTradeDict = {}
        unusedItems = self.items.copy()
        id = 0
        for item in self.items:
            exchangeChoice = item
            while exchangeChoice==item:
                exchangeChoice = random.choice(unusedItems)
            self.peopleDict[id] = Scene(id, exchangeChoice, item)
            # initTradeDict[item] = exchangeChoice
            if(self.peopleDict[id].getWidth()> self.maxLineLength):
                self.maxLineLength = self.peopleDict[id].getWidth()
            id +=1
    def generateGame(self):
        initTradeDict = {}
        unusedItems = self.items.copy()
        id = 0
        for item in self.items:
            exchangeChoice = item
            while exchangeChoice==item:
                if(len(unusedItems) == 1 and unusedItems[0] == item):
                    print("unused items is only of length 1")
                    print("it is also the same as the item we're on")
                    print("this means the last item of items was also randomly the last unused item")
                    break
                suggestedChoice = random.choice(unusedItems)
                if(suggestedChoice in initTradeDict):
                    #circular dependency
                    # i need to fix this lol
                    if(initTradeDict[suggestedChoice] == item):
                        if len(unusedItems)==1:
                            print("special case")
                        continue
                exchangeChoice =suggestedChoice
            unusedItems.remove(exchangeChoice)
            self.peopleDict[id] = Scene(id, item, exchangeChoice)
            initTradeDict[item] = exchangeChoice
            if(self.peopleDict[id].getWidth()> self.maxLineLength):
                self.maxLineLength = self.peopleDict[id].getWidth()
            id +=1
    #THIS IS PROPRIETARY TO DUMB PROTOTYPE
    #This is where I should also add trashcans and stuff
    def assignFaces(self):

        self.peoplePerFace = math.ceil(len(self.peopleDict)/8)
        availableToUse = list(self.peopleDict.keys()).copy()
        trashCanId = 0
        for i in range(0,8):
            idsOnFaces = []
            for j in range(0, self.peoplePerFace):
                if(len(availableToUse) == 0):
                    break
                choice = random.choice(availableToUse)
                idsOnFaces.append(choice)
                availableToUse.remove(choice)
            #I can place trash cans and vending machines here
            #based on +-2 faces and stuff. loop through face dict
            #lets start by putting one trashcan on each

            self.shapeFaceDict[i] = ShapeFace(idsOnFaces, [], [])
        #all of the faces are set
        #ASSIGN THE TRASHCANS TO THE FACES

        availableFaces = list(range(0,8))

        for i in range(0, self.trashcansInGame):
            choice = random.choice(availableFaces)
            peopleOptions = []
            while(len(peopleOptions)==0):
                diffOfFace = random.randrange(-self.faceThreshold, self.faceThreshold)
                peopleOptions = self.shapeFaceDict[(choice+diffOfFace)%8].scenesOnFace
            sceneNumOnFace= random.choice(peopleOptions)
            contents = ""
            #ASSIGN TRASH CAN CONTENTS
            if(random.random()>self.coinSpawnProbibility):
                contents = self.peopleDict[sceneNumOnFace].itemsRequested[0]
            else:
                contents = "coin"
            self.shapeFaceDict[choice].trashCansOnFace.append(TrashCan(contents, trashCanId))
            trashCanId+=1
            availableFaces.remove(choice)


        availableFaces = list(range(0,8))
        vendingMachineID = 0
        possibleOptions = set()

        for face in self.shapeFaceDict:
            for person in self.shapeFaceDict[face].scenesOnFace:
                for request in self.peopleDict[person].itemsRequested:
                    possibleOptions.add(request)
        for i in range(0, self.numVendingMachines):
            choice = random.choice(availableFaces)
            allOptions = set()
            while len(allOptions)<4:
                # peopleOptions = []
                # while(len(peopleOptions)==0):
                #     diffOfFace = random.randrange(-self.faceThreshold, self.faceThreshold)
                #     peopleOptions = self.shapeFaceDict[(choice+diffOfFace)%8].scenesOnFace
                #add random item to vending machine +- 2 faces
                allOptions.add(random.choice(list(possibleOptions)))

            self.shapeFaceDict[choice].vendingMachinesOnFace.append(VendingMachine(allOptions, vendingMachineID))
            vendingMachineID+=1
            availableFaces.remove(choice)


    def displayCurrentScene(self):
        # sceneArray = ["" for x in range(30)]
        sceneArray = []
        self.maxLineLength = 0
        for face in self.peopleDict:
            faceArray = self.peopleDict[face].getAsciiFaceArray()
            for line in faceArray:
                if len(line)> self.maxLineLength:
                    self.maxLineLength= len(line)

        offset = 0
        faceNumFromTop = 0
        cylinderXOffset = 6
        for i in range(0, 3):
            sceneArray.append(" "*(self.maxLineLength*self.peoplePerFace))

        sceneArray[2] = " "*cylinderXOffset + "_"*((self.peoplePerFace*self.maxLineLength)+1) + " " + ("_"*8)
        for i in range(0, 3):
            for j in range(0, 6):
                sceneArray.append("")
                leftChar = ''
                rightChar = ''
                if(i == 0):
                    leftChar = "/"
                    rightChar = "\\"
                elif(i == 2):
                    leftChar = "\\"
                    rightChar = "/"
                else:
                    leftChar = "|"
                    rightChar= "|"
                if(j == 5):
                    if(i ==2):
                        sceneArray[(i*6)+j+3] = (" " * cylinderXOffset)+ leftChar+ ("_"*((self.maxLineLength*self.peoplePerFace))) + leftChar + ("_" * ((6-cylinderXOffset)*2+8)) + rightChar
                    else:
                        sceneArray[(i*6)+j+3] = (" " * cylinderXOffset)+ leftChar+ ("_"*((self.maxLineLength*self.peoplePerFace))) + leftChar + (" " * ((6-cylinderXOffset)*2+8)) + rightChar
                else:
                    sceneArray[(i*6)+j+3]= (" "*cylinderXOffset) +leftChar+ (" "*(self.maxLineLength*self.peoplePerFace)) + leftChar + (" " * ((6-cylinderXOffset)*2+8)) + rightChar
                if(i==0):
                    cylinderXOffset-=1
                elif(i==2):
                    cylinderXOffset+=1
        #draw the scenery on top
        for face in self.currentFaces:
            if(faceNumFromTop == 0 or faceNumFromTop == 2):
                offset = 6
            else:
                offset = 0
            #DRAW FACES

            for i in range(0, 6):
                megaString = ""
                personNum = 0
                for sceneID in self.shapeFaceDict[face].scenesOnFace:
                    faceArray= self.peopleDict[sceneID].getAsciiFaceArray()
                    lineLen= len(faceArray[i])
                    megaString+=faceArray[i]
                    megaString+= sceneArray[(faceNumFromTop*6)+i][offset+(self.maxLineLength*personNum)+lineLen: offset+(self.maxLineLength*(personNum+1))]
                    personNum+=1
                sceneArray[(faceNumFromTop*6)+i] = sceneArray[(faceNumFromTop*6)+i][0:offset] + megaString + (sceneArray[(faceNumFromTop*6)+i][offset+ len(megaString):])

            #DRAW TRASHCANS
            trashcanXOffset = 20
            trashcanYOffset = 5
            if(len(self.shapeFaceDict[face].trashCansOnFace) != 0):
                pic = "trashcan"
                if(self.shapeFaceDict[face].trashCansOnFace[0].hasBeenUsed):
                    pic = "usedTrashcan"
                for i in range(0, len(sceneryDict[pic])):
                    sceneArray[(faceNumFromTop*6)+trashcanYOffset+i] = sceneArray[(faceNumFromTop*6)+trashcanYOffset+i][0: trashcanXOffset+offset] + sceneryDict[pic][i]+ sceneArray[(faceNumFromTop*6)+trashcanYOffset+i][trashcanXOffset + len(sceneryDict[pic][i])+offset:]


            vmXOffset = 30
            vmYOffset = 5
            if(len(self.shapeFaceDict[face].vendingMachinesOnFace) != 0):
                for i in range(0, len(sceneryDict["vendingMachine"])):
                    sceneArray[(faceNumFromTop*6)+vmYOffset+i] = sceneArray[(faceNumFromTop*6)+vmYOffset+i][0: vmXOffset+offset] + sceneryDict["vendingMachine"][i]+ sceneArray[(faceNumFromTop*6)+vmYOffset+i][vmXOffset + len(sceneryDict["vendingMachine"][i])+offset:]

            faceNumFromTop+=1

        #draw the you are here
        message = "<-- you are here"
        sceneArray[6] = sceneArray[6][0:3 + self.peoplePerFace*self.maxLineLength] + message + sceneArray[7][3 + len(message)+1 + self.peoplePerFace*self.maxLineLength:]

        #draw trash cans and vendingMachines

        #draw inventory probably
        #draw available commands
        sceneArray.extend(self.getUIArray())
        for i in sceneArray:
            print(i)
    def getUIArray(self):
        #UI STUFF PER FRAME
        activeFace = self.shapeFaceDict[self.currentFaces[0]]
        uiArray = []
        if(self.message!=""):
            uiArray.append(self.message)
            uiArray.append("")
        if(len(activeFace.trashCansOnFace) !=0):



            for trashcan in activeFace.trashCansOnFace:
                if(not trashcan.hasBeenUsed):
                    uiArray.append("there is a trashcan with somethin in it")
                    uiArray.append(trashcan.contents)
                else:
                    uiArray.append("there is an empty trashcan")


        if(len(activeFace.vendingMachinesOnFace) !=0):
            uiArray.append("there is a vending machine")
            for vm in activeFace.vendingMachinesOnFace:
                for item in vm.itemsForSale:
                    uiArray.append((" " * 4) + "coin -> " + item)

        uiArray.append("")
        uiArray.append("Inventory:")
        for key in self.inventory:
            if(self.inventory[key]==1):
                uiArray.append(key)
            else:
                uiArray.append(key + " x" +str((self.inventory[key])))


        #UI STUFF PER FRAME


        maxLineLen = 0
        for line in uiArray:
            if len(line)>maxLineLen:
                maxLineLen= len(line)
        if(len(uiArray)==0):
            return []
        returnArray = []
        returnArray.append("+" + ("-" * (maxLineLen + 2)) + "+")
        for line in uiArray:
            returnArray.append("| " + line + (" "*(maxLineLen-len(line))) + " |")
        returnArray.append("+" + ("-" * (maxLineLen + 2)) + "+")
        return returnArray
    def handleInput(self, arg):
        if(arg=="exit"):
            return

        activeFace = self.shapeFaceDict[self.currentFaces[0]]
        if(arg.startswith("take")):
            if(len(activeFace.trashCansOnFace)!=0):
                # tempMessage = "you recieved: "
                numAvailable= 0
                tempMessage = ""
                for trashcan in activeFace.trashCansOnFace:
                    if(not trashcan.hasBeenUsed):
                        if(trashcan.contents not in self.inventory):
                            self.inventory[trashcan.contents] = 0
                        self.inventory[trashcan.contents] +=1
                        tempMessage+= trashcan.contents + ", "
                        trashcan.hasBeenUsed=True
                        numAvailable+=1
                if(numAvailable!=0):
                    tempMessage += "you recieced: " + tempMessage
                else:
                    tempMessage = "you already used all of these trashcans"
                self.message = tempMessage
            else:
                self.message = "there are nothing to take"
        elif(arg.startswith("up") or arg =="u"):
            self.message = "move up (rotating the cylinder counter clockwise)"
            for i in range(0,3):
                self.currentFaces[i]-=1
                self.currentFaces[i]%=8
        elif(arg.startswith("down") or arg =="d"):
            self.message = "move down (rotating the cylinder clockwise)"
            for i in range(0,3):
                self.currentFaces[i]+=1
                self.currentFaces[i]%=8
        elif(arg.startswith("help")):
            self.handleHelp(activeFace)
        elif(arg.startswith("vend")):
            itemToVend = arg[4:].strip()
            activeFace = self.shapeFaceDict[self.currentFaces[0]]

            if(len(activeFace.vendingMachinesOnFace) == 0):
                self.message = "there are no vending machines on this face"
                self.displayCurrentScene()
                return
            if("coin" not in self.inventory):
                self.message = "you have no money!"
                self.displayCurrentScene()
                return
            itemInAMachine = False
            for machine in activeFace.vendingMachinesOnFace:
                if(itemToVend in machine.itemsForSale):
                    if(itemToVend not in self.inventory):
                        self.inventory[itemToVend]= 0
                    self.inventory[itemToVend]+=1
                    if(self.inventory["coin"]==1):
                        self.inventory.pop("coin")
                    else:
                        self.inventory["coin"]-=1
                    self.message="you got " + itemToVend +" from the vending machine"
                    itemInAMachine = True
                    break
            if(not itemInAMachine):
                self.message += itemToVend + " not in any machine"
        elif(arg == "debug"):
            self.printDebug()
        else:
            self.message = "unrecognized input: " + currentCommand
        self.displayCurrentScene()

    def printDebug(self):
        print("visible faces")

        for i in self.currentFaces:
            print("\t"+ str(i))
        print("assignedFaces")
        for face in self.shapeFaceDict:
            print("FACE " + str(face))
            print("\tpeople")
            for i in self.shapeFaceDict[face].scenesOnFace:
                print("\t\t" + str(i))
            print("\ttrashcans: " + str(len(self.shapeFaceDict[face].trashCansOnFace)))
            print("\tvending machines " + str(len(self.shapeFaceDict[face].vendingMachinesOnFace)))
    def handleHelp(self, activeFace):
        #check if only one person wants it
        peopleWhoYouCanHelp = []
        for scene in activeFace.scenesOnFace:
            if(all(elem in list(self.inventory.keys()) for elem in self.peopleDict[scene].itemsRequested)):
                peopleWhoYouCanHelp.append(scene)

        personNum = 0
        personToHelp = -1
        if(len(peopleWhoYouCanHelp) == 0):
            self.message = "you can't help anyone on this layer"
            return
        while personToHelp not in peopleWhoYouCanHelp:

            for person in peopleWhoYouCanHelp:
                print(person)
                faceArray = self.peopleDict[person].getAsciiFaceArray()
                for line in faceArray:
                    print(line)
                personNum+=1

            personToHelp = input("who do you want to help?")
            if(personToHelp.isdigit()):
                personToHelp = int(personToHelp)
            else:
                print("input not valid")
        conflicts = []
        for person in self.peopleDict:
            if(person == personToHelp):
                continue
            if(self.peopleDict[person].hasBeenHelped):
                continue
            for item in self.peopleDict[personToHelp].itemsRequested:
                if item in self.peopleDict[person].itemsRequested:
                    conflicts.append(person)
                    break
        if len(conflicts)>0:
            print("you are making " + str(len(conflicts)) + " people upset by doing this")

        for person in conflicts:
            if len(self.peopleDict[person].itemsRequested)==2:
                continue
            choice = self.peopleDict[person].itemToGive
            while choice in self.peopleDict[person].itemsRequested or choice == self.peopleDict[person].itemToGive:
                choice = random.choice(self.items)
            self.peopleDict[person].itemsRequested.append(choice)
            print(self.peopleDict[person].itemsRequested)
        activeFace.scenesOnFace.remove(personToHelp)
        self.peopleDict[personToHelp].hasBeenHelped = True
        for item in self.peopleDict[personToHelp].itemsRequested:
            self.inventory[item]-=1
            if(self.inventory[item] == 0):
                self.inventory.pop(item)
        if self.peopleDict[personToHelp].itemToGive not in self.inventory:
            self.inventory[self.peopleDict[personToHelp].itemToGive] = 0
        self.inventory[self.peopleDict[personToHelp].itemToGive]+=1


    def executeGive(self, itemToGive, activeFace, person):
        self.message = "giving " +itemToGive + " to person "
        activeFace.scenesOnFace.remove(person)
        if(self.inventory[itemToGive] == 1):
            self.inventory.pop(itemToGive)
        else:
            self.inventory[itemToGive] -=1
        if(self.peopleDict[person].itemToGive not in self.inventory):
            self.inventory[self.peopleDict[person].itemToGive] = 0
        self.inventory[self.peopleDict[person].itemToGive]+=1


Game = Game()

def handleAdd(item):
    if(item not in Game.items):
        print(item + " not a valid item")
        return
    if item not in Game.inventory:
        Game.inventory[item] = 0
    Game.inventory[item] +=1
    print("you now have, through the power of god: " + item)

def introSceneLine(line, timeAfter):
    print(line)
    time.sleep(timeAfter)
def introScene():
    pass
currentCommand = ""
introScene()
Game.displayCurrentScene()
while currentCommand!="exit":
    currentCommand = input("enter a command: ")
    if(currentCommand.startswith("add")):
        handleAdd(currentCommand[3:].strip())
    Game.handleInput(currentCommand)
