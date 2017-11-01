
##
## Artificial Intelligence Final Project
##
## ####
##
## James Clisham
##
## 
## Ant Colony Optimization implemented in a variety of ways to solve the graph coloring problem.
## Primary focus on manipulating the various different components of ACO and pitting them against
## each other in trials.
##

import os, sys, time, random, curses

#
# DEBUG ISSUES
#
# If the program is crashing randomly on startup with an error saying something about addch error, or any kind of
# window initialization error, then the window is probably not large enough for the curses output. I'm developing
# and testing on a size of 1024x768, so running the program in a terminal at least as large as that shouldn't have 
# this issue.
#
# ** Further Note **
# If experimenting with the number of nodes, the program will crash if the nodes go offscreen due to curses'
# handling of drawing. This could be fixed by having everything print out to a 'pad' instead of a 'window', if
# anyone so desires to go through the arduous process of doing so. I hate to phrase it like that, but hey, time
# limits.







#
# GLOBAL VALUES
#


NUM_OF_NODES_IN_GRAPH = 20
MAX_Y_VALUE_OF_GRAPH_NODE = 5

NUM_OF_CYCLES = 1000
NUM_OF_ANTS = 5

PHEROMONE_STRENGTH = .05
INITIAL_PHEROMONE_QUANTITY = .5
PHEROMONE_DECAY_RATE = .02
MOVEMENT_PHEROMONE_DECAY = .1

RANDOM_MOVE_CHANCE = 30
PHEROMONE_MOVE_CHANCE = 70


# Delay Value
# 
# For delaying output for long enough between cycles to be visible to the human eye
#
# NOTICE: I am writing and testing this code on a laptop from 1999, and have less than 256mb of RAM.
# The delay will likely need to be adjusted for any other computer running this code.
#
# It is implemented as an iterator and has to reach the specified value each frame before the frame is
# actually processed. 100 works for me, but I'm willing to bet any modern computer will need a significantly
# larger number for testing.
#
# With a value of 0, there is no delay and will skip straight to the end of the calculation.
#

DISPLAY_DELAY = 0




#
# CLASS DEFINITIONS
# 



class Ant:

    def __init__(self):

        self.xCoord = 0
        self.yCoord = 0


#
# AntColony Algorithm 1
#
# -Random movement
# -Random color selection based on local conflicts
#
# 
#

class AntColonyAlg1:


    def __init__(self,solution,numberOfAnts,numberOfCycles,displayDelay): #Initialization of class variables


        # if there are more ants than nodes, set number of ants to number of nodes
        if(numberOfAnts>solution.numOfNodes):
            numberOfAnts = solution.numOfNodes

        self.numberOfAnts = numberOfAnts
        self.numberOfCycles = numberOfCycles

        
        self.randomMoveChance = 200   # Always chooses random movement over pheromone movement
        
        self.displayDelay = displayDelay
        
        
        
        self.antList = []


        for i in range(0,numberOfAnts): # Sets up initial ant list

            newAnt = Ant()
            self.antList.append(newAnt)



    def solve(self,solution,outputWindow):  # Main Solving Loop


        # ##
        # determineNumOfConflictingNodes
        # ##
        #
        # Returns the number of overall conflicting nodes in the entire problem (not used in this algorithm)
        #

        def determineNumOfConflictingNodes(solution):

            conflictingNum = 0
            for yList in solution.nodeList:

                for eachNode in yList:

                    for i in eachNode.connectedNodeList:

                        if(i.color==eachNode.color):
                            conflictingNum += 1


            return conflictingNum


        # ##
        # determineNumOfLocalConflicts
        # ##
        #
        # Returns the number of local color conflicts around the specificed node
        #

        def determineNumOfLocalConflicts(node):

            localConflicts = 0
            for i in node.connectedNodeList:

                if(i.color==node.color or node.color==0 or i.color==0):

                    localConflicts += 1

            return localConflicts



        # ##
        # changeColorOfNode
        # ##
        #
        # Randomly picks a new color for the specified node
        #


        def changeColorOfNode(node):

            colorDifferent = False
            while(colorDifferent==False):

                newColor = random.randrange(1,4)
                if(node.color==newColor):
                    pass
                else:
                    node.color = newColor
                    colorDifferent = True
        # ##
        # moveAnt
        # ##
        #
        # Randomly chooses a new location based on the neighboring nodes of the ant.
        # Will not move into a node currently occupied by another ant.
        #

        def moveAnt(solution,ant):


            neighboringNodes = []
            neighboringNodes.extend(solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)].connectedNodeList)

            nodesToRemove = []

            for i in neighboringNodes: # builds a list of neighboring unoccupied nodes

                for g in self.antList: 
                    

                    if(g.xCoord==i.xCoord and g.yCoord==i.yCoord):
                        nodesToRemove.append(i)

            for eachNode in nodesToRemove:
                try:
                    neighboringNodes.remove(eachNode)
                except:
                    pass

            if(neighboringNodes==[]): # surrounded by other ants, so stays in current place
                pass
            else: # goes to random node

                nodeChoice = random.randrange(0,len(neighboringNodes))
                ant.xCoord = neighboringNodes[nodeChoice].xCoord
                ant.yCoord = neighboringNodes[nodeChoice].yCoord
                
        # Initial ant setup

        for ant in self.antList: # places each ant in a random and unique location in the graph

            antLocationUnique = False
            while(antLocationUnique==False):
                randX = random.randrange(0,len(solution.nodeList))
                randY = random.randrange(0,len(solution.nodeList[randX]))
            
                testXCoord = solution.nodeList[randX][randY].xCoord
                testYCoord = solution.nodeList[randX][randY].yCoord

                antConflict = 0
                for eachAnt in self.antList: # makes sure no other ant is currently occupied the chosen space
                                             # otherwise, flags to not end the loop
                    if(eachAnt.xCoord==testXCoord and eachAnt.yCoord == testYCoord):
                        antConflict = 1

                if(antConflict==0):
                    antLocationUnique = True

                    ant.xCoord = testXCoord
                    ant.yCoord = testYCoord
                        

        #
        # SOLUTION MAIN LOOP
        #


        # Delay Values
        # 
        # For delaying output for long enough between cycles to be visible to the human eye
        #
        # NOTICE: I am writing and testing this code on a laptop from 1999, and have less than 256mb of RAM.
        # The delay will likely need to be adjusted for any other computer running this code.
        #
        # SEE GLOBAL VALUES AT TOP FOR FURTHER EXPLANATION (don't change these values, change the one at the top)

        displayDelay = self.displayDelay
        displayCounter = displayDelay





        currentCycle = 1
        cyclesToRun = self.numberOfCycles

        solutionSolved = False
        while(solutionSolved==False and cyclesToRun>0):

            if(displayCounter>=displayDelay):

                displayCounter = 0


                # Display cycle number
                cycleString = "Cycle Number: "+str(currentCycle)
                outputWindow.addstr(0,0,cycleString)

                stringLength = len(str(currentCycle))
                outputWindow.addstr(0,14+stringLength,'     ')

                # Determines whether current solution is a solved state
                if(solution.isSolutionState()==True):
                    solutionSolved = True

                numOfConflictingNodes = determineNumOfConflictingNodes(solution)

                for ant in self.antList:

                    # Determines whether current solution is a solved state
                    if(solution.isSolutionState()==True):
                        solutionSolved = True

                    # Finds the working node
                    currentNode = solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)]

                    # Determines the number of local conflicts (including whether nearby nodes are uncolored or not)
                    numOfLocalConflicts = determineNumOfLocalConflicts(currentNode)

                    # If there are conflicts, swap the color and add pheromones
                    if(numOfLocalConflicts==0):
                        pass
                    else:

                        changeColorOfNode(currentNode)

                    # Process ant movement
                    moveAnt(solution,ant)

                    
                


                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()

                # Iterate cycle counters
                currentCycle += 1
                cyclesToRun -= 1

            else:

                # Iterate display counter
                displayCounter += 1

                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()


        return currentCycle








