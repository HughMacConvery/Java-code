# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]
    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        "foodList = foodGrid.asList()"
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodList = newFood.asList()
        ghostPosition = successorGameState.getGhostPositions()
        distToFood = -1
        for food in foodList:
            distance = util.manhattanDistance(newPos, food)
            if distToFood >= distance or distToFood == -1:
                distToFood = distance
        disToGhost = 1
        proxToGhost = 0
        for ghost in ghostPosition:
            distance = util.manhattanDistance(newPos, ghost)
            disToGhost += distance
            if distance <= 1:
                proxToGhost += 1
        value = (1 /float(distToFood)) - (1 / float(disToGhost)) - proxToGhost
        score = successorGameState.getScore() + value
        return score
def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()
class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.
    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        Here are some method calls that might be useful when implementing minimax.
        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
        gameState.getNumAgents():
        Returns the total number of agents in the game
        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        def minimax(pacman, depth, gameState):
            if gameState.isLose():
                return self.evaluationFunction(gameState)
            if gameState.isWin():
                return self.evaluationFunction(gameState)
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            if pacman == 0:
                maxing = max(minimax(1, depth, gameState.generateSuccessor(pacman, node)) for node in gameState.getLegalActions(pacman))
                return maxing
            else:
                nextP = pacman + 1
                if gameState.getNumAgents() == nextP:
                    nextP = 0
                if nextP == 0:
                   depth += 1
                mining = min(minimax(nextP, depth, gameState.generateSuccessor(pacman, node)) for node in gameState.getLegalActions(pacman))
                return mining
        maximum = float("-inf")
        action = Directions.NORTH
        for Pstate in gameState.getLegalActions(0):
            utility = minimax(1, 0, gameState.generateSuccessor(0, Pstate))
            if utility > maximum:
                maximum = utility
                action = Pstate
            if maximum == float("-inf"):
                maximum = utility
                action = Pstate 
        return action
        util.raiseNotDefined()
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def maxing(pacman, depth, gameState, AlphaA, BetaA): 
            value = float("-inf")
            for node in gameState.getLegalActions(pacman):
                value = max(value, AlphaBeta(1, depth, gameState.generateSuccessor(pacman, node), AlphaA, BetaA))
                if value > BetaA:
                    return value
                AlphaA = max(AlphaA, value)
            return value
        def mining(pacman, depth, gameState, AlphaA, BetaA):  
            value = float("inf")
            nextP = pacman + 1 
            if gameState.getNumAgents() == nextP:
                nextP = 0
            if nextP == 0:
                depth += 1
            for node in gameState.getLegalActions(pacman):
                value = min(value, AlphaBeta(nextP, depth, gameState.generateSuccessor(pacman, node), AlphaA, BetaA))
                if value < AlphaA:
                    return value
                BetaA = min(BetaA, value)
            return value
        def AlphaBeta(pacman, depth, gameState, AlphaA, BetaA):
            if gameState.isLose():
                return self.evaluationFunction(gameState)
            if gameState.isWin():
                return self.evaluationFunction(gameState)
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            if pacman == 0:
                return maxing(pacman, depth, gameState, AlphaA, BetaA)
            else:
                return mining(pacman, depth, gameState, AlphaA, BetaA)
        utility = float("-inf")
        action = Directions.NORTH
        alpha = float("-inf")
        beta = float("inf")
        for Pstate in gameState.getLegalActions(0):
            ghostV = AlphaBeta(1, 0, gameState.generateSuccessor(0, Pstate), alpha, beta)
            if ghostV > utility:
                utility = ghostV
                action = Pstate
            if utility > beta:
                return utility
            alpha = max(alpha, utility)
        return action
        util.raiseNotDefined()
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def expectimax(pacman, depth, gameState):
            if gameState.isLose():
                return self.evaluationFunction(gameState)
            if gameState.isWin():
                return self.evaluationFunction(gameState)
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            if pacman == 0:
                maxing = max(expectimax(1, depth, gameState.generateSuccessor(pacman, node))for node in gameState.getLegalActions(pacman))
                return maxing
            else:
                nextP = pacman + 1
                if gameState.getNumAgents() == nextP:
                    nextP= 0
                if nextP == 0:
                    depth += 1
                Sum = sum(expectimax(nextP, depth, gameState.generateSuccessor(pacman, node)) for node in gameState.getLegalActions(pacman))
                value = Sum / float(len(gameState.getLegalActions(pacman)))
                return value
        maximum = float("-inf")
        action = Directions.NORTH
        for Pstate in gameState.getLegalActions(0):
            utility = expectimax(1, 0, gameState.generateSuccessor(0, Pstate))
            if utility > maximum:
                maximum = utility
                action = Pstate
            if maximum == float("-inf"):
                maximum = utility
                action = Pstate
        return action
        util.raiseNotDefined()
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    foodList = newFood.asList()
    distToFood = -1
    for food in foodList:
        distance = util.manhattanDistance(newPos, food)
        if distToFood >= distance or distToFood == -1:
            distToFood = distance
        disToGhost = 1
        proxToGhost = 0
    for Gstate in currentGameState.getGhostPositions():
        distance = util.manhattanDistance(newPos, Gstate)
        disToGhost += distance
        if distance <= 1:
            proxToGhost += 1
    pellet = currentGameState.getCapsules()
    numOfPellets = len(pellet)
    value = (1 / float(distToFood)) - (1 / float(disToGhost)) - proxToGhost - numOfPellets
    score = currentGameState.getScore() + value
    return score
    util.raiseNotDefined()
# Abbreviation
better = betterEvaluationFunction