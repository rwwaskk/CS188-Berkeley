# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
from __future__ import division #to make sure float
from util import manhattanDistance
from game import Directions
import random, util
import random, util, math
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
     
        #new food
        newFood = successorGameState.getFood()
        foodGrid = newFood.asList()
     
         
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        nearestFood=None
        disFromNearestFood = None
        for food in currentGameState.getFood().asList():
        	tmp = manhattanDistance(food, currentGameState.getPacmanPosition())
        	if (disFromNearestFood==None or disFromNearestFood>tmp):
        		disFromNearestFood=tmp
        		nearestFood=food
        
        disFromNearestFoodNew=manhattanDistance(nearestFood,newPos)
        
        ghostEval=0
        pelletEval=0
        
        for ghost in newGhostStates:
        	if ghost.scaredTimer<=0:
        		if (manhattanDistance(newPos,ghost.getPosition())<=3):
        			ghostEval-=(3-manhattanDistance(newPos, ghost.getPosition()))**2
        else:
                pelletEval+=10
            
            
        			
        	
        		
      	return ghostEval-disFromNearestFoodNew+pelletEval
      

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
    
    	#get pacman legal actions
    	legalMoves=gameState.getLegalActions(0)
    	
    	#result gamestate for all legal actions
    	resultStates=[gameState.generateSuccessor(0,action) for action in legalMoves]
    	
    	#get scores from minimizer
    	scores=[self.minimizer(0,state,1) for state in resultStates]
    	bestScore = max(scores)
    	bestIndices = [index for index in range(len(scores)) if scores[index]==bestScore]
    	chosenIndex = random.choice(bestIndices)
    	return legalMoves[chosenIndex]
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
        """
        "*** YOUR CODE HERE ***"
    def maximizer(self,currentDepth,gameState):
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
    	legalMoves=gameState.getLegalActions(0)
    	resultStates=[gameState.generateSuccessor(0,action) for action in legalMoves]
    	scores=[self.minimizer(currentDepth,state,1) for state in resultStates]
    	return max(scores)
    	
    def minimizer(self,currentDepth,gameState,ghostIndex):
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
    	
    	
    	legalMoves=gameState.getLegalActions(ghostIndex)
    	resultStates=[gameState.generateSuccessor(ghostIndex, action) for action in legalMoves]
    	
    	if (ghostIndex>=gameState.getNumAgents()-1):
    		scores=[self.maximizer(currentDepth+1,state) for state in resultStates]
    	else:
    		scores=[self.minimizer(currentDepth,state,ghostIndex+1) for state in resultStates]
    	return min(scores)
    


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def minimizer(self,currentDepth,gameState,ghostIndex,alpha,beta):
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
    	legalMoves = gameState.getLegalActions(ghostIndex)
    	currentScore=float('infinity')
    	for action in legalMoves:
    		resultState=gameState.generateSuccessor(ghostIndex,action)
    		if(ghostIndex<gameState.getNumAgents()-1):
    			currentScore=min(currentScore,self.minimizer(currentDepth,resultState,ghostIndex+1,alpha,beta))
    		elif(ghostIndex==gameState.getNumAgents()-1):
    			currentScore=min(currentScore,self.maximizer(currentDepth+1,resultState,alpha,beta))
    		if (currentScore<alpha):
    			return currentScore
    		beta=min(currentScore,beta)
    	return currentScore
    
    def maximizer(self,currentDepth,gameState,alpha,beta):
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
    	legalMoves=gameState.getLegalActions(0)
    	currentScore=float('-infinity')
    	for move in legalMoves:
    		resultState=gameState.generateSuccessor(0,move)
    		currentScore=max(currentScore,self.minimizer(currentDepth,resultState,1,alpha,beta))
    		if(currentScore>beta):
    			return currentScore
    	
    	return currentScore
	
	
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha=float('-infinity')
        beta=float('infinity')
        legalMoves=gameState.getLegalActions(0)
        
        currentScore=float('-infinity')
        currentMove=legalMoves[0]
        
        for move in legalMoves:
        	resultState=gameState.generateSuccessor(0,move)
        	resultScore=self.minimizer(0,resultState,1,alpha,beta)
        	if (resultScore>currentScore):
        		currentScore=resultScore
        		currentMove=move
        	if(resultScore>beta):
        		return currentMove
        	alpha=max(alpha,resultScore)
        	
        return currentMove
    
	
        		
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expecti (self,currentDepth,gameState,ghostIndex):
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
    	legalMoves=gameState.getLegalActions(ghostIndex)
    	resultStates=[gameState.generateSuccessor(ghostIndex,move) for move in legalMoves]
    	
    	if(ghostIndex==gameState.getNumAgents()-1):
    		scores=[self.maximizer(currentDepth+1,state) for state in resultStates]
    	elif(ghostIndex<gameState.getNumAgents()-1):
    		scores=[self.expecti(currentDepth,state,ghostIndex+1) for state in resultStates]
    	
    	return sum(scores)/len(scores)
    	
    def maximizer(self,currentDepth,gameState):
    	if(self.depth==currentDepth or gameState.isLose() or gameState.isWin()):
    		return self.evaluationFunction(gameState)
    	legalMoves=gameState.getLegalActions(0)
    	resultStates=[gameState.generateSuccessor(0,move) for move in legalMoves]
    	scores=[self.expecti(currentDepth,state,1) for state in resultStates]
    	return max(scores)

    def getAction(self, gameState):
    	legalMoves=gameState.getLegalActions(0)
    	resultStates=[gameState.generateSuccessor(0,move) for move in legalMoves]
    	scores=[self.expecti(0,state,1) for state in resultStates]
    	bestScore=max(scores)
    	bestIndices=[index for index in range(len(scores)) if scores[index]==bestScore]
    	chosenIndex=random.choice(bestIndices)
    	return legalMoves[chosenIndex]
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    
    DESCRIPTION:
    Stuff that's good- ghosts not so close that they can kill Pacman, food, power pellets, scared ghosts
    Stuff that's bad- dying
  """
  "*** YOUR CODE HERE ***"
  
  pos= currentGameState.getPacmanPosition()
  foodGrid = currentGameState.getFood().asList()
  ghostStates = currentGameState.getGhostStates() 
  
  
  distToNearestFood = None
  for food in foodGrid:
    tmp = mazeDistance(pos, food,currentGameState.getWalls())
    if(distToNearestFood == None or distToNearestFood > tmp):
        distToNearestFood = tmp
  if(distToNearestFood == None):
    distToNearestFood = 0
    

  
  ghostEval = 0
  capsuleEval = 0
  for ghostState in ghostStates:
    if(ghostState.scaredTimer <= 0):
      if(mazeDistance(pos, ghostState.getPosition(),currentGameState.getWalls()) <= 3):
        ghostEval -= (3 - mazeDistance(pos, ghostState.getPosition(),currentGameState.getWalls()))**4
    else:
      capsuleEval += 10
  
  
  return  ghostEval + capsuleEval - 0.2 * distToNearestFood+scoreEvaluationFunction(currentGameState) 


