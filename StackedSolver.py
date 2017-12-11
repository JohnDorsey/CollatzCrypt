from __future__ import print_function

from SortedStack import *
from ListTools import *
import Collatz
import time


class Solver:
  def __init__(self,start,goal,overshoot,sortEnabled=True,reverseEnabled=False):
    print("initializing solver... ",end="")
    self.start, self.goal, self.overshoot = start, goal, overshoot
    self.sortEnabled, self.reverseEnabled = sortEnabled, reverseEnabled
    self.path = []
    self.upperBound = max(self.start, self.goal) * self.overshoot
    self.done = False
    print("solver initialized")
  
  def solve(self,preview=None):
    self.path, self.upperBound = Collatz.solve(self.start,self.goal,self.upperBound,preview=preview)
    self.done = True

class StackedSolver(Solver):

  #stacksToPath = lambda options, selectors: 
  def __init__(self,start,goal,overshoot,poolSize,sortEnabled=True,reverseEnabled=False):
    Solver.__init__(self,start,goal,overshoot,sortEnabled=sortEnabled,reverseEnabled=reverseEnabled)
    self.visited = SortedStack([])
    self.optionStack, self.selectorStack, self.head = [[start]], [0], 0
    self.poolSize = poolSize
    self.setupGoalForSolve()
    
  def setupGoalForSolve(self):
    print("setting up goal for solve: poolSize=" + str(self.poolSize) +", start=" + str(self.start) + ", goal=" + str(self.goal))
    if self.poolSize > 1:
      self.goalPool = Collatz.generatePoolEdgewise(self.goal,self.poolSize,self.upperBound)
      self.isDone = lambda value: self.goalPool[-1].__contains__(value)
    else:
      self.goalPool = Collatz.generatePool(self.goal,1,self.upperBound)
      self.isDone = lambda value: self.goal == value
    print("done setting up goal")
  
  def solve(self,preview=None):
    print("solving...")
    startTime = time.clock()
    iters = 0
    self.resideSolvingWithin = True
    while(not self.done):
      self.reside()
      if iters%1024==0:
        if preview:
          self.path = self.select(self.optionStack[-128:],self.selectorStack[-128:])
          preview(self.path)
      if self.selectorStack[0] > 0:
        #print("start point failure")
        self.selectorStack[0] = 0
        break
      iters += 1
      #if i%16 == 0 and not textMode:
      #  drawPath(Solution.pathToInstructions(
    self.path = self.select(self.optionStack,self.selectorStack)
    if self.poolSize > 1:
      intersection = self.path[-1]
      self.path.__delitem__(len(self.path)-1)
      self.path += Collatz.browseSegmentedPool(self.goalPool,intersection)
    print("solving took " + str(time.clock() - startTime) + " seconds")
    
  def select(self,options,selectors):
    result = [(-11111 if options[i] == None else (options[i][selectors[i]] if len(options[i]) > selectors[i] else -777700-selectors[i])) for i in range(len(options))]
    trimNeg(result)
    return result
    
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