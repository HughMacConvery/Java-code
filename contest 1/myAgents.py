# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from game import Agent
from searchProblems import PositionSearchProblem
import util
import time
import search
"""IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]
chaseFood = util.Queue()
indexQ = util.Queue()
targetList = []
PacmanPosition = []
class MyAgent(Agent):
    """Implementation of your agent."""
    def manhattanDist(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])
    def take(self, elem):
                return elem[1]
    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        global PacmanPosition
        global targetList
        PacmanPosition[self.index] = state.getPacmanPosition(self.index) 
        if self.actions.isEmpty():
            food = state.getFood().asList()
            self.food = food
            global chaseFood
            global indexQ
            startPosition = state.getPacmanPosition(self.index)
            for lenList in range(len(chaseFood.list)):
                cF = chaseFood.pop()
                iQ = indexQ.pop()
                if cF != self.goal:
                    chaseFood.push(cF)
                    indexQ.push(iQ)
            pellets = food[:]
            for lenFood in range(len(food)):
                pellets[lenFood] = (lenFood, self.manhattanDist(food[lenFood], startPosition))
            pellets.sort(key = self.take)
            LenOfChoice = len(food)
            if LenOfChoice > 5:
                LenOfChoice = 5
            look = True
            for length in range(LenOfChoice):
                p = pellets[length]
                goal = food[p[0]]
                distance = p[1]
                test = False
                for lenFood in range(len(chaseFood.list)):
                    if (self.manhattanDist(chaseFood.list[lenFood], goal) <= 3):
                        if (distance + 2 >= self.manhattanDist(goal, PacmanPosition[indexQ.list[lenFood]])):
                            test = True
                            break
                        targetList[indexQ.list[lenFood]] = 0
                if test == True:
                    continue
                look = False
                break
            if look == False:
                self.goal = goal
            else:
                self.goal = food[pellets[0][0]]   
                distance = pellets[0][1]
            chaseFood.push(self.goal)
            indexQ.push(self.index)
            targetList[self.index] = 1
            problem = NewFoodSearchProblem(state, self.index, self.goal)
            actionList = search.aStarSearch(problem, heuristic=self.manhattanHeuristic)
            LenOfActions = len(actionList)
            for actions in range(LenOfActions):
                aL = actionList[actions]
                self.actions.push(aL)
        action = self.actions.pop()
        return action
        "raise NotImplementedError()"
    def manhattanHeuristic(self, position, problem, info={}):
        "The Manhattan distance heuristic for a PositionSearchProblem"
        xy1 = position
        goal = self.goal
        distance =  abs(xy1[0] - goal[0]) + abs(xy1[1] - goal[1])
        food = self.food
        if goal in food:
            distance += 10
        return distance
    def initialize(self):
        """Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank"""
        self.actions = util.Queue()
        self.goal = (0,0)
        global PacmanPosition
        PacmanPosition.append((0,0))
        global targetList
        targetList.append(0)
        "raise NotImplementedError()"
"""Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)"""
class ClosestDotAgent(Agent):
    def findPathToClosestDot(self, gameState):
        """Returns a path (a list of actions) to the closest dot, starting from
        gameState."""
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)
        return search.bfs(problem)
        util.raiseNotDefined()
    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]
class AnyFoodSearchProblem(PositionSearchProblem):
    """A search problem for finding a path to any food.
    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.
    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.
    You can use this search problem to help you fill in the findPathToClosestDot
    method."""
    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        self.food = gameState.getFood()
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE
    def isGoalState(self, state):
        """The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition."""
        x,y = state
        foods = self.food.asList()
        if state in foods:
            return True
        else:
            return False
        util.raiseNotDefined()
class NewFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to a specific food.
    """
    def __init__(self, gameState, agentIndex, goal):
        "Stores information from the gameState.  You don't need to change this."
        self.food = gameState.getFood()
        self.goal = goal
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        if x == self.goal[0] and y == self.goal[1]:
            return True
        else:
            return False
        util.raiseNotDefined()