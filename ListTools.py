
from __future__ import print_function
from SortedList import *



def distance(vect1,vect2):
  if len(vect1) > 2 or len(vect2) > 2:
    return sum((vect1[i]-vect2[i])**2 for i in range(min(len(vect1),len(vect2))))**(1.0/min(len(vect1),len(vect2)))
  return ((vect1[0]-vect2[0])**2 + (vect1[1]-vect2[1])**2)**0.5


def dedupe(inputList):
  offset = 1
  i = 0
  length = len(inputList)
  while i < length - offset:
    while i + offset < length and inputList[i] == inputList[i+offset]:
      offset += 1
    if i + offset < length:
      inputList[i+1] = inputList[i+offset]
    elif inputList[i] == inputList[i + offset - 1]:
      i -= 1
    i += 1
  for ii in range(length - i - 1):
    inputList.__delitem__(length - ii - 1)
  inputList.sort()

    
def intersect(inputList1, inputList2):
  if len(inputList1) > len(inputList2):
    if not isinstance(inputList1,SortedList):
      print("IntersectSoSlow",end="")
    return [item for item in inputList2 if inputList1.__contains__(item)]
  else:
    if not isinstance(inputList2,SortedList):
      print("IntersectSoSlow",end="")
    return [item for item in inputList1 if inputList2.__contains__(item)]

def certify(inputList):
  repeats = []
  lengths = []
  inputList.sort()
  i = 0
  while (i < len(inputList) - 1):
    if inputList[i] == inputList[i+1]:
      runLength = 1
      for ii in range(2,len(inputList)-i):
        if not inputList[i] == inputList[ii]:
          runLength = ii
          break
      repeats.append(i)
      lengths.append(runLength)
      i += runLength - 1
    i += 1
  print(str(len(repeats)) + " runs",end="")
  if len(lengths) > 0:
    print(", " + str(max(lengths)) + " max, " + str(sum(lengths)) + " total")
  else:
    print("")

def avg(input): #accepts generators
  result, i = 0, 1
  for item in input:
    result = (1-(1.0/i))*result + (1.0/i)*item
    i += 1
  return result
  
def blur(inputList,clamp=1,radius=10,blend=1,depth=1):
  result = list(inputList)
  for d in range(depth):
    inputList = list(result)
    for w in range(0,len(inputList)):
      sampleRange = (max(w-radius,0),min(w+radius+1,len(result)-1))
      result[w] = avg(inputList[sampleRange[0]:sampleRange[1]] + ([inputList[0]]*abs(min(0,w-radius-2))+[inputList[-1]]*min(0,1+radius+w-len(inputList))))
    for ci in [0,-1]:
      result[ci] = result[ci]*(1-clamp) + inputList[ci]*clamp
  return [result[i]*blend + inputList[i]*(1-blend) for i in range(len(result))]
      
def trimNeg(inputList):
  length = len(inputList)
  for i in range(length):
    if inputList[length-i-1] < 0:
      inputList.__delitem__(length-i-1)
    else:
      return


 
    
def sortedSortByClosest(contestants,target):
  
  if len(contestants) <= 1:
    return
  if contestants[-1] < target:
    contestants.reverse()
    return
  if contestants[0] > target:
    return
  if len(contestants) == 2 and contestants[1] - target < target - contestants[0]:
    contestants.reverse()
    return
  sortByClosest(contestants,target)
   
def sortByClosest(contestants,target):
  temp = 0
  for passNum in range(len(contestants)-1):
    for i in range(len(contestants) - 1):
      if abs(contestants[i]-target) > abs(contestants[i+1]-target):
        temp = contestants[i]
        contestants[i] = contestants[i+1]
        contestants[i+1] = temp