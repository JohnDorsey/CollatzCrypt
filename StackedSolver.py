from SortedStack import *
import Collatz
import time


class StackedSolver:

  #stacksToPath = lambda options, selectors: 

  def __init__(self,overshoot,poolSize,start,goal,sortEnabled=True,reverseEnabled=False):
    print("initializing solver...")
    self.overshoot, self.poolSize, self.start, self.goal = overshoot, poolSize, start, goal
    self.sortEnabled, self.reverseEnabled = sortEnabled, reverseEnabled
    self.visited = SortedStack([])
    self.path = []
    self.upperBound = max(self.start, self.goal) * self.overshoot
    self.optionStack, self.selectorStack, self.head = [[start]], [0], 0
    self.done = False
    print("solver initialized")
    
  def setupGoalForSolve(self):
    print("setting up goal for solve: poolSize=" + str(self.poolSize) +", start=" + str(self.start) + ", goal=" + str(self.goal))
    if self.poolSize > 1:
      self.goalPool = Collatz.generatePoolEdgewise(self.goal,self.poolSize,self.upperBound)[-1]
      self.isDone = lambda value: self.goalPool.__contains__(value)
    else:
      self.goalPool = Collatz.generatePool(self.goal,1,self.upperBound)
      self.isDone = lambda value: self.goal == value
    #print("internal tracking: " +track.toString())
  
  def solve(self):
    print("solving...")
    startTime = time.clock()
    i = 0
    self.resideSolvingWithin = True
    while(not self.done):
      self.reside()
      if self.selectorStack[0] > 0:
        #print("start point failure")
        self.selectorStack[0] = 0
        break
      i += 1
      #if i%16 == 0 and not textMode:
      #  drawPath(Solution.pathToInstructions(
    self.path = [(-11111 if self.optionStack[i] == None else (self.optionStack[i][self.selectorStack[i]] if len(self.optionStack[i]) > self.selectorStack[i] else -777700-self.selectorStack[i])) for i in range(len(self.optionStack))]
    print("solving took " + str(time.clock() - startTime) + " seconds")
    
  def reside(self):
    #I create myself
    selection = self.selectorStack[self.head]
    if selection >= len(self.optionStack[self.head]): # I died
      self.selectorStack[self.head-1] += 1  #I tell the previous item that it should not have created me
      self.selectorStack[self.head] = None
      self.optionStack[self.head] = None
      self.head -= 1
      return
    #I am here
    here = self.optionStack[self.head][selection]
    #}I am recorded
    self.visited.append(here)
    if self.isDone(here):
      self.done = True
      return
    self.head += 1
    if len(self.optionStack) <= self.head:
      self.optionStack.append(None)
    if len(self.selectorStack) <= self.head:
      self.selectorStack.append(None)
    self.optionStack[self.head] = Collatz.optionsFrom(here,self.goal,self.visited,self.upperBound,doSort=self.sortEnabled,doReverse=self.reverseEnabled)
    self.selectorStack[self.head] = 0
    return