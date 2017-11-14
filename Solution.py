


def __init__(self):
  pass #this is a hideous workaround for compatability with python2
  
def valuesToOperation(a,b):
  return (0 if b*3+1 == a else 1 if b*2 == a else "LO_"+str(a)+"_"+str(b)) if b < a else (2 if a*2==b else 3 if a*3+1==b else "HI_"+str(a)+"_"+str(b)) if b > a else "EQ_"+str(a)
def operationToValue(input, op):
  return (input-1)/3 if op==0 else input/2 if op==1 else input*2 if op==2 else input*3+1 if op==3 else op

def pathToInstructions(path):
    result = []
    for i in range(1,len(path)):
      result.append( valuesToOperation(path[i-1],path[i]))
    return result
    
def solveInstructions(startVal,instructions):
  return  instructionsToPath(startVal,instructions,createPath=False)

def instructionsToPath(startVal,instructions,createPath=True):
  if createPath:
    result = []
  nextVal = startVal
  i = 0
  for operation in instructions:
    nextVal =  operationToValue(nextVal,operation)
    if type(nextVal)==str:
      print(" instructionsToPath: Error at operation " + str(i) + "/" + str(len(instructions)) + ": operation=" + str(operation) + " nextVal=" + str(nextVal))
      print("quitting...")
      exit()
    nextVal = int(nextVal)
    if createPath:
      result.append(nextVal)
    i += 1
  return result if createPath else nextVal
  
def reverseInstructions(path):
  startLength = len(path)
  path.reverse()
  for i in range(len(path)):
    path[i] = 3 - path[i]
  if len(path) != startLength:
    print(" reverseInstructions: argument path changed in length")
    
def instructionsToNestedExpression(startVal,instructions):
  starts = ["(","","","("]
  ends = ["-1)/3","/2","*2","*3+1)"]
  result = str(startVal)
  for operation in instructions:
    result = starts[operation] + result + ends[operation]
  return result

def instructionsToProcedure(startVal,instructions,width=10):
  starts = ["(","","",""]
  ends = ["-1)/3","/2","*2","*3+1"]
  result = ""
  lastVal = startVal
  for operation in instructions:
    addition = starts[operation] + str(lastVal) + ends[operation]
    result  += " " * (width - len(addition)) + addition + "="
    lastVal = eval(addition.replace("/","//"))
    result += str(lastVal) + "\n"
  if width < 0:
    resultSplit = [part for item in result.split("\n") for part in item.split("=") if len(part) > 0]
    width = max([len(part) for part in resultSplit[::2]])
    for i in range(len(resultSplit)):
      if i % 2 == 0:
        resultSplit[i] = " " * (width - len(resultSplit[i])) + resultSplit[i] + "="
      else:
        resultSplit[i] += "\n"
    result = "".join(resultSplit)
  return result