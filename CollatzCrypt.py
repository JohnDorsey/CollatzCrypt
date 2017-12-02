
from __future__ import print_function
print("Hello!")

'''+++++++++++++++++++++++++++++++'''
#Configure me:

textMode = False

trimOutput = True

sortEnabled = True
reverseEnabled = False
logarithmicOutputEnabled = True
drawType = "type" #"direct", "type", "exact"


SIZE = (1280,640)
fontSize = 14
fontName = "courier"
'''-------------------------------------------------------'''


import sys
ver = sys.version[:1]
if len(sys.argv) > 1:
  print("args: " + str(sys.argv[1:]))
  title = sys.argv[1]
else:
  title = "CollatzCrypt"

from SortedList import *
from SortedStack import *
from ListTools import *
from StackedSolver import *
import Solution
import Collatz

import math
import time


if not textMode:
  try:
    print("importing pygame...")
    import pygame
    print("initializing pygame...")
    pygame.init()
    print("creating window...")
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(title)
    font = pygame.font.SysFont(fontName,fontSize)
    #from jdev import *
  except:
    print("couldn't find pygame module. running in text mode...")
    if ver == "3":
      print("to view the full output, install pygame by running python's package manager directly from the shell or command prompt.")
      print("windows command prompt or linux shell:")
      print("    pip install pygame")
    textMode = True


alpha = 24
colors = {"down":[210,0,255,alpha], "up":[0,255,192,alpha],"err":[127,0,0,alpha],"large":[220,220,0,alpha],"small":[15,144,220,alpha],0:[192,0,35,alpha],1:[124,192,0,alpha],2:[35,0,192,alpha],3:[0,192,124,alpha],"hud":[255,255,255,alpha],"guide":[191,31,31,alpha]}

overshoot = 4

if logarithmicOutputEnabled:
  screenv = lambda v, upperBound: SIZE[1] - min(max(int(float(SIZE[1]-1) * ((1.0*math.log(v+4,1.0025) / math.log(upperBound+4,1.0025)))) + 2,0),SIZE[1]-1)
else:
  screenv = lambda v, upperBound: SIZE[1] - min(max(int(float(SIZE[1]-4) * ((v / upperBound))) + 2,0),SIZE[1]-1)
#





print("configuring drawing methods...")

if textMode:
  def drawRate(*args,**kwargs): pass
  def drawGuides(*args,**kwargs): pass
  def drawHorizGuide(*args,**kwargs): pass
  def drawPath(*args,**kwargs): pass
  def drawSpiral(*args,**kwargs): pass
  def drawFrequencies(*args,**kwargs): pass
  def drawInstructions(*args,**kwargs): pass
  def pollEvents(*args,**kwargs): pass
  def clear(*args,**kwargs): pass
