
from __future__ import print_function
print("Hello!")

'''+++++++++++++++++++++++++++++++'''
#Configure me:

textMode = False
SIZE = (1280,640)
fontSize = 14
fontName = "courier"

trimOutput = True

logarithmicOutputEnabled = True
drawType = "type" #"direct", "type", "exact"


sortEnabled = True
reverseEnabled = False
textInputLength = 5
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
import Key

import math
import time

charSet = Key.B26

if not textMode:
  try:
    print("importing pygame...")
    import pygame
    print("initializing pygame...")
    pygame.init()
    print("creating window...")
    if __name__=="__main__":
      screen = pygame.display.set_mode(SIZE)
      pygame.display.set_caption(title)
    font = pygame.font.SysFont(fontName,fontSize)
    InterfaceFont = pygame.font.SysFont(fontName,fontSize*2)
    from VisualText import *
    #from jdev import *
  except:
    print("couldn't find pygame module. running in text mode...")
    textMode = True
    if ver == "3":
      print("to view the full output, install pygame by running python's package manager directly from the shell or command prompt.")
      print("windows command prompt or linux shell:")
      print("    pip install pygame")


alpha = 24
colors = {"down":[210,0,255,alpha], "up":[0,255,192,alpha],"err":[127,0,0,alpha],"large":[220,220,0,alpha],"small":[15,144,220,alpha],0:[192,0,35,alpha],1:[124,192,0,alpha],2:[35,0,192,alpha],3:[0,192,124,alpha],"hud":[255,255,255,alpha],"guide":[191,31,31,alpha]}

overshoot = 4

if logarithmicOutputEnabled:
  screenv = lambda v, upperBound: SIZE[1] - min(max(int(float(SIZE[1]-1) * ((1.0*math.log(v+4,1.0025) / math.log(upperBound+4,1.0025)))) + 2,0),SIZE[1]-1)
else:
  screenv = lambda v, upperBound: SIZE[1] - min(max(int(float(SIZE[1]-4) * ((v / upperBound))) + 2,0),SIZE[1]-1)
#




def getTextInput(text):
  return (input if ver=="3" else raw_input)(text)

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
  def getInput(text):
    return getTextInput(text)
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
    message = str(Solution.pathToInstructions(inputPath)).replace(" ","")[:2*SIZE[0]//fontSize-8]
    for i in range(len(message)):
      if font.size(message + "...")[0] > SIZE[0]:
        message = message[:-8]
      else:
        break
    if not message[-1] == "]":
      message += "..."
    screen.blit(font.render(message,False,colors["hud"]),(16,0.5*font.size("|")[1]))
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
    dodge = lambda trip, amt: [int(chan*(1-amt) + 255*amt) for chan in trip]
    frequencyMap = [0 for i in range(SIZE[1]+8)]
    for point in inputPath:
      #print(screenv(point))
      if point > 0:
        frequencyMap[screenv(point,upperBound)] += 1
    frequencyMap = blur(frequencyMap,radius=4,depth=3)
    scale = SIZE[0] * 0.5 / max(max(frequencyMap),0.5**20)
    for passNum in range(1,16):
      frequencyMap = blur(frequencyMap,radius=1+int(passNum**1.1),depth=1)
      dodgedColors = {}
      for key in colors:
        dodgedColors[key] = dodge(colors[key],(passNum/20)**2)
      for i in range(len(frequencyMap)-8):
        pygame.draw.aaline(screen,[int(channel*((passNum/16)**1.22*0.9+0.1)) for channel in dodgedColors["down" if frequencyMap[i+8]<frequencyMap[i] else "up"]],(SIZE[0]*0.5+frequencyMap[i]*scale,i),(SIZE[0]*0.5+frequencyMap[i+8]*scale,i+8),3)
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
  
  def getInput(text):
    return getTextInput(text)
  
      
    
   
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



def investigate(solver,alphabet=None):
  show = lambda num: str(num) + (" (" + Key.toCharArr(num,alphabet) + ")" if alphabet else "")
  if not solver.done:
    print("FAILED TO CREATE a path between " + show(solver.start) + " and " + show(solver.goal) + ": the solver never finished.")
  elif not Solution.pathIsValid(solver.path):
    print("FAILED TO CREATE a path between " +  show(solver.start) + " and " + show(solver.goal) + ": the solution is not valid.")
  else:
    print("\nSUCCESSFULLY CREATED a path from " + show(solver.start) + " to " + show(solver.goal))
  if len(solver.path) == 0:
    solver.path = [0]
  print("path: " + trimOut(solver.path,length=360))
  instructions = Solution.pathToInstructions(solver.path)
  print("instructions: " + trimOut(instructions,length=360))
  print("Encrypted data:" + show(Solution.instructionsToNumber(instructions)))
  print("re-solve: " + str(show(Solution.solveInstructions(solver.path[0],instructions))))
  drawGuides({"min":min(solver.path),"max":max(solver.path)},solver.upperBound)
  drawRate(solver.upperBound)
  drawFrequencies(solver.path,solver.upperBound)
  drawPath(solver.path,solver.upperBound)
  print("sorted: " + str(sortEnabled) + ", reversed: " + str(reverseEnabled) + ", " + str(len(solver.path)) + " steps",end="")
  if isinstance(solver,StackedSolver):
    print(", " + str(len(solver.visited)) + " visited\n")
    print("visited non-repetition certification: ",end=""); certify(solver.visited)
    print("goalPool non-repetition certification: ",end=""); certify(solver.goalPool)
  else:
    print("")
  print("path non-repetition certification: ",end=""); certify(solver.path)

def directNumberInterfaceDual():
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
    try:
      inputNums = [eval(string) for string in (getInput("\n\nstart goal overshoot poolSize:")).split(" ")]
    except EOFError:
      exit()
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
    pollEvents()
    def peek(path): clear(); drawPath(path,solver.upperBound); pollEvents()
    solver.solve(preview=peek); pollEvents()
    clear()
    if solver.done:
      investigate(solver)


def getTextInput(text):
  return Key.conform((input if ver=="3" else raw_input)(text),charSet)

def textInterface():
  if not textMode:
    ft = FixedTerminal([Field("Enter a key: ",default="c"),Field("Enter text to encrypt: ",default="b")],pygame,InterfaceFont,screen)
  while True:
    if textMode:
      try:
        text1 = getTextInput("\n\nEnter a key:")
        if text1 == "": return
        text2 = getTextInput("Enter text to encrypt:")
        if text2 == "": return
      except EOFError:
        exit()
    else:
      ft.getInputs()
      text1, text2 = ft.get_values()
    text1, text2 = text1[:5], text2[:6]
    num1 = Key.fromCharArr(text1,charSet)
    num2 = Key.fromCharArr(text2,charSet)
    overshoot = 7
    solver = Solver(num1,num2,overshoot)
    pollEvents()
    def peek(path): clear(); drawPath(path,solver.upperBound); pollEvents()
    solver.solve(preview=peek); pollEvents()
    clear()
    if solver.done:
      investigate(solver,alphabet=charSet)

def decryptInterface():
  while True:
    return

if __name__=="__main__":
  textInterface()