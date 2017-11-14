
from __future__ import print_function


'''+++++++++++++++++++++++++++++++'''
#Configure me:

textMode = False

trimOutput = True

sortEnabled = True
reverseEnabled = False
logarithmicOutputEnabled = False
drawType = "exact" #"direct", "type", "exact"

'''-------------------------------------------------------'''


import sys
ver = sys.version[:1]
from SortedList import *
from SortedStack import *
from ListTools import *
import Solution
import Collatz


SIZE = (1280,640)



import math
import time

if not textMode:
  try:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("John Dorsey's CollatzCrypt, non-recursive implementation")
    #from jdev import *
  except:
    print("couldn't find pygame module. running in text mode...")
    if ver == "3":
      print("to view the full output, install pygame by running python's package manager directly from the shell or command prompt.")
      print("windows command prompt or linux shell:")
      print("    pip install pygame")
    textMode = True


alpha = 24
colors = {"down":[210,0,255,alpha], "up":[0,255,192,alpha],"err":[127,0,0,alpha],"large":[220,220,0,alpha],"small":[15,144,220,alpha],0:[192,0,35,alpha],1:[124,192,0,alpha],2:[35,0,192,alpha],3:[0,192,124,alpha]}

overshoot = 4

if logarithmicOutputEnabled:
  screenv = lambda v, upperBound: SIZE[1] - min(max(int(float(SIZE[1]-4) * ((2*math.log(v+1,1.000125) / math.log(upperBound+1,1.000125)) - 1)) + 2,0),SIZE[1]-1)
else:
  screenv = lambda v, upperBound: min(max(int(float(SIZE[1]-4) * ((v / upperBound))) + 2,0),SIZE[1]-1)
#




class Track:
  def __init__(self):
    self.discardedOptions = {}
  def reset(self):
    self.discardedOptions = {"overshoot2":0, "overshoot3":0, "nonintegral2":0, "nonintegral3":0, "duplicate":0, "non":0}
  def toString(self,doReset=True):
    text = str(track.discardedOptions)
    if doReset:
      self.reset()
    return text
#track = Track()


class CollatzSolver:

  #stacksToPath = lambda options, selectors: 

  def __init__(self,start,goal,poolSize):
    print("initializing solver...")
    self.start, self.goal = start, goal
    self.visited = SortedStack([])
    self.path = []
    self.upperBound = max(self.start, self.goal) * overshoot
    self.optionStack, self.selectorStack, self.head = [[start]], [0], 0
    self.done = False
    self.poolSize = poolSize
    print("solver initialized")
    
  def setupGoalForSolve(self):
    print("setting up goal for solve...")
    if self.poolSize > 1:
      self.goalPool = Collatz.generatePoolEdgewise(self.goal,self.poolSize,self.upperBound)
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
    self.optionStack[self.head] = Collatz.optionsFrom(here,self.goal,self.visited,self.upperBound,doSort=sortEnabled,doReverse=reverseEnabled)
    self.selectorStack[self.head] = 0
    return
    



if textMode:
  def drawRate(a):
    pass
  def drawGuides(a,b,c,d):
    pass
  def drawHorizGuide(a):
    pass
  def drawPath(a,b):
    pass
  def drawSpiral(a):
    pass
  def drawFrequencies(a,b):
    pass
  def drawInstructions(instructions,reversed=False):
    pass
  def pollEvents():
    pass