#
# AntColony Algorithm 2
#
# -Random and pheromone-based movement
# -Random color selection based on local conflicts
#
# -Each node is filled with a given initial amount of pheromones, and pheromone level decays over time.
#

class AntColonyAlg2:


    def __init__(self,solution,numberOfAnts,numberOfCycles,pheromoneStrength,initialPheromoneQuantity,pheromoneDecayRate,displayDelay,randomMoveChance,pheromoneMoveChance): #Initialization of class variables


        # if there are more ants than nodes, set number of ants to number of nodes
        if(numberOfAnts>solution.numOfNodes):
            numberOfAnts = solution.numOfNodes

        self.numberOfAnts = numberOfAnts
        self.numberOfCycles = numberOfCycles

        self.initialPheromoneQuantity = initialPheromoneQuantity
        self.pheromoneStrength = pheromoneStrength
        self.pheromoneDecayRate = pheromoneDecayRate
        
        self.randomMoveChance = 30
        self.pheromoneMoveChance = 70
        
        self.displayDelay = displayDelay
        
        
        
        self.antList = []


        for i in range(0,numberOfAnts): # Sets up initial ant list

            newAnt = Ant()
            self.antList.append(newAnt)



    def solve(self,solution,outputWindow):  # Main Solving Loop


        # ##
        # determineNumOfConflictingNodes
        # ##
        #
        # Returns the number of overall conflicting nodes in the entire problem (not used in this algorithm)
        #

        def determineNumOfConflictingNodes(solution):

            conflictingNum = 0
            for yList in solution.nodeList:

                for eachNode in yList:

                    for i in eachNode.connectedNodeList:

                        if(i.color==eachNode.color):
                            conflictingNum += 1


            return conflictingNum


        # ##
        # determineNumOfLocalConflicts
        # ##
        #
        # Returns the number of local color conflicts around the specificed node
        #

        def determineNumOfLocalConflicts(node):

            localConflicts = 0
            for i in node.connectedNodeList:

                if(i.color==node.color or node.color==0 or i.color==0):

                    localConflicts += 1

            return localConflicts



        # ##
        # changeColorOfNode
        # ##
        #
        # Randomly picks a new color for the specified node
        #


        def changeColorOfNode(node):

            colorDifferent = False
            while(colorDifferent==False):

                newColor = random.randrange(1,4)
                if(node.color==newColor):
                    pass
                else:
                    node.color = newColor
                    colorDifferent = True
        # ##
        # moveAnt
        # ##
        #
        # Randomly chooses a new location based on the neighboring nodes of the ant.
        # Will not move into a node currently occupied by another ant.
        #

        def moveAnt(solution,ant):

            moveDecision = random.randrange(0,self.randomMoveChance+self.pheromoneMoveChance)

            if(moveDecision<=self.randomMoveChance):

                neighboringNodes = []
                neighboringNodes.extend(solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)].connectedNodeList)

                nodesToRemove = []

                for i in neighboringNodes: # builds a list of neighboring unoccupied nodes

                    for g in self.antList: 
                    

                        if(g.xCoord==i.xCoord and g.yCoord==i.yCoord):
                            nodesToRemove.append(i)

                for eachNode in nodesToRemove:
                    try:
                        neighboringNodes.remove(eachNode)
                    except:
                        pass

                if(neighboringNodes==[]): # surrounded by other ants, so stays in current place
                    pass
                else: # goes to random node

                    nodeChoice = random.randrange(0,len(neighboringNodes))
                    ant.xCoord = neighboringNodes[nodeChoice].xCoord
                    ant.yCoord = neighboringNodes[nodeChoice].yCoord
                

            else: # move to neighbor with highest amount of pheromones

                neighboringNodes = []
                neighboringNodes.extend(solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)].connectedNodeList)

                removalList = []
        
                for i in neighboringNodes: # builds a list of neighboring unoccupied nodes

                    for g in self.antList:

                        if(g.xCoord==i.xCoord and g.yCoord==i.yCoord):

                            removalList.append(i)

                for i in removalList:

                    neighboringNodes.remove(i)

                if(neighboringNodes==[]): # surrounded by other ants
                        
                    pass

                else: # goes to node with most pheromones, otherwise picks a random one

                    currentHighestNode = neighboringNodes[random.randrange(0,len(neighboringNodes))]
                    for i in neighboringNodes:
                        
                        if(i.pheromoneConcentration>currentHighestNode.pheromoneConcentration):

                            currentHighestNode = i

                    ant.xCoord = currentHighestNode.xCoord
                    ant.yCoord = currentHighestNode.yCoord

                        



        # Initial ant setup

        for ant in self.antList: # places each ant in a random and unique location in the graph

            antLocationUnique = False
            while(antLocationUnique==False):
                randX = random.randrange(0,len(solution.nodeList))
                randY = random.randrange(0,len(solution.nodeList[randX]))
            
                testXCoord = solution.nodeList[randX][randY].xCoord
                testYCoord = solution.nodeList[randX][randY].yCoord

                antConflict = 0
                for eachAnt in self.antList: # makes sure no other ant is currently occupied the chosen space
                                             # otherwise, flags to not end the loop
                    if(eachAnt.xCoord==testXCoord and eachAnt.yCoord == testYCoord):
                        antConflict = 1

                if(antConflict==0):
                    antLocationUnique = True

                    ant.xCoord = testXCoord
                    ant.yCoord = testYCoord
                        

        for yList in solution.nodeList:

            for eachNode in yList:

                eachNode.pheromoneConcentration = self.initialPheromoneQuantity


        #
        # SOLUTION MAIN LOOP
        #


        # Delay Values
        # 
        # For delaying output for long enough between cycles to be visible to the human eye
        #
        # NOTICE: I am writing and testing this code on a laptop from 1999, and have less than 256mb of RAM.
        # The delay will likely need to be adjusted for any other computer running this code.
        #
        # SEE GLOBAL VALUES AT TOP FOR FURTHER EXPLANATION (don't change these values, change the one at the top)

        displayDelay = self.displayDelay
        displayCounter = displayDelay





        currentCycle = 1
        cyclesToRun = self.numberOfCycles

        solutionSolved = False
        while(solutionSolved==False and cyclesToRun>0):

            if(displayCounter>=displayDelay):

                displayCounter = 0


                # Decay all pheromones by some amount

                for yList in solution.nodeList:

                    for eachNode in yList:

                        eachNode.pheromoneConcentration -= self.pheromoneDecayRate


                # Display cycle number
                cycleString = "Cycle Number: "+str(currentCycle)
                outputWindow.addstr(0,0,cycleString)

                stringLength = len(str(currentCycle))
                outputWindow.addstr(0,14+stringLength,'     ')


                # Determines whether current solution is a solved state
                if(solution.isSolutionState()==True):
                    solutionSolved = True

                numOfConflictingNodes = determineNumOfConflictingNodes(solution)

                for ant in self.antList:

                    # Determines whether current solution is a solved state
                    if(solution.isSolutionState()==True):
                        solutionSolved = True

                    # Finds the working node
                    currentNode = solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)]

                    # Determines the number of local conflicts (including whether nearby nodes are uncolored or not)
                    numOfLocalConflicts = determineNumOfLocalConflicts(currentNode)

                    # If there are conflicts, swap the color and add pheromones
                    if(numOfLocalConflicts==0):
                        pass
                    else:

                        changeColorOfNode(currentNode)
                        
                        # Adds pheromones proportional to the amount of conflicts around the current node
                        currentNode.pheromoneConcentration = numOfLocalConflicts * self.pheromoneStrength

                    # Process ant movement
                    moveAnt(solution,ant)

                    
                


                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()

                # Iterate cycle counters
                currentCycle += 1
                cyclesToRun -= 1

            else:

                # Iterate display counter
                displayCounter += 1

                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()


        return currentCycle