else:
  def drawRate(upperBound):
    last, current = (0,0), (0,0)
    for i in range(int(SIZE[1]**0.6666)):
      i = int(i**1.5)
      last = current
      current = ((i)*(SIZE[0]/SIZE[1]),screenv(upperBound*i/(1.0*SIZE[1]),upperBound))
      pygame.draw.aaline(screen,colors["guide"],last,current,4)
      pygame.display.flip()
    pollEvents()

  def drawGuides(guidesToDraw,upperBound):
    clear()
    for key in guidesToDraw:
      drawHorizGuide(screenv(guidesToDraw[key],upperBound),name=(key+": "+str(guidesToDraw[key])))
    pollEvents()

  def drawHorizGuide(height,name=""):
    pygame.draw.aaline(screen,colors["guide"],(0,height),(SIZE[0],height),1)
    if not name=="":
      screen.blit(font.render(name,False,colors["hud"]),(SIZE[0]-font.size(name)[0]-16,height))

  def drawPath(inputPath,upperBound,label="extrema"):
    deltaPos = float(SIZE[0] * 0.5) / len(inputPath)
    color = "err"
    scale = int(min(deltaPos,64))
    for i in range(len(inputPath)-1):
      if inputPath[i+1] > 0:
        color = colorFrom(drawType,inputPath[i],inputPath[i+1])
        a = (deltaPos*i,screenv(inputPath[i],upperBound))
        b = (deltaPos*(i+1),screenv(inputPath[i+1],upperBound))
        if inputPath[i] > 0:
          pygame.draw.aaline(screen,colors[color],a,b,max(scale//24,1))
        if scale > 8:
          pygame.draw.circle(screen,colors[color],(int(b[0]),int(b[1])),max(scale//8,1))
        if scale > fontSize:
          if (label == "all" or (label == "extrema" and (inputPath[i+1]==max(inputPath[i:i+3]) or inputPath[i+1]==min(inputPath[i:i+3])))):
            screen.blit(font.render(" " +str(inputPath[i+1]),False,colors[color]),(b[0],b[1]-0.5*fontSize+(-1 if b[1]<a[1] else 1)*0.5*fontSize))
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
    scale = SIZE[0] * 0.5 / max(frequencyMap)
    for passNum in range(1,3):
      for i in range(len(frequencyMap)-4):
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
        print("Quitting...")
        pygame.display.quit()
        exit()
        
  def clear():
    screen.fill([0,0,0])
      
    
   
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
  
print("ready.\n\n\n\n")
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
clear()
for x in range(SIZE[1])[::-1]:
  print(x)
  for y in range(x)[::-1]:
    if screen.get_at((x,y))[2] != 0:
      continue
    #print("#",end="")
    upperBound = max(x,y)*5
    path = Collatz.solve(x,y,upperBound)
    
    #place = (x,y)
    for i in range(1,len(path)):
      for ii in range(1,i):
        #ii = i - 1
        place = (max(path[i],path[ii]),min(path[i],path[ii]))
      #place = (path[i],max(path))
      #place = toSpiral(path[i],startPos=(SIZE[0]//4,SIZE[1]//2))
        if place[0] < SIZE[0] and place[1] < SIZE[1]:
          last = screen.get_at(place)
          if last[2] != 0:
            continue
          screen.set_at(place,[last[0],min((64*max(path[i:ii+1]+[upperBound])//upperBound),255),63,255])
    #screen.set_at(place,[int(255*(float(min(path))/float(upperBound))**0.25),0,int(255*(float(upperBound - max(path))/float(upperBound))**0.25),255])
    
    #screen.set_at((x,y),[0,255 if len([item for item in pools[2] if item > y and item < x]) > 0 else 0, 255 if len([item for item in pools[2] if item > x]) > 0 else 0,255])
  pollEvents()
print("done.")
while True:
  pass
'''
  
print("input takes the form of 4 numbers, seperated by spaces:")
print("start goal overshoot poolSize")
print("\nif poolSize is omitted, the expanding pool solver will be used")
print("\nhere are some tips for selecting values:\n")
print("overshoot:")
print("     High values of overshoot (10 and up) help avoid generation failure, but can increase runtime")
print("     recommended values: 3, 5, 7\n")
print("poolSize:")
print("     poolSize controlls the goalPool size, or the number of items branching out from the goal to be cached. Larger pool size decreases runtime, unless pool generation time exceeds solve time. Difficulty of generating pool to size n increases more quickly than n")
print("     recommended values: 1 (disabled), 5, 256, 65536\n")
print("start, goal:")
print("     start and goal are the two values that the solver will attempt to connect. without a sizeable goal pool, solve time increases very fast relative to these input values.")
print("     recommended values for each: up to 100 times the value of poolSize, or up to 10000 if poolSize is 1\n")


while True:
  num1, num2, overshoot, poolSize  = 0, 1, 1, 1
  solver = None
  inputNums = [-1,-1,-1,-1]
  inputNums = [eval(string) for string in ((input if ver=="3" else raw_input)("start goal overshoot poolSize:")).split(" ")]
  if len(inputNums) < 3:
    print("please enter 3 or 4 values: ")
    print("    3 values are unpacked as (start, goal, overshoot) to run the expanding pool solver")
    print("    4 values are unpacked as (start, goal, overshoot, poolSize) to run the stacked solver")
    continue
  num1, num2, overshoot = inputNums[0], inputNums[1], inputNums[2]
  pollEvents()
  if len(inputNums) == 3:
    poolSize = 1
    solver = Solver(num1,num2,overshoot)
  else:
    poolSize = inputNums[3]
    solver = StackedSolver(num1,num2,overshoot,poolSize)
  clear()
  pollEvents()
  def peek(path): clear(); drawPath(path,solver.upperBound); pollEvents()
  solver.solve(preview=peek); pollEvents()
  pollEvents()
  
  #print("option stack: " + str(solver.optionStack)[:360])
  print("path: " + trimOut(solver.path,length=360))
  instructions = Solution.pathToInstructions(solver.path)
  #if poolSize <= 1:
  print("instructions: " + trimOut(instructions,length=360))
  print("re-solve: " + str(Solution.solveInstructions(num1,instructions)))
  #else:
  #  print("instruction solver demo isn't available while using a goal pool")
  drawGuides({"upperBound":solver.upperBound,"min":min(solver.path),"max":max(solver.path)},solver.upperBound)
  if len(instructions) <  min(SIZE[0],SIZE[1]) * 0.5 and False:
    drawInstructions(instructions)
    if poolSize <= 1:
      Solution.reverseInstructions(instructions)
      drawInstructions(instructions,reversed=True)
  elif len(solver.path) < (SIZE[0]//2) * (SIZE[1]) * 3 and False:
    #drawSpiral(list(i**(4/3) for i in range(1,int((SIZE[1]*SIZE[0]//2)**(3/4)))))
    drawSpiral(list(item*(SIZE[0]//2)*(SIZE[1])//solver.upperBound for item in solver.path))
  else:
    drawPath(solver.path,solver.upperBound)
    drawRate(solver.upperBound)
  drawFrequencies(solver.path,solver.upperBound)
  print(("\nsuccessfully created " if  Solution.pathIsValid(solver.path) else "failed to create ").upper() + "a path from " + str(solver.start) + " to " + str(solver.goal))
  print("sorted: " + str(sortEnabled) + ", reversed: " + str(reverseEnabled) + ", " + str(len(solver.path)) + " steps",end="")
  if isinstance(solver,StackedSolver):
    print(", " + str(len(solver.visited)) + " visited\n")
    print("visited non-repetition certification: ",end=""); certify(solver.visited)
    print("goalPool non-repetition certification: ",end=""); certify(solver.goalPool)
  else:
    print("")
  print("path non-repetition certification: ",end=""); certify(solver.path)