def mazeDistance(x, y, walls):
	from util import Queue
 
	queue = Queue()
	visitedSet = set()
	queue.push((x, 0))
  
	while not queue.isEmpty():
		currentNode = queue.pop()
		if(currentNode[0] == y):
			return currentNode[1]
		successors = getSuccessors(currentNode[0], walls)
		for successor in successors:
			if successor not in visitedSet:
				queue.push((successor, currentNode[1] + 1))
				visitedSet.add(successor)
      
	return None
  

def getSuccessors(pos, walls):
	results=[]
	x=pos[0]
	y=pos[1]
	
	if x>=1:
		if not walls[x-1][y]:
			results.append((x-1,y-1))
	
			
	if x<walls.width-1:
		if not walls[x+1][y]:
			results.append((x+1,y))
		if y>=1:
			if not walls[x+1][y-1]:
				results.append((x+1,y-1))
		if y<walls.height-1:
			if not walls[x+1][y+1]:
				results.append((x+1,y+1))
		if y>=1:
			if not walls[x][y-1]:
				results.append((x,y-1))
		if y<walls.height-1:
			if not walls[x][y+1]:
				results.append((x,y+1))
				
				
	if y>=1:
		if not walls[x-1][y-1]:
			results.append((x-1,y-1))
	if y<walls.height-1:
		if not walls[x-1][y+1]:
			results.append((x-1,y-1))
	
		
	return results
  

  


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """
    
  def __init__(self, evalFn='betterEvaluationFunction', depth='3'):
    MultiAgentSearchAgent.__init__(self, evalFn, depth)
  
  def minEvalGhosts(self, currentDepth, gameState, ghostIndex, alpha, beta):
    if(self.depth == currentDepth or gameState.isLose() or gameState.isWin()):
        return self.evaluationFunction(gameState)
    numGhosts = gameState.getNumAgents() - 1
    minScore = None
    legalActions = gameState.getLegalActions(ghostIndex)
    score = float('infinity')
    for action in legalActions:
      resultingGameState = gameState.generateSuccessor(ghostIndex, action)
      if(ghostIndex < numGhosts):
        score = min(score, self.minEvalGhosts(currentDepth, resultingGameState, ghostIndex + 1, alpha, beta))
      elif(ghostIndex == numGhosts):
        score = min(score, self.maxEvalPacman(currentDepth + 1, resultingGameState, alpha, beta))
      if(score < alpha):
        return score
      beta = min(score, beta)
    return score
    
  def maxEvalPacman(self, currentDepth, gameState, alpha, beta):
    if (self.depth == currentDepth or gameState.isLose() or gameState.isWin()):
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalPacmanActions()
    legalActions.remove(Directions.STOP)
    score = float('-infinity')
    
    for action in legalActions:
      resultingGameState = gameState.generatePacmanSuccessor(action)
      score = max(score, self.minEvalGhosts(currentDepth, resultingGameState, 1, alpha, beta))
      if(score > beta):
        return score
      alpha = max(alpha, score)

    return score
    
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    print 'get action'
    
    legalActions = gameState.getLegalPacmanActions()
    print legalActions
    legalActions.remove(Directions.STOP)
    print legalActions
    score = float('-infinity')
    bestAction = legalActions[0]
    print bestAction
    for action in legalActions:
      resultingGameState = gameState.generatePacmanSuccessor(action)
      
     
        
    return bestAction
  