#
# AntColony Algorithm 3
#
# -Random and pheromone-based movement
# -Random color selection based on local conflicts
#
# -Each node is filled with a given initial amount of pheromones, and pheromone level decays over time.
# -In addition, ant movement speeds up decay of pheromone levels in areas with no conflict
# 

class AntColonyAlg3:


    def __init__(self,solution,numberOfAnts,numberOfCycles,pheromoneStrength,initialPheromoneQuantity,pheromoneDecayRate,displayDelay,randomMoveChance,pheromoneMoveChance,movementPheromoneDecay): #Initialization of class variables


        # if there are more ants than nodes, set number of ants to number of nodes
        if(numberOfAnts>solution.numOfNodes):
            numberOfAnts = solution.numOfNodes

        self.numberOfAnts = numberOfAnts
        self.numberOfCycles = numberOfCycles

        self.initialPheromoneQuantity = initialPheromoneQuantity
        self.pheromoneStrength = pheromoneStrength
        self.pheromoneDecayRate = pheromoneDecayRate
        self.movementPheromoneDecay = movementPheromoneDecay
        
        self.randomMoveChance = 30
        self.pheromoneMoveChance = 70
        
        self.displayDelay = displayDelay
        
        
        
        self.antList = []


        for i in range(0,numberOfAnts): # Sets up initial ant list

            newAnt = Ant()
            self.antList.append(newAnt)



    def solve(self,solution,outputWindow):  # Main Solving Loop


        # ##
        # determineNumOfConflictingNodes
        # ##
        #
        # Returns the number of overall conflicting nodes in the entire problem (not used in this algorithm)
        #

        def determineNumOfConflictingNodes(solution):

            conflictingNum = 0
            for yList in solution.nodeList:

                for eachNode in yList:

                    for i in eachNode.connectedNodeList:

                        if(i.color==eachNode.color):
                            conflictingNum += 1


            return conflictingNum


        # ##
        # determineNumOfLocalConflicts
        # ##
        #
        # Returns the number of local color conflicts around the specificed node
        #

        def determineNumOfLocalConflicts(node):

            localConflicts = 0
            for i in node.connectedNodeList:

                if(i.color==node.color or node.color==0 or i.color==0):

                    localConflicts += 1

            return localConflicts



        # ##
        # changeColorOfNode
        # ##
        #
        # Randomly picks a new color for the specified node
        #


        def changeColorOfNode(node):

            colorDifferent = False
            while(colorDifferent==False):

                newColor = random.randrange(1,4)
                if(node.color==newColor):
                    pass
                else:
                    node.color = newColor
                    colorDifferent = True
        # ##
        # moveAnt
        # ##
        #
        # Randomly chooses a new location based on the neighboring nodes of the ant.
        # Will not move into a node currently occupied by another ant.
        #

        def moveAnt(solution,ant):

            moveDecision = random.randrange(0,self.randomMoveChance+self.pheromoneMoveChance)

            if(moveDecision<=self.randomMoveChance):

                neighboringNodes = []
                neighboringNodes.extend(solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)].connectedNodeList)

                nodesToRemove = []

                for i in neighboringNodes: # builds a list of neighboring unoccupied nodes

                    for g in self.antList: 
                    

                        if(g.xCoord==i.xCoord and g.yCoord==i.yCoord):
                            nodesToRemove.append(i)

                for eachNode in nodesToRemove:
                    try:
                        neighboringNodes.remove(eachNode)
                    except:
                        pass

                if(neighboringNodes==[]): # surrounded by other ants, so stays in current place
                    pass
                else: # goes to random node

                    nodeChoice = random.randrange(0,len(neighboringNodes))
                    ant.xCoord = neighboringNodes[nodeChoice].xCoord
                    ant.yCoord = neighboringNodes[nodeChoice].yCoord
                

            else: # move to neighbor with highest amount of pheromones

                neighboringNodes = []
                neighboringNodes.extend(solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)].connectedNodeList)

                removalList = []
        
                for i in neighboringNodes: # builds a list of neighboring unoccupied nodes

                    for g in self.antList:

                        if(g.xCoord==i.xCoord and g.yCoord==i.yCoord):

                            removalList.append(i)

                for i in removalList:

                    neighboringNodes.remove(i)

                if(neighboringNodes==[]): # surrounded by other ants
                        
                    pass

                else: # goes to node with most pheromones, otherwise picks a random one

                    currentHighestNode = neighboringNodes[random.randrange(0,len(neighboringNodes))]
                    for i in neighboringNodes:
                        
                        if(i.pheromoneConcentration>currentHighestNode.pheromoneConcentration):

                            currentHighestNode = i

                    ant.xCoord = currentHighestNode.xCoord
                    ant.yCoord = currentHighestNode.yCoord



        # Initial ant setup

        for ant in self.antList: # places each ant in a random and unique location in the graph

            antLocationUnique = False
            while(antLocationUnique==False):
                randX = random.randrange(0,len(solution.nodeList))
                randY = random.randrange(0,len(solution.nodeList[randX]))
            
                testXCoord = solution.nodeList[randX][randY].xCoord
                testYCoord = solution.nodeList[randX][randY].yCoord

                antConflict = 0
                for eachAnt in self.antList: # makes sure no other ant is currently occupied the chosen space
                                             # otherwise, flags to not end the loop
                    if(eachAnt.xCoord==testXCoord and eachAnt.yCoord == testYCoord):
                        antConflict = 1

                if(antConflict==0):
                    antLocationUnique = True

                    ant.xCoord = testXCoord
                    ant.yCoord = testYCoord
                        

        for yList in solution.nodeList:

            for eachNode in yList:

                eachNode.pheromoneConcentration = self.initialPheromoneQuantity


        #
        # SOLUTION MAIN LOOP
        #


        # Delay Values
        # 
        # For delaying output for long enough between cycles to be visible to the human eye
        #
        # NOTICE: I am writing and testing this code on a laptop from 1999, and have less than 256mb of RAM.
        # The delay will likely need to be adjusted for any other computer running this code.
        #
        # SEE GLOBAL VALUES AT TOP FOR FURTHER EXPLANATION (don't change these values, change the one at the top)

        displayDelay = self.displayDelay
        displayCounter = displayDelay





        currentCycle = 1
        cyclesToRun = self.numberOfCycles

        solutionSolved = False
        while(solutionSolved==False and cyclesToRun>0):

            if(displayCounter>=displayDelay):

                displayCounter = 0


                # Decay all pheromones by some amount

                for yList in solution.nodeList:

                    for eachNode in yList:

                        eachNode.pheromoneConcentration -= self.pheromoneDecayRate


                # Display cycle number
                cycleString = "Cycle Number: "+str(currentCycle)
                outputWindow.addstr(0,0,cycleString)

                stringLength = len(str(currentCycle))
                outputWindow.addstr(0,14+stringLength,'     ')


                # Determines whether current solution is a solved state
                if(solution.isSolutionState()==True):
                    solutionSolved = True

                numOfConflictingNodes = determineNumOfConflictingNodes(solution)

                for ant in self.antList:

                    # Determines whether current solution is a solved state
                    if(solution.isSolutionState()==True):
                        solutionSolved = True

                    # Finds the working node
                    currentNode = solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)]

                    # Determines the number of local conflicts (including whether nearby nodes are uncolored or not)
                    numOfLocalConflicts = determineNumOfLocalConflicts(currentNode)

                    # If there are no conflicts, decay the current node's pheromones by given rate
                    if(numOfLocalConflicts==0):
                        currentNode.pheromoneConcentration -= self.movementPheromoneDecay
                    else:

                        changeColorOfNode(currentNode)
                        
                        # Adds pheromones proportional to the amount of conflicts around the current node
                        currentNode.pheromoneConcentration = numOfLocalConflicts * self.pheromoneStrength

                    # Process ant movement
                    moveAnt(solution,ant)

                    
                


                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()

                # Iterate cycle counters
                currentCycle += 1
                cyclesToRun -= 1

            else:

                # Iterate display counter
                displayCounter += 1

                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()




        return currentCycle












