
from __future__ import print_function
from SortedList import *

def getSum(inputList):
  total = 0
  for item in inputList:
    total += item
  return total
  
  
def getMax(inputList):
  if len(inputList) < 1:
    return 0
  record = inputList[0]
  for item in inputList:
    if item > record:
      record = item
  return record
  
def getMin(inputList):
  record = inputList[0]
  for item in inputList:
    if item < record:
      record = item
  return record


def distance(vect1,vect2):
  if len(vect1) > 2 or len(vect2) > 2:
    return getSum([(vect1[i]-vect2[i])**2 for i in range(min(len(vect1),len(vect2)))])**(1.0/min(len(vect1),len(vect2)))
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
  print(str(len(repeats)) + " runs, " + str(getMax(lengths)) + " max, " + str(getSum(lengths)) + " total")

  
      
def trimNeg(inputList):
  length = len(inputList)
  for i in range(length):
    if inputList[length-i-1] < 0:
      inputList.__delitem__(length-i-1)
    else:
      return
    