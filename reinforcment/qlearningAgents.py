# qlearningAgents.py
# ------------------
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
from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
import random,util,math
class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.qvalues = {}
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        qValues = self.qvalues
        if (state, action) not in qValues:
            return 0.0
        else:
            return qValues[(state, action)]
        util.raiseNotDefined()
    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        pAction = self.getLegalActions(state)
        if len(pAction) == 0:
            return 0
        compValue = None
        result = None
        for action in pAction:
            QValue = self.getQValue(state, action)
            if compValue == None:
                compValue = QValue
                result = action
            if QValue > compValue:
                compValue = QValue
                result = action
        if compValue == None:
            compValue = 0
        return compValue
        util.raiseNotDefined()
    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        pAction = self.getLegalActions(state)
        if len(pAction) == 0:
            return 0
        compValue = None
        result = None
        for action in pAction:
            QValue = self.getQValue(state, action)
            if compValue == None:
                compValue = QValue
                result = action
            if QValue > compValue:
                compValue = QValue
                result = action
        return result
        util.raiseNotDefined()
    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        if len(legalActions) == 0:
            return None
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        return self.computeActionFromQValues(state)
        util.raiseNotDefined()
        return action
    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        discount = self.discount
        qValues = self.qvalues
        alpha = self.alpha
        if (state, action) not in qValues:
            qValues[(state, action)] = 0.0
        nextValue = self.computeValueFromQValues(nextState)
        currentValue = qValues[(state, action)]
        cal = reward + (discount * nextValue) - currentValue
        qValues[(state, action)] = currentValue + (alpha * cal)
        "util.raiseNotDefined()"
    def getPolicy(self, state):
        return self.computeActionFromQValues(state)
    def getValue(self, state):
        return self.computeValueFromQValues(state)
class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)
    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action
class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()
    def getWeights(self):
        return self.weights
    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        feature = self.featExtractor.getFeatures(state, action)
        QValue = 0.0
        weight = self.weights
        for f in feature:
            QValue += weight[f] * feature[f]
        return QValue
        util.raiseNotDefined()
    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        feature = self.featExtractor.getFeatures(state, action)
        discount = self.discount
        gValue = self.getValue
        getQvalue = self.getQValue
        weight = self.weights
        alpha = self.alpha
        update = reward + discount * gValue(nextState) - getQvalue(state, action)
        for f in feature:
            weight[f] += alpha * update * feature[f]
        "util.raiseNotDefined()"
    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)
        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            print (self.weights)
            pass