#
# AntColony Algorithm 4
#
# -Random and pheromone-based movement
#
# -Each node is filled with a given initial amount of pheromones, and pheromone level decays over time.
# -In addition, ant movement speeds up decay of pheromone levels in areas with no conflict
# 

class AntColonyAlg4:


    def __init__(self,solution,numberOfAnts,numberOfCycles,pheromoneStrength,initialPheromoneQuantity,pheromoneDecayRate,displayDelay,randomMoveChance,pheromoneMoveChance,movementPheromoneDecay): #Initialization of class variables


        # if there are more ants than nodes, set number of ants to number of nodes
        if(numberOfAnts>solution.numOfNodes):
            numberOfAnts = solution.numOfNodes

        self.numberOfAnts = numberOfAnts
        self.numberOfCycles = numberOfCycles

        self.initialPheromoneQuantity = initialPheromoneQuantity
        self.pheromoneStrength = pheromoneStrength
        self.pheromoneDecayRate = pheromoneDecayRate
        self.movementPheromoneDecay = movementPheromoneDecay
        
        self.randomMoveChance = 30
        self.pheromoneMoveChance = 70
        
        self.displayDelay = displayDelay
        
        
        
        self.antList = []


        for i in range(0,numberOfAnts): # Sets up initial ant list

            newAnt = Ant()
            self.antList.append(newAnt)



    def solve(self,solution,outputWindow):  # Main Solving Loop


        # ##
        # determineNumOfConflictingNodes
        # ##
        #
        # Returns the number of overall conflicting nodes in the entire problem (not used in this algorithm)
        #

        def determineNumOfConflictingNodes(solution):

            conflictingNum = 0
            for yList in solution.nodeList:

                for eachNode in yList:

                    for i in eachNode.connectedNodeList:

                        if(i.color==eachNode.color):
                            conflictingNum += 1


            return conflictingNum


        # ##
        # determineNumOfLocalConflicts
        # ##
        #
        # Returns the number of local color conflicts around the specificed node
        #

        def determineNumOfLocalConflicts(node):

            localConflicts = 0
            for i in node.connectedNodeList:

                if(i.color==node.color or node.color==0 or i.color==0):

                    localConflicts += 1

            return localConflicts

        
        # ##
        # changeColorOfNodeRandom
        # ##
        #
        # Randomly changes the color of the current node
        
        def changeColorOfNodeRandom(node):

            colorDifferent = False
            while(colorDifferent==False):

                newColor = random.randrange(1,4)
                if(node.color==newColor):
                    pass
                else:
                    node.color = newColor
                    colorDifferent = True
        

        # ##
        # changeColorOfNode
        # ##
        #
        # Changes the color of the current node depending on what would locally be best suited


        def changeColorOfNode(node):

            acceptableColor = False
            while(acceptableColor==False):

                neighboringNodes = []
                neighboringNodes.extend(node.connectedNodeList)

                possibleColors = [1,2,3]

                for i in neighboringNodes:

                    for g in possibleColors:

                        if(i.color==g):

                            possibleColors.remove(g)

                # If surrounded by all possible colors, just pick randomly because no local best is possible
                if(possibleColors==[]):

                    changeColorOfNodeRandom(node)
                    acceptableColor = True

                else:

                    # picks randomly from the locally acceptable colors 
                    node.color = possibleColors[random.randrange(0,len(possibleColors))]
                    acceptableColor = True


            
        # ##
        # moveAnt
        # ##
        #
        # Randomly chooses a new location based on the neighboring nodes of the ant.
        # Will not move into a node currently occupied by another ant.
        #

        def moveAnt(solution,ant):

            moveDecision = random.randrange(0,self.randomMoveChance+self.pheromoneMoveChance)

            if(moveDecision<=self.randomMoveChance):

                neighboringNodes = []
                neighboringNodes.extend(solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)].connectedNodeList)

                nodesToRemove = []

                for i in neighboringNodes: # builds a list of neighboring unoccupied nodes

                    for g in self.antList: 
                    

                        if(g.xCoord==i.xCoord and g.yCoord==i.yCoord):
                            nodesToRemove.append(i)

                for eachNode in nodesToRemove:
                    try:
                        neighboringNodes.remove(eachNode)
                    except:
                        pass

                if(neighboringNodes==[]): # surrounded by other ants, so stays in current place
                    pass
                else: # goes to random node

                    nodeChoice = random.randrange(0,len(neighboringNodes))
                    ant.xCoord = neighboringNodes[nodeChoice].xCoord
                    ant.yCoord = neighboringNodes[nodeChoice].yCoord
                

            else: # move to neighbor with highest amount of pheromones

                neighboringNodes = []
                neighboringNodes.extend(solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)].connectedNodeList)

                removalList = []
        
                for i in neighboringNodes: # builds a list of neighboring unoccupied nodes

                    for g in self.antList:

                        if(g.xCoord==i.xCoord and g.yCoord==i.yCoord):

                            removalList.append(i)

                for i in removalList:

                    neighboringNodes.remove(i)

                if(neighboringNodes==[]): # surrounded by other ants
                        
                    pass

                else: # goes to node with most pheromones, otherwise picks a random one

                    currentHighestNode = neighboringNodes[random.randrange(0,len(neighboringNodes))]
                    for i in neighboringNodes:
                        
                        if(i.pheromoneConcentration>currentHighestNode.pheromoneConcentration):

                            currentHighestNode = i

                    ant.xCoord = currentHighestNode.xCoord
                    ant.yCoord = currentHighestNode.yCoord



        # Initial ant setup

        for ant in self.antList: # places each ant in a random and unique location in the graph

            antLocationUnique = False
            while(antLocationUnique==False):
                randX = random.randrange(0,len(solution.nodeList))
                randY = random.randrange(0,len(solution.nodeList[randX]))
            
                testXCoord = solution.nodeList[randX][randY].xCoord
                testYCoord = solution.nodeList[randX][randY].yCoord

                antConflict = 0
                for eachAnt in self.antList: # makes sure no other ant is currently occupied the chosen space
                                             # otherwise, flags to not end the loop
                    if(eachAnt.xCoord==testXCoord and eachAnt.yCoord == testYCoord):
                        antConflict = 1

                if(antConflict==0):
                    antLocationUnique = True

                    ant.xCoord = testXCoord
                    ant.yCoord = testYCoord
                        

        for yList in solution.nodeList:

            for eachNode in yList:

                eachNode.pheromoneConcentration = self.initialPheromoneQuantity


        #
        # SOLUTION MAIN LOOP
        #


        # Delay Values
        # 
        # For delaying output for long enough between cycles to be visible to the human eye
        #
        # NOTICE: I am writing and testing this code on a laptop from 1999, and have less than 256mb of RAM.
        # The delay will likely need to be adjusted for any other computer running this code.
        #
        # SEE GLOBAL VALUES AT TOP FOR FURTHER EXPLANATION (don't change these values, change the one at the top)

        displayDelay = self.displayDelay
        displayCounter = displayDelay





        currentCycle = 1
        cyclesToRun = self.numberOfCycles

        solutionSolved = False
        while(solutionSolved==False and cyclesToRun>0):

            if(displayCounter>=displayDelay):

                displayCounter = 0


                # Decay all pheromones by some amount

                for yList in solution.nodeList:

                    for eachNode in yList:

                        eachNode.pheromoneConcentration -= self.pheromoneDecayRate


                # Display cycle number
                cycleString = "Cycle Number: "+str(currentCycle)
                outputWindow.addstr(0,0,cycleString)

                stringLength = len(str(currentCycle))
                outputWindow.addstr(0,14+stringLength,'     ')


                # Determines whether current solution is a solved state
                if(solution.isSolutionState()==True):
                    solutionSolved = True

                numOfConflictingNodes = determineNumOfConflictingNodes(solution)

                for ant in self.antList:

                    # Determines whether current solution is a solved state
                    if(solution.isSolutionState()==True):
                        solutionSolved = True

                    # Finds the working node
                    currentNode = solution.nodeList[int(ant.xCoord/6)][int(ant.yCoord/6)]

                    # Determines the number of local conflicts (including whether nearby nodes are uncolored or not)
                    numOfLocalConflicts = determineNumOfLocalConflicts(currentNode)

                    # If there are no conflicts, decay the current node's pheromones by given rate
                    if(numOfLocalConflicts==0):
                        currentNode.pheromoneConcentration -= self.movementPheromoneDecay
                    else:

                        changeColorOfNode(currentNode)
                        
                        # Adds pheromones proportional to the amount of conflicts around the current node
                        currentNode.pheromoneConcentration = numOfLocalConflicts * self.pheromoneStrength

                    # Process ant movement
                    moveAnt(solution,ant)

                    
                


                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()

                # Iterate cycle counters
                currentCycle += 1
                cyclesToRun -= 1

            else:

                # Iterate display counter
                displayCounter += 1

                # Display output
                solution.display(outputWindow)
                solution.drawAnts(outputWindow,self.antList)
                outputWindow.refresh()




        return currentCycle