else:
  def drawRate(upperBound):
    last = (0,0)
    current = (0,0)
    for i in range(SIZE[1]):
      last = current
      current = ((i)*(SIZE[0]/SIZE[1]),screenv(upperBound*i/(1.0*SIZE[1]),upperBound))
      pygame.draw.aaline(screen,colors["err"],last,current,4)
      pygame.display.flip()
    pollEvents()

  def drawGuides(start,goal,upperBound,inputPath):
    screen.fill([0,0,0])
    for val in [start,goal,upperBound,getMin(inputPath),getMax(inputPath)]:
      drawHorizGuide(screenv(val,upperBound))
    pollEvents()

  def drawHorizGuide(height):
    pygame.draw.aaline(screen,colors["err"],(0,height),(SIZE[0],height),1)

  def drawPath(inputPath,upperBound):
    deltaPos = float(SIZE[0] * 0.5) / len(inputPath)
    color = "err"
    for i in range(len(inputPath)-1):
      if inputPath[i] > 0:
        color = colorFrom(drawType,inputPath[i],inputPath[i+1])
        pygame.draw.aaline(screen,
          colors[color],
          (deltaPos*i,screenv(inputPath[i],upperBound)),
          (deltaPos*(i+1),screenv(inputPath[i+1],upperBound)),1)
      else:
        pygame.draw.aaline(screen,colors["err"],(deltaPos*i,0),(deltaPos*(i+1),SIZE[1]-1),1)
    pollEvents()

  def drawSpiral(inputPath):
    #currentPt = (SIZE[0]//2,SIZE[1]//4)
    centerPt = (SIZE[0]//4,SIZE[1]//2)
    currentPt = toSpiral(inputPath[0],startPos=centerPt)
    lastPt = currentPt
    color = "err"
    optionLenths = []
    for i in range(len(inputPath)-1):
      color = colorFrom(drawType,inputPath[i],inputPath[i+1])
      currentPt = toSpiral(inputPath[i+1],startPos=centerPt)
      #print(currentPt)
      
      pygame.draw.aaline(screen,colors[color],lastPt,currentPt,1)
      lastPt=currentPt
    pollEvents()
       
  def drawFrequencies(inputPath,upperBound):
    frequencyMap = [0 for i in range(SIZE[1]+8)]
    for point in inputPath:
      #print(screenv(point))
      if point > 0:
        frequencyMap[screenv(point,upperBound)] += 1
    scale = SIZE[0] * 0.5 / getMax(frequencyMap)
    for i in range(len(frequencyMap)-4):
      for passNum in range(4):
        pygame.draw.aaline(screen, colors["down" if frequencyMap[i+passNum]<frequencyMap[i] else "up"],(SIZE[0]*0.5+frequencyMap[i]*scale,i),(SIZE[0]*0.5+frequencyMap[i+passNum]*scale,i+passNum),1)
      pygame.display.flip()
    pollEvents()
  
  def drawInstructions(instructions,reversed=False):
    pos = (SIZE[0]//4, SIZE[1]//2)
    color = "err"
    inc = (0,0)
    for op in instructions:
      inc = (-1 if op==0 else 1 if op==2 else 0, -1 if op==1 else 1 if op==3 else 0)
      pos = (pos[0] + inc[0], pos[1] + inc[1]) if not reversed else (pos[0] + inc[1], pos[1] + inc[0])
      screen.set_at((pos[0]%SIZE[0],pos[1]%SIZE[1]),colors[op])
    pollEvents()
    
  def pollEvents():
    pygame.display.flip()
    for ev in pygame.event.get():
      if ev.type == pygame.QUIT:
        exit()
      
    
   
def colorFrom(drawt, current, next):
  if drawt == "type" or drawt=="exact":
    op = Solution.valuesToOperation(current,next)
    if type(op) == int:
      if drawt=="exact":
        return op
      return "small" if [1,2].__contains__(op) else "large"
    else:
      return "err"
  elif drawt == "direct":
    return "down" if next<current else "up"
  else:
    print("unknown draw type: " + str(drawt))
    return "err"
  

def trimOut(inputText,length=60):
  text = "" + str(inputText) + ""
  return ("ends with ..." + text[-length:]) if len(text) > length and trimOutput else text
      
  
def toSpiral(num,startPos = (0,0)):
  x, y = startPos
  length = 1
  for i in range(1,512):
    y += min(num,length)
    num -= length
    if num <= 0:
      break
    length += 1
    x += min(num,length)
    num -= length
    if num <= 0:
      break
    y -= min(num,length)
    num -= length
    if num <= 0:
      break
    length += 1
    x -= min(num,length)
    num -= length
    if num <= 0:
      break
  return (x,y)
'''  
testDupes = [1,2,3,3,4,5,6,6,7,7,7,8,9]      
print(testDupes)
dedupe(testDupes)
print(testDupes)


testDupes = [1,2,3,3,4,5,6,6,7,7,7,8,9,9]      
print(testDupes)
dedupe(testDupes)
print(testDupes)'''
'''
screen.fill([0,0,0])
for i in range(min(SIZE[0],SIZE[1])**2):
  screen.set_at(toSpiral(i,startPos=(320,320)),[255,255,255,255])
  pollEvents()
  screen.set_at(toSpiral(i,startPos=(320,320)),[255,0,0,255])
'''
'''
screen.fill([0,0,0])
for x in range(SIZE[1]):
  print(x)
  for y in range(x):
    if screen.get_at((x,y))[1] != 0:
      continue
    #print("#",end="")
    upperBound = max(x,y)*14
    pools = Collatz.meetPools(x,y,upperBound)
    if len(pools[2]) < 1:
      #screen.set_at((x,y),[255,0,0,255])
      continue
    path = Collatz.browseSegmentedPool(pools[0],pools[2][0])
    path.reverse()
    path.__delitem__(-1)
    path.extend(Collatz.browseSegmentedPool(pools[1],pools[2][0]))
    
    #place = (x,y)
    for i in range(1,len(path)):
      for ii in range(1,i):
        #ii = i - 1
        place = (max(path[i],path[ii]),min(path[i],path[ii]))
      #place = (path[i],getMax(path))
      #place = toSpiral(path[i],startPos=(SIZE[0]//4,SIZE[1]//2))
        if place[0] < SIZE[0] and place[1] < SIZE[1]:
          last = screen.get_at(place)
          screen.set_at(place,[last[0],min(last[1]+1,255),63,255])
    #screen.set_at(place,[int(255*(float(getMin(path))/float(upperBound))**0.25),0,int(255*(float(upperBound - getMax(path))/float(upperBound))**0.25),255])
    
    #screen.set_at((x,y),[0,255 if len([item for item in pools[2] if item > y and item < x]) > 0 else 0, 255 if len([item for item in pools[2] if item > x]) > 0 else 0,255])
  pollEvents()
print("done.")
while True:
  pass
'''
  
print("input takes the form of 4 numbers, seperated by spaces:")
print("overshoot poolSize start target")
print("\nhere are some tips for selecting values:\n")
print("overshoot:")
print("     High values of overshoot (6 and up) help avoid generation failure, but can increase runtime")
print("     recommended values: 3, 4, 5\n")
print("poolSize:")
print("     poolSize controlls the goalPool size, or the number of items branching out from the goal to be cached. Larger pool size decreases runtime, unless pool generation time exceeds solve time. Difficulty of generating pool to size n increases at about n^2")
print("     recommended values: 1 (disabled), 5, 256, 65536\n")
print("start, target:")
print("     start and target are the two values that the solver will attempt to connect. without a sizeable goal pool, solve time increases very fast relative to these input values.")
print("     recommended values for each: up to 100 times the value of poolSize, or up to 10000 if not using pool\n")


while True:
  overshoot, poolSize, num1, num2 = 0, 1, 1, 1
  solver = None
  if ver == "3":
    overshoot, poolSize, num1, num2 = (eval(string) for string in input("overshoot poolSize start target:").split(" "))
  else:
    #overshoot, poolSize, num1, num2 = input("overshoot>"), input("poolSize>"), input("start>"), input("target>")
    #overshoot, poolSize, num1, num2 = (eval(raw_input(promptText + ">")) for promptText in ["overshoot", "poolSize", "start", "target"])
    inputNums = [eval(string) for string in raw_input("overshoot poolsize start target:").split(" ")]
    if len(inputNums) < 4:
      print("please enter all 4 values")
      continue
    overshoot = inputNums[0]
    poolsize = inputNums[1]
    num1 = inputNums[2]
    num2 = inputNums[3]
  pollEvents()
  solver = CollatzSolver(num1,num2,poolSize); pollEvents()
  #print("Tracking: " + track.toString())
  solver.setupGoalForSolve(); pollEvents()
  solver.solve(); pollEvents()
  trimNeg(solver.path); pollEvents()
  #print("option stack: " + str(solver.optionStack)[:360])
  #print("Tracking: " + track.toString())
  print("path: " + trimOut(solver.path,length=360))
  instructions = Solution.pathToInstructions(solver.path)
  if len(solver.goalPool) <= 1:
    print("instructions: " + trimOut(instructions))
    print("re-solve: " + trimOut(Solution.solveInstructions(num1,instructions)))
    #Solution.reverseInstructions(instructions)
    #print("reversed instructions: " + trimOut(instructions))
    #print("re-solve: " + trimOut(Solution.solveInstructions(num2,instructions)))
  else:
    print("instruction solver demo isn't available while using a goal pool")
  drawGuides(num1,num2,solver.upperBound,solver.path)
  #if len(instructions)**0.5 < SIZE[0]//2:
  if len(instructions) <  min(SIZE[0],SIZE[1]) * 0.5:
    drawInstructions(instructions)
    if len(solver.goalPool) <= 1:
      Solution.reverseInstructions(instructions)
      drawInstructions(instructions,reversed=True)
  elif len(solver.path) < (SIZE[0]//2) * (SIZE[1]) * 3:
    #drawSpiral(list(i**(4/3) for i in range(1,int((SIZE[1]*SIZE[0]//2)**(3/4)))))
    drawSpiral(list(item*(SIZE[0]//2)*(SIZE[1])//solver.upperBound for item in solver.path))
  else:
    drawPath(solver.path,solver.upperBound)
    drawRate(solver.upperBound)
  drawFrequencies(solver.path,solver.upperBound)
  print(("\nsuccessfully created " if  solver.done else "failed to create ").upper() + "a path from " + str(solver.start) + " to " + str(solver.goal))
  print("sorted: " + str(sortEnabled) + ", reversed: " + str(reverseEnabled) + ", goal pool size: " + str(len(solver.goalPool)) + ", " + str(len(solver.path)) + " steps, " + str(len(solver.visited)) + " visited\n")
  print("goalPool non-repetition certification: ",end=""); certify(solver.goalPool)
  print("path non-repetition certification: ",end=""); certify(solver.path)
  print("visited non-repetition certification: ",end=""); certify(solver.visited)



