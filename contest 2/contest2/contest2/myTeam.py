# myTeam.py
# ---------
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
from captureAgents import CaptureAgent
import random, time, util
from game import Directions, Actions
import game
#################
# Team creation #
#################
def createTeam(firstIndex, secondIndex, isRed, first = 'OffenseAgent', second = 'DefenseAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.
  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]
##########
# Agents #
##########
class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """
  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)
    IMPORTANT: This method may run for at most 15 seconds.
    """
    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)
    '''
    Your initialization code goes here, if you need any.
    '''
  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)
    '''
    You should change this in your own agent.
    '''
    return random.choice(actions)
class OffenseAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.epsilon = 0.0 
        self.alpha = 0.2 
        self.discountRate = 0.8 
        self.weights = {'closestPellet': -2.2558226236802597} 
        self.weights ['bias'] = 1.0856704846852672 
        self.weights['ghost1Away'] = -0.18419418670562
        self.weights['successorScore'] = -0.027287497346388308
        self.weights['eatFood'] = 9.970429654829946
    def getQValue(self, gameState, action):
        features = self.getFeatures(gameState, action)
        return features * self.weights
    def getValue(self, gameState):
        qValues = []
        legalActions = gameState.getLegalActions(self.index)
        if len(legalActions) == 0:
            return 0.0
        else:
            for action in legalActions:
                qValues.append(self.getQValue(gameState, action))
            return max(qValues)
    def getPolicy(self, gameState):
        values = []
        legalActions = gameState.getLegalActions(self.index)
        legalActions.remove(Directions.STOP)
        if len(legalActions) == 0:
            return None
        else:
            for action in legalActions:
                values.append((self.getQValue(gameState, action), action))
        return max(values)[1]
    def chooseAction(self, gameState):
        legalActions = gameState.getLegalActions(self.index)
        action = None
        if len(legalActions) != 0:
            probability = util.flipCoin(self.epsilon)
            if probability:
                action = random.choice(legalActions)
            else:
                    action = self.getPolicy(gameState)
        return action
    def getFeatures(self, gameState, action):
        food = gameState.getBlueFood()
        wall = gameState.getWalls()
        ghosts = []
        opponentAgents = CaptureAgent.getOpponents(self, gameState)
        if opponentAgents:
            for opponent in opponentAgents:
                opponentPosition = gameState.getAgentPosition(opponent)
                opponentIsPacman = gameState.getAgentState(opponent).isPacman
                if opponentPosition and not opponentIsPacman: 
                    ghosts.append(opponentPosition)
        counter = util.Counter()
        successor = self.getSuccessor(gameState, action)
        counter['successorScore'] = self.getScore(successor)
        counter["bias"] = 1.0
        x, y = gameState.getAgentPosition(self.index)
        dx, dy = Actions.directionToVector(action)
        nextX, nextY = int(x + dx), int(y + dy)
        counter["ghost1Away"] = sum((nextX, nextY) in Actions.getLegalNeighbors(g, wall) for g in ghosts)
        if not counter["ghost1Away"] and food[nextX][nextY]:
            counter["eatFood"] = 1.0
        dist = self.closestFood((nextX, nextY), food, wall)
        if dist is not None:
            counter["closestPellet"] = float(dist) / (wall.width * wall.height) 
        counter.divideAll(10.0)
        return counter
    def update(self, gameState, action):
        features = self.getFeatures(gameState, action)
        nextState = self.getSuccessor(gameState, action)
        reward = nextState.getScore() - gameState.getScore()
        for feature in features:
            rewardDiscount = (reward + self.discountRate * self.getValue(nextState))
            update = rewardDiscount - self.getQValue(gameState, action)
            weight = self.weights[feature] + self.alpha * update * features[feature]
            self.weights[feature] = weight
    def getSuccessor(self, gameState, action):
        successor = gameState.generateSuccessor(self.index, action)
        position = successor.getAgentState(self.index).getPosition()
        if position != util.nearestPoint(position):
            return successor.generateSuccessor(self.index, action)
        else:
            return successor
    def closestFood(self, pos, food, walls):
        pelletPosition = [(pos[0], pos[1], 0)]
        expand = set()
        while pelletPosition:
            positionX, positionY, dist = pelletPosition.pop(0)
            if (positionX, positionY) in expand:
                continue
            expand.add((positionX, positionY))
            if food[positionX][positionY]:
                return dist
            neighbor = Actions.getLegalNeighbors((positionX, positionY), walls)
            for neighborAtX, neighborAtY in neighbor:
                pelletPosition.append((neighborAtX, neighborAtY, dist+1))
        return None
    
class DefenseAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.myAgents = CaptureAgent.getTeam(self, gameState)
        self.opponentsAgents = CaptureAgent.getOpponents(self, gameState)
        self.myFoods = CaptureAgent.getFood(self, gameState).asList()
        self.opponentsFoods = CaptureAgent.getFoodYouAreDefending(self, gameState).asList()
    def getSuccessor(self, gameState, action):
        successor = gameState.generateSuccessor(self.index, action)
        position = successor.getAgentState(self.index).getPosition()
        if position  != util.nearestPoint(position):
            return successor.generateSuccessor(self.index, action)
        else:
            return successor
    def getFeatures(self, gameState, action):
        counter = util.Counter()
        successor = self.getSuccessor(gameState, action)
        state = successor.getAgentState(self.index)
        position = state.getPosition()
        counter['onDefense'] = 1
        if state.isPacman: 
            counter['onDefense'] = 0
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        opponenets = [x for x in enemies if x.isPacman and x.getPosition() != None]
        counter['opponenetsNumbers'] = len(opponenets)
        if len(opponenets) > 0:
            dists = [self.getMazeDistance(position, x.getPosition()) for x in opponenets]
            counter['opponenetsDefense'] = min(dists)
        if action == Directions.STOP: 
            counter['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: 
            counter['reverse'] = 1
        return counter
    def getWeights(self, gameState, action):
        weight = {'opponenetsNumbers': -1000} 
        weight ['onDefense'] = 100
        weight ['opponenetsDefense'] = -10 
        weight ['stop'] = -100 
        weight ['reverse'] = -2
        return weight
    def evaluate(self, gameState, action):
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights
    def chooseAction(self, gameState):
        agentPossition = gameState.getAgentPosition(self.index)
        actions = gameState.getLegalActions(self.index)
        distToFood = []
        for food in self.myFoods:
            distToFood.append(self.distancer.getDistance(agentPossition, food))
        distanceOpponent = []
        for opponent in self.opponentsAgents:
            opponentPosition = gameState.getAgentPosition(opponent)
            if opponentPosition != None:
                distanceOpponent.append(self.distancer.getDistance(agentPossition, opponentPosition))
        values = [self.evaluate(gameState, x) for x in actions]
        maxValue = max(values)
        bestActions = [x for x, value in zip(actions, values) if value == maxValue]
        return random.choice(bestActions)