# Individual node for use by GraphSolution class

class GraphNode:

    def __init__(self,xCoord):

        self.xCoord = xCoord

        self.yCoord = 0

        self.color = 0#random.randrange(1,4)
        self.icon = '#'

        self.removalFlag = False

        self.connectedNodeList = []

        self.pheromoneConcentration = 0



#
# GraphSolution Class
#
# ##
# Parameters:
# ##
# 
# - numOfNodes: number of GraphNodes to generate in the solution set
# - window: curses window to output to

class GraphSolution:



    def __init__(self,numOfNodes,window):

        #
        # Class Properties
        #


        self.nodeList = []

        self.numOfNodes = numOfNodes
        self.lastTier = 0


        #
        # Solution Setup
        #

        def connectNodes(node1,node2):

            node1.connectedNodeList.append(node2)
            node2.connectedNodeList.append(node1)
        

        currentTier = 0
        sameTierCounter = 1
        nodeCounter = 0

        currentTierList = []

        for i in range(0,self.numOfNodes):

            #newNode = GraphNode(currentTier)
            #if(lastNode!=None):
                #connectNodes(newNode,lastNode)
            
            #newNode = GraphNode(currentTier)
            #currentTierList.append(newNode)

        
            tierIterChoice = random.randrange(0,100)
            if((tierIterChoice>70 or sameTierCounter>=MAX_Y_VALUE_OF_GRAPH_NODE) and sameTierCounter>1):
                currentTier += 6
                sameTierCounter = 1
                self.nodeList.append(currentTierList)
                currentTierList = []
            else:
                sameTierCounter += 1
            
            newNode = GraphNode(currentTier)
            currentTierList.append(newNode)


        self.nodeList.append(currentTierList)
        self.lastTier = int((currentTier/6))#+1)
        # Seperates out each node on the same X coordinate
        # to different Y coordinates

        checkTier = -1
        checkTierCounter = 0

        for g in self.nodeList:

            for node in g:
    
                if(checkTier!=node.xCoord):

                    checkTier = node.xCoord
                    checkTierCounter = 0

                else:

                    checkTierCounter += 6

                node.yCoord = checkTierCounter
                


        for k in self.nodeList:

            for node in k:


                node.xCoord += 3
                node.yCoord += 3



        # Connect nodes to each other
        #


        nodelistCounter = 1

        for j in self.nodeList:
    
            for node in j:

                if(nodelistCounter>=len(self.nodeList)):

                    pass

                else:

                    for otherNode in self.nodeList[nodelistCounter]:

                        if(node.yCoord==otherNode.yCoord):
                
                            connectNodes(node,otherNode)


                for nodeOnSameY in j:

                    if(nodeOnSameY.yCoord+6==node.yCoord):

                        connectNodes(nodeOnSameY,node)



            nodelistCounter += 1






    def display(self,window):

        # An insane mess, but it works.
        #
        # Draws connections between each node and it's immediate neighbors in the 4 cardinal directions.
        # Originally was intended in support all sorts of more nonlinear connections, but for the sake of
        # simplicity, this was removed. There's still some elements of that left in however.

        def drawConnectingLines(node1,node2):

            def drawUntilTouching(node1,node2,yOffset,xOffset,icon,directionCode,diagonalCode): 

                notTouching = True

                xIncrease = 0
                yIncrease = 0
                diagonalSwitchCounter = 0

                while(notTouching==True):

                    #if(node1.yCoord+yOffset+yIncrease==node2.yCoord+1 and node1.xCoord+xOffset+xIncrease==node2.xCoord+1):

                        #notTouching = False

                    window.addch(node1.yCoord+yOffset+yIncrease,node1.xCoord+xOffset+xIncrease,icon)
                    
                    if(directionCode==0):


                        if(node1.yCoord+yOffset+yIncrease==node2.yCoord+3 and diagonalCode != 1 or node1.yCoord+yOffset+yIncrease==node2.yCoord-1 or node1.yCoord+yOffset+yIncrease==node2.yCoord+1):

                            if(diagonalCode==0):
                                notTouching = False
                            elif(diagonalCode==1 and diagonalSwitchCounter>0):
                                notTouching = False
                            else:
                                diagonalSwitchCounter += 1
                                directionCode = 1
                                icon = '-'
                                if(xOffset<0):
                                    xIncrease -= 1
                                else:
                                    xIncrease += 1

                        else:
                            
                            if(node1.yCoord+yOffset+yIncrease-1==node2.yCoord+1 and diagonalCode==1):

                                icon = '/'

                            if(yOffset<0):
                                yIncrease -= 1
                            else:
                                yIncrease += 1

                    elif(directionCode==1):

                        if(node1.xCoord+xOffset+xIncrease==node2.xCoord-1 or node1.xCoord+xOffset+xIncrease==node2.xCoord+3 and diagonalCode != 1 or node1.xCoord+xOffset+xIncrease==node2.xCoord+1):


                            if(diagonalCode==0):
                                notTouching = False
                            elif(diagonalCode==1 and diagonalSwitchCounter>0):
                                notTouching = False
                            else:
                                diagonalSwitchCounter += 1
                                directionCode = 0
                                icon = '|'
                                if(yOffset<0):
                                    yIncrease -= 1
                                else:
                                    yIncrease += 1

                        else:
                            
                            if(xOffset<0):
                                xIncrease -= 1
                            else:
                                xIncrease += 1



            if(node1.xCoord==node2.xCoord):

                if(node1.yCoord>node2.yCoord):

                    drawUntilTouching(node1,node2,-1,1,'|',0,0)    


                elif(node1.yCoord<node2.yCoord):

                    drawUntilTouching(node1,node2,3,1,'|',0,0)

                else:

                    window.addstr(20,21,'error in same X')

            else:

                if(node1.xCoord<node2.xCoord):

                    if(node1.yCoord==node2.yCoord):

                        drawUntilTouching(node1,node2,1,3,'-',1,0)

                    elif(node1.yCoord<node2.yCoord):

                       # window.addstr(0,0,'IT HAPPENED #1')
                        pass# drawUntilTouching(node1,node2,1,-2,'|',0,1)

                    elif(node1.yCoord>node2.yCoord):

                        window.addch(node1.yCoord+1,node1.xCoord+3,'-')
                        window.addch(node1.yCoord+1,node1.xCoord+4,'/')
                        window.addch(node1.yCoord,node1.xCoord+4,'|')
                        drawUntilTouching(node1,node2,-1,4,'|',0,1)

                elif(node1.xCoord>node2.xCoord):

                    if(node1.yCoord==node2.yCoord):

                        drawUntilTouching(node1,node2,1,-1,'-',1,0)

                    elif(node1.yCoord<node2.yCoord):

                        pass #   window.addstr(0,1,'IT HAPPENED #2')

                    elif(note1.yCoord>node2.yCoord):

                        pass#  window.addstr(0,2,'IT HAPPENED #3')


                else:

                    window.addstr(20,20,'error in not X')



        for nodeList in self.nodeList:

            for node in nodeList:

            # draw 9 characters in a square to represent
            # each node
            
                window.attron(curses.color_pair(node.color))
                window.addch(node.yCoord,node.xCoord,node.icon)
                window.addch(node.yCoord+1,node.xCoord,node.icon)
                window.addch(node.yCoord,node.xCoord+1,node.icon)
                window.addch(node.yCoord+1,node.xCoord+1,node.icon)
                window.addch(node.yCoord+2,node.xCoord,node.icon)
                window.addch(node.yCoord+2,node.xCoord+1,node.icon)
                window.addch(node.yCoord+2,node.xCoord+2,node.icon)
                window.addch(node.yCoord+1,node.xCoord+2,node.icon)
                window.addch(node.yCoord,node.xCoord+2,node.icon)
                window.attroff(curses.color_pair(node.color))

                for i in node.connectedNodeList:

                    drawConnectingLines(node,i)
            

        ## INFO OUTPUTS ##

        # Number of Nodes
        nodeCounter = 0
        for xList in self.nodeList:
            for yList in xList:
                nodeCounter += 1
        numOfNodesString = "Number of Nodes: "+str(nodeCounter)
        window.addstr(40,0,numOfNodesString)

    


        ## DEBUG OUTPUTS ##

        # window.addstr(20,20,str(self.nodeList[0].xCoord))


    def drawAnts(self,window,antList):

        for i in antList:

            window.attron(curses.color_pair(4))
            window.addch(i.yCoord+1,i.xCoord+1,'*')
            window.attroff(curses.color_pair(4))


    def isSolutionState(self):

        solutionFailed = 0
        for eachY in self.nodeList:

            for eachNode in eachY:

                for i in eachNode.connectedNodeList:

                    if(i.color==eachNode.color or i.color==0):

                        solutionFailed = 1
                        break

        if(solutionFailed==1):

            return False

        else:

            return True



    def resetSolution(self):

        for yList in self.nodeList:

            for eachNode in yList:

                eachNode.color = 0
                eachNode.pheromoneConcentration = 0




