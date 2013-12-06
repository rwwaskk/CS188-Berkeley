# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """
                                                         
    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]
    
    
class Node:
	def __init__(self,state,parent,action,cost,c_cost):
		self.state=state
		self.parent=parent
		self.action=action
		self.cost=cost
		self.c_cost=c_cost
		
	def getState(self):
		return self.state
	def getParent(self):
		return self.parent
	def getAction(self):
		return self.action
	def getCost(self):
		return self.cost
	def getCCost(self):
		return self.c_cost
	def SetCCost(cost):
		self.c_cost=cost
		    
    
    
    


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
   
    #closed set
    closed_set=set()
    
    #path
    path=[]
    
    #created a stack, stack stores data in the form of ()
    stack=util.Stack()
    startNode =Node(problem.getStartState(), None, None,0,0)
    stack.push(startNode)
   
    while not stack.isEmpty():
    	u=stack.pop()
    	closed_set.add(u.getState())
    	
    	if problem.isGoalState(u.getState()):
    		print 'goal state!'
    		p=u.getParent()
    		if p is None: return []
    		
    		path.append(u.getAction())
    		while p!=problem.getStartState():
    		 	
    		 	path.append(p.getAction())
    		 	if p.getAction() is None:
    		 		
    		 		
    		 		path.reverse()
    		 		path=path[1:]
    		 		
    		 		return path#['West','West','West','West','South','South','East','South','South','West']
    			
    			p=p.getParent()
    		
    		return path
    		
    	for w in problem.getSuccessors(u.getState()):
    		if w[0] not in closed_set:
    			stack.push(Node(w[0],u,w[1],w[2],None))
    			
    			
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    #print "StartState:",problem.getStartState()
    #created a stack, stack stores data in the form of ()
    queue=util.Queue()
    #closed set
    closed_set=set()
	#path
    path=[]
    startNode =Node(problem.getStartState(), None, None,0,0)
    queue.push(startNode)
    
    while not queue.isEmpty():
    	
    	u=queue.pop()
       # print u.getState(),u.getAction()
    	closed_set.add(u.getState())
    	
    	
    	
    	if problem.isGoalState(u.getState()):
    		
    		#print 'goal state!'
    		p=u.getParent()
    		if p is None: return []
    		path.append(u.getAction())
    		while p!=problem.getStartState():
    		 	path.append(p.getAction())
    		 	if p.getAction() is None:
    		 		path.reverse()
    		 		
    		 		path=path[1:]
    		 		
    		 		
    		 		#print path
    		 		return path#['West','West','West','West','South','South','East','South','South','West']
    			p=p.getParent()
    		
    		return path
    		
    	for w in problem.getSuccessors(u.getState()):
    		
    		if w[0] not in closed_set:
    			queue.push(Node(w[0],u,w[1],w[2],None))
    			
    			closed_set.add(w[0])
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    p_queue=util.PriorityQueue()
   #closed set
    closed_set=set()
	#path
    path=[]
    startNode =Node(problem.getStartState(), None, None,0,0)
    p_queue.push(startNode,startNode.getCCost())
    
    while not p_queue.isEmpty():
    	
    	
    	u=p_queue.pop()
    	while u.getState() in closed_set:
    		u=p_queue.pop()
    	closed_set.add(u.getState())
    	#print u.getState()
    	
    	if problem.isGoalState(u.getState()):
    		print 'goal state!'
    		p=u.getParent()
    		if p is None: return []
    		path.append(u.getAction())
    		while p!=problem.getStartState():
    			
    		 	path.append(p.getAction())
    		 	if p.getAction() is None:
    		 		path.reverse()
    		 		path=path[1:]
    		 		return path#['West','West','West','West','South','South','East','South','South','West']
    			p=p.getParent()
    		return path
    		
    	for w in problem.getSuccessors(u.getState()):
    		if w[0] not in closed_set:
    			node=Node(w[0],u,w[1],w[2],w[2]+u.getCCost())
    			#closed_set.add(u.getState())
    			p_queue.push(node,node.getCCost())
    		
    
    
    
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    p_queue=util.PriorityQueue()
    closed_set=set()
    path=[]
    startNode =Node(problem.getStartState(), None, None,0,0)

    
    p_queue.push(startNode,heuristic(startNode.getState(),problem))
    
   
    while not p_queue.isEmpty():
    
    
		    
    	u=p_queue.pop()
    	while u.getState() in closed_set:
    		u=p_queue.pop()
    	closed_set.add(u.getState())
    	
    	
    	
    	#print u.getState() in closed_set
    	#print u.getState()
    	if problem.isGoalState(u.getState()):
    		#print 'goal state!'
    		#print u.getState()
    		
    		
    		p=u.getParent()
    		if p is None: return []
    		path.append(u.getAction())
    		while p!=problem.getStartState():
    			
    		 	path.append(p.getAction())
    		 	if p.getAction() is None:
    		 		path.reverse()
    		 		path=path[1:]
    		 		return path
    			p=p.getParent()
    		return path
    		
    	for w in problem.getSuccessors(u.getState()):
    		if w[0] not in closed_set:
    			node=Node(w[0],u,w[1],w[2],w[2]+u.getCCost())
    			p_queue.push(node,heuristic(w[0],problem)+node.getCCost())
    			
    
    
	
	
	


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