# ##
# testAlg#
# ##
#
# These functions all do a single test of the given algorithm, with a provided graph and
# over the amount of trials inputted. They return the average number of cycles needed to find a solution.


    
def testAlg1(outputWindow,numOfTests,solution):

    resultList = []
    for i in range(0,numOfTests):

        solution.resetSolution()

        newAntColonyAlg1 = AntColonyAlg1(solution,NUM_OF_ANTS,NUM_OF_CYCLES,DISPLAY_DELAY)

        currentResult = newAntColonyAlg1.solve(solution,outputWindow)
        resultList.append(currentResult)


    resultSum = 0
    for i in resultList:

        resultSum += i

    outputWindow.clear()
    resultSum = resultSum/len(resultList)
    outputWindow.addstr(2,3,"Current trial's average cycles of Algorithm 1 over the same graph:")
    outputWindow.addstr(3,3,str(resultSum))
    outputWindow.addstr(5,3,"PRESS ANY KEY TO CONTINUE")

    outputWindow.getch()
    outputWindow.clear()

    return resultSum

def testAlg2(outputWindow,numOfTests,solution):

    resultList = []
    for i in range(0,numOfTests):

        solution.resetSolution()

        newAntColonyAlg2 = AntColonyAlg2(solution,NUM_OF_ANTS,NUM_OF_CYCLES,PHEROMONE_STRENGTH,INITIAL_PHEROMONE_QUANTITY,PHEROMONE_DECAY_RATE,DISPLAY_DELAY,RANDOM_MOVE_CHANCE,PHEROMONE_MOVE_CHANCE)

        

        currentResult = newAntColonyAlg2.solve(solution,outputWindow)
        resultList.append(currentResult)


    resultSum = 0
    for i in resultList:

        resultSum += i

    outputWindow.clear()
    resultSum = resultSum/len(resultList)
    outputWindow.addstr(2,3,"Current trial's average cycles of Algorithm 2 over the same graph:")
    outputWindow.addstr(3,3,str(resultSum))
    outputWindow.addstr(5,3,"PRESS ANY KEY TO CONTINUE")

    outputWindow.getch()
    outputWindow.clear()

    return resultSum

def testAlg3(outputWindow,numOfTests,solution):

    resultList = []
    for i in range(0,numOfTests):

        solution.resetSolution()

        newAntColonyAlg3 = AntColonyAlg3(solution,NUM_OF_ANTS,NUM_OF_CYCLES,PHEROMONE_STRENGTH,INITIAL_PHEROMONE_QUANTITY,PHEROMONE_DECAY_RATE,DISPLAY_DELAY,RANDOM_MOVE_CHANCE,PHEROMONE_MOVE_CHANCE,MOVEMENT_PHEROMONE_DECAY)

        
        
        currentResult = newAntColonyAlg3.solve(solution,outputWindow)
        resultList.append(currentResult)


    resultSum = 0
    for i in resultList:

        resultSum += i

    outputWindow.clear()
    resultSum = resultSum/len(resultList)
    outputWindow.addstr(2,3,"Current trial's average cycles of Algorithm 3 over the same graph:")
    outputWindow.addstr(3,3,str(resultSum))
    outputWindow.addstr(5,3,"PRESS ANY KEY TO CONTINUE")

    outputWindow.getch()
    outputWindow.clear()

    return resultSum

def testAlg4(outputWindow,numOfTests,solution):

    resultList = []
    for i in range(0,numOfTests):

        solution.resetSolution()

        newAntColonyAlg4 = AntColonyAlg4(solution,NUM_OF_ANTS,NUM_OF_CYCLES,PHEROMONE_STRENGTH,INITIAL_PHEROMONE_QUANTITY,PHEROMONE_DECAY_RATE,DISPLAY_DELAY,RANDOM_MOVE_CHANCE,PHEROMONE_MOVE_CHANCE,MOVEMENT_PHEROMONE_DECAY)

        
        
        currentResult = newAntColonyAlg4.solve(solution,outputWindow)
        resultList.append(currentResult)


    resultSum = 0
    for i in resultList:

        resultSum += i

    outputWindow.clear()
    resultSum = resultSum/len(resultList)
    outputWindow.addstr(2,3,"Current trial's average cycles of Algorithm 4 over the same graph:")
    outputWindow.addstr(3,3,str(resultSum))
    outputWindow.addstr(5,3,"PRESS ANY KEY TO CONTINUE")

    outputWindow.getch()
    outputWindow.clear()

    return resultSum

# ##
# comparativeTrialsOfAlgorithms
# ##
#
# Runs each algorithm against each other in several tests
#
# Each algorithm is tested 100 times on 3 different graphs, and the results
# are averaged together.
#



def comparativeTrialsOfAlgorithms(outputWindow):

    outputWindow.addstr(3,3,"Comparative Trials")
    outputWindow.addstr(4,3,"------------------")
    outputWindow.addstr(5,3,"These tests will be measuring the efficiency of Algorithm 1, Algorithm 2, and Algorithm 3")
    outputWindow.addstr(6,3,"on a graph whose layout will change between each trial. Each algorithm will be put through")
    outputWindow.addstr(7,3,"three trials of 100 tests each. The details of the algorithms are below.")

    outputWindow.addstr(10,3,"Algorithm 1")
    outputWindow.addstr(11,3,"-----------")
    outputWindow.addstr(12,3,"* Random movement of ants")
    outputWindow.addstr(13,3,"* New color of each node is chosen randomly")
    outputWindow.addstr(14,3,"* Aware of the amount of local conflicts of current node")

    outputWindow.addstr(16,3,"Algorithm 2")
    outputWindow.addstr(17,3,"-----------")
    outputWindow.addstr(18,3,"* Pheromone-based and random movement of ants")
    outputWindow.addstr(19,3,"* Pheromones are generated on the current node whenever a color is flipped")
    outputWindow.addstr(20,3,"* New color of each node is chosen randomly")
    outputWindow.addstr(21,3,"* Aware of the amount of local conflicts of current node")
    outputWindow.addstr(22,3,"* Each node is given an initial pheromone level")
    outputWindow.addstr(23,3,"* All pheromone levels decay over time")

    outputWindow.addstr(25,3,"Algorithm 3")
    outputWindow.addstr(26,3,"-----------")
    outputWindow.addstr(27,3,"* Pheromone-based and random movement of ants")
    outputWindow.addstr(28,3,"* Pheromones are generated on the current node whenever a color is flipped")
    outputWindow.addstr(29,3,"* Pheromones are directly decayed each time an ant moves over a locally optimal node.")
    outputWindow.addstr(30,3,"* New color of each node is chosen randomly")
    outputWindow.addstr(31,3,"* Aware of the amount of local conflicts of current node")
    outputWindow.addstr(32,3,"* Each node is given an initial pheromone level")
    outputWindow.addstr(33,3,"* All pheromone levels decay over time")

    outputWindow.addstr(35,3,"Algorithm 4")
    outputWindow.addstr(36,3,"-----------")
    outputWindow.addstr(37,3,"* Pheromone-based and random movement of ants")
    outputWindow.addstr(38,3,"* Pheromones are generated on the current node whenever a color is flipped")
    outputWindow.addstr(39,3,"* Pheromones are directly decayed each time an ant moves over a locally optimal node.")
    outputWindow.addstr(40,3,"* New color of each node is chosen by determing the locally best color")
    outputWindow.addstr(41,3,"* Aware of the amount of local conflicts of current node")
    outputWindow.addstr(42,3,"* Each node is given an initial pheromone level")
    outputWindow.addstr(43,3,"* All pheromone levels decay over time")

    outputWindow.addstr(46,3,"PRESS ANY KEY TO BEGIN THE TESTS")

    outputWindow.getch()




    graphSolution1 = GraphSolution(NUM_OF_NODES_IN_GRAPH,stdscr)
        
    outputWindow.addstr(10,10,"TRIAL 1 OF ALGORITHM 1")
    outputWindow.clear()
    outputWindow.refresh()
    Alg1_Trial1 = testAlg1(stdscr,100,graphSolution1)
    
    outputWindow.addstr(10,10,"TRIAL 1 OF ALGORITHM 2")
    outputWindow.clear()
    outputWindow.refresh()
    Alg2_Trial1 = testAlg2(stdscr,100,graphSolution1)
    
    outputWindow.addstr(10,10,"TRIAL 1 OF ALGORITHM 3")
    outputWindow.clear()
    outputWindow.refresh()
    Alg3_Trial1 = testAlg3(stdscr,100,graphSolution1)
    
    outputWindow.addstr(10,10,"TRIAL 1 OF ALGORITHM 4")
    outputWindow.clear()
    outputWindow.refresh()
    Alg4_Trial1 = testAlg4(stdscr,100,graphSolution1)
    

    
    graphSolution2 = GraphSolution(NUM_OF_NODES_IN_GRAPH,stdscr)
        
    outputWindow.addstr(10,10,"TRIAL 2 OF ALGORITHM 1")
    outputWindow.clear()
    outputWindow.refresh()
    Alg1_Trial2 = testAlg1(stdscr,100,graphSolution2)
    
    outputWindow.addstr(10,10,"TRIAL 2 OF ALGORITHM 2")
    outputWindow.clear()
    outputWindow.refresh()
    Alg2_Trial2 = testAlg2(stdscr,100,graphSolution2)
    
    outputWindow.addstr(10,10,"TRIAL 2 OF ALGORITHM 3")
    outputWindow.clear()
    outputWindow.refresh()
    Alg3_Trial2 = testAlg3(stdscr,100,graphSolution2)
    
    outputWindow.addstr(10,10,"TRIAL 2 OF ALGORITHM 4")
    outputWindow.clear()
    outputWindow.refresh()
    Alg4_Trial2 = testAlg4(stdscr,100,graphSolution2)
    

 
    graphSolution3 = GraphSolution(NUM_OF_NODES_IN_GRAPH,stdscr)
        
    outputWindow.addstr(10,10,"TRIAL 3 OF ALGORITHM 1")
    outputWindow.clear()
    outputWindow.refresh()
    Alg1_Trial3 = testAlg1(stdscr,100,graphSolution3)
    
    outputWindow.addstr(10,10,"TRIAL 3 OF ALGORITHM 2")
    outputWindow.clear()
    outputWindow.refresh()
    Alg2_Trial3 = testAlg2(stdscr,100,graphSolution3)
    
    outputWindow.addstr(10,10,"TRIAL 3 OF ALGORITHM 3")
    outputWindow.clear()
    outputWindow.refresh()
    Alg3_Trial3 = testAlg3(stdscr,100,graphSolution3)
    
    outputWindow.addstr(10,10,"TRIAL 3 OF ALGORITHM 4")
    outputWindow.clear()
    outputWindow.refresh()
    Alg4_Trial3 = testAlg4(stdscr,100,graphSolution3)
    


    outputWindow.clear()
    outputWindow.refresh()

    outputWindow.addstr(3,3,"FINAL RESULTS")
    outputWindow.addstr(4,3,"-------------")

    outputWindow.addstr(6,3,"Algorithm 1")
    outputWindow.addstr(7,3,"-----------")
    outputWindow.addstr(8,3,"Trial 1: ")
    outputWindow.addstr(8,13,str(Alg1_Trial1))
    outputWindow.addstr(9,3,"Trial 2: ")
    outputWindow.addstr(9,13,str(Alg1_Trial2))
    outputWindow.addstr(10,3,"Trial 3: ")
    outputWindow.addstr(10,13,str(Alg1_Trial3))
    outputWindow.addstr(12,3,"Average: ")
    outputWindow.addstr(12,13,str(round(((Alg1_Trial1+Alg1_Trial2+Alg1_Trial3)/3),2)))


    outputWindow.addstr(14,3,"Algorithm 2")
    outputWindow.addstr(15,3,"-----------")
    outputWindow.addstr(16,3,"Trial 1: ")
    outputWindow.addstr(16,13,str(Alg2_Trial1))
    outputWindow.addstr(17,3,"Trial 2: ")
    outputWindow.addstr(17,13,str(Alg2_Trial2))
    outputWindow.addstr(18,3,"Trial 3: ")
    outputWindow.addstr(18,13,str(Alg2_Trial3))
    outputWindow.addstr(20,3,"Average: ")
    outputWindow.addstr(20,13,str(round(((Alg2_Trial1+Alg2_Trial2+Alg2_Trial3)/3),2)))


    outputWindow.addstr(22,3,"Algorithm 3")
    outputWindow.addstr(23,3,"-----------")
    outputWindow.addstr(24,3,"Trial 1: ")
    outputWindow.addstr(24,13,str(Alg3_Trial1))
    outputWindow.addstr(25,3,"Trial 2: ")
    outputWindow.addstr(25,13,str(Alg3_Trial2))
    outputWindow.addstr(26,3,"Trial 3: ")
    outputWindow.addstr(26,13,str(Alg3_Trial3))
    outputWindow.addstr(28,3,"Average: ")
    outputWindow.addstr(28,13,str(round(((Alg3_Trial1+Alg3_Trial2+Alg3_Trial3)/3),2)))


    outputWindow.addstr(30,3,"Algorithm 4")
    outputWindow.addstr(31,3,"-----------")
    outputWindow.addstr(32,3,"Trial 1: ")
    outputWindow.addstr(32,13,str(Alg4_Trial1))
    outputWindow.addstr(33,3,"Trial 2: ")
    outputWindow.addstr(33,13,str(Alg4_Trial2))
    outputWindow.addstr(34,3,"Trial 3: ")
    outputWindow.addstr(34,13,str(Alg4_Trial3))
    outputWindow.addstr(36,3,"Average: ")
    outputWindow.addstr(36,13,str(round(((Alg4_Trial1+Alg4_Trial2+Alg4_Trial3)/3),2)))

    stdscr.getch()
    stdscr.clear()
    stdscr.refresh()


def printMainMenu(outputWindow):

    outputWindow.addstr(3,3,"Artificial Intelligence Research Project")
    outputWindow.addstr(4,3,"----------------------------------------")
    outputWindow.addstr(6,3,"By James Clisham")
    outputWindow.addstr(10,3,"Enter one of the following keys to make a selection: ")

    outputWindow.addstr(12,5,"1 - Run a test of a single algorithm")
    outputWindow.addstr(13,5,"2 - Comparative Analysis of all algorithms")
    outputWindow.addstr(14,5,"3 - Exit the program")



def singleAlgTestMenu(outputWindow):


    outputWindow.addstr(38,3,"Enter one of the following keys to make a selection: ")
    outputWindow.addstr(40,3,"1 - Test Algorithm 1")
    outputWindow.addstr(41,3,"2 - Test Algorithm 2")
    outputWindow.addstr(42,3,"3 - Test Algorithm 3")
    outputWindow.addstr(43,3,"4 - Test Algorithm 4")
    outputWindow.addstr(44,3,"5 - Return to Main Menu")


    outputWindow.addstr(3,3,"Algorithm 1")
    outputWindow.addstr(4,3,"-----------")
    outputWindow.addstr(5,3,"* Random movement of ants")
    outputWindow.addstr(6,3,"* New color of each node is chosen randomly")
    outputWindow.addstr(7,3,"* Aware of the amount of local conflicts of current node")

    outputWindow.addstr(9,3,"Algorithm 2")
    outputWindow.addstr(10,3,"-----------")
    outputWindow.addstr(11,3,"* Pheromone-based and random movement of ants")
    outputWindow.addstr(12,3,"* Pheromones are generated on the current node whenever a color is flipped")
    outputWindow.addstr(13,3,"* New color of each node is chosen randomly")
    outputWindow.addstr(14,3,"* Aware of the amount of local conflicts of current node")
    outputWindow.addstr(15,3,"* Each node is given an initial pheromone level")
    outputWindow.addstr(16,3,"* All pheromone levels decay over time")

    outputWindow.addstr(18,3,"Algorithm 3")
    outputWindow.addstr(19,3,"-----------")
    outputWindow.addstr(20,3,"* Pheromone-based and random movement of ants")
    outputWindow.addstr(21,3,"* Pheromones are generated on the current node whenever a color is flipped")
    outputWindow.addstr(22,3,"* Pheromones are directly decayed each time an ant moves over a locally optimal node.")
    outputWindow.addstr(23,3,"* New color of each node is chosen randomly")
    outputWindow.addstr(24,3,"* Aware of the amount of local conflicts of current node")
    outputWindow.addstr(25,3,"* Each node is given an initial pheromone level")
    outputWindow.addstr(26,3,"* All pheromone levels decay over time")

    outputWindow.addstr(28,3,"Algorithm 4")
    outputWindow.addstr(29,3,"-----------")
    outputWindow.addstr(30,3,"* Pheromone-based and random movement of ants")
    outputWindow.addstr(31,3,"* Pheromones are generated on the current node whenever a color is flipped")
    outputWindow.addstr(32,3,"* Pheromones are directly decayed each time an ant moves over a locally optimal node.")
    outputWindow.addstr(33,3,"* New color of each node is chosen by determing the locally best color")
    outputWindow.addstr(34,3,"* Aware of the amount of local conflicts of current node")
    outputWindow.addstr(35,3,"* Each node is given an initial pheromone level")
    outputWindow.addstr(36,3,"* All pheromone levels decay over time")
 


#
#
# MAIN LOOP
# 
#

# only executes if this file is being run itself, rather than being used as a library
if(__name__ == "__main__"):

    # curses initialization
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.start_color()
    curses.curs_set(0)

    # color initialization
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_BLUE,curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_MAGENTA,curses.COLOR_BLACK)

    # main while loop, ensures input is continually captured in main screen until correct input is found
    mainLoopRunning = True
    while(mainLoopRunning):

        # clears and refreshes the screen
        stdscr.clear()
        stdscr.refresh()

        # outputs the main menu text
        printMainMenu(stdscr)

        # waits for user input and captures whatever key is pressed
        userInput = stdscr.getch()

        if(userInput==ord('1')):


            # ensures that input is continually captured until correct input is found
            inSingleTestMenu = True
            while(inSingleTestMenu):

                # creates a new graph for whichever algorithm is chosen      
                singleGraphSolution = GraphSolution(NUM_OF_NODES_IN_GRAPH,stdscr)

                stdscr.clear()
                stdscr.refresh()

                # outputs the single test menu text
                singleAlgTestMenu(stdscr)

                # waits for user input, captures keys, etc
                userInput = stdscr.getch()

                # statements handle what input is pressed
                if(userInput==ord('1')):

                    stdscr.clear()
                    stdscr.refresh()

                    testAlg1(stdscr,1,singleGraphSolution)

                elif(userInput==ord('2')):

                    stdscr.clear()
                    stdscr.refresh()

                    testAlg2(stdscr,1,singleGraphSolution)

                elif(userInput==ord('3')):

                    stdscr.clear()
                    stdscr.refresh()

                    testAlg3(stdscr,1,singleGraphSolution)

                elif(userInput==ord('4')):

                    stdscr.clear()
                    stdscr.refresh()

                    testAlg4(stdscr,1,singleGraphSolution)
                
                elif(userInput==ord('5')):

                    stdscr.clear()
                    stdscr.refresh()

                    inSingleTestMenu = False



        elif(userInput==ord('2')):

            stdscr.clear()
            stdscr.refresh()

            comparativeTrialsOfAlgorithms(stdscr)

        elif(userInput==ord('3')):

            # resets the shell back to normal mode
            curses.endwin()

            exit()



























