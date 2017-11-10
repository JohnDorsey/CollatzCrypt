
from __future__ import print_function

import time
from SortedList import *
from ListTools import *
print("Collatz.py initialized")



def meetPools(start,goal,upperBound):
  startPool = [[],SortedList([start])]
  goalPool = [[],SortedList([goal])]
  overlapByStart = []
  overlapByGoal = []
  overlapCenter = []
  startFull = False
  goalFull = False
  while True:
    print("s",end="")
    startFull = expandSegmentedPool(start,startPool,upperBound)
    print("i",end="")
    overlapByStart = intersect(startPool[-1],goalPool[-1])
    if len(overlapByStart) > 0: break
    print("g",end="")
    goalFull = expandSegmentedPool(goal,goalPool,upperBound)
    print("i",end="")
    overlapByGoal = intersect(startPool[-2],goalPool[-1])
    if len(overlapByGoal) > 0: break
    print("i",end="")
    overlapCenter = intersect(startPool[-1],goalPool[-1])
    if len(overlapCenter) > 0: break
    if goalFull or startFull:  break
  return (startPool, goalPool, [relevant for relevant in [overlapByStart,overlapByGoal,overlapCenter] if len(relevant) > 0])

def generatePoolEdgewise(around,numItems,upperBound):
  startTime = time.clock()
  pool = [[],SortedList([around])]
  poolSize = lambda: getSum(list(len(generation) for generation in pool))
  while poolSize() < numItems:
    shouldStop = expandSegmentedPool(around,pool,upperBound)
    if shouldStop:
      break
  result = desegment(pool,drain=True)
  print("generatePoolEdgewise took " + str(time.clock() - startTime) + " seconds")
  return result
  
def desegment(pool,drain=False):
  result = []
  i = len(pool) -1
  while i > 0:
    result.extend(pool[i])
    if drain:
      pool.__delitem__(len(pool)-1)
    i -= 1
  result.sort()
  preDedupeLength = len(result)
  dedupe(result)
  print("desegmenter had to remove " + str(preDedupeLength - len(result)) + " items")
  return result
  
  
def expandSegmentedPool(around,pool,upperBound):
  pool.append( poolExpansion(pool[-1],around,pool[-2],upperBound))
  if len(pool[-1]) == 0:
    print("the pool is full at iteration " + str(len(pool)-2))
    return True
  #pool[-1].sort()
  #dedupe(pool[-1])
  print("iteration " + str(len(pool)-2) + ": added " + str(len(pool[-1])) + " items to pool")
  return False
  
    
def generatePool(around,numItems,upperBound):
  startTime = time.clock()
  pool = SortedList([around])
  extension = SortedList([around])
  iter = 0
  lastLength = 0
  while len(pool) < numItems:
    extension =  poolExpansion(extension,around,pool,upperBound) #iterating on only the last iteration's extension decreases work complexity
    if len(extension) == 0:
      print("the pool is full, at just " + str(len(pool)) + " items")
      numItems = -1
    lastLength = len(pool)
    print(".",end="")
    pool.extend(extension)
    pool.sort()
    dedupe(pool)
    print("iteration " + str(iter) + ": added " + str(len(pool)-lastLength) + "/" + str(len(extension)) + " items to pool, it now has " + str(len(pool)) + "/" + str(numItems))
    iter += 1
  print("generatePool took " + str(time.clock() - startTime) + " seconds")
  return pool

def poolExpansion(startBatch,goal,exclusions,upperBound):
  stopAt = len(startBatch)
  result = SortedList([])
  i = 0
  while i < stopAt:
    result.extend(optionsFrom(startBatch[i],goal,exclusions,upperBound))
    i += 1
  print("/",end="")
  result.sort()
  print("&",end="")
  dedupe(result)
  return result

def optionsFrom(here,goal,exclusions,upperBound,doSort=False,doReverse=False,invertExclusions=False):
#    print("options for " + str(here) + ": ",end="")
  options = []
  if here > 1:
    if ((here - 1.0) / 3.0) % 1.0 == 0.0:
      options.append((here - 1) // 3)
#      else:
#        track.discardedOptions["nonintegral3"] += 1
    if (here % 2.0 == 0):
      options.append(here // 2)
#      else:
#        track.discardedOptions["nonintegral2"] += 1
  if here * 2 < upperBound:
    options.append(here * 2)
    if here * 3 < upperBound:
      options.append(here * 3 + 1)
#      else:
#        track.discardedOptions["overshoot3"] += 1
#    else:
#      track.discardedOptions["overshoot2"] += 1
#      track.discardedOptions["overshoot3"] += 1
  result = []
#    print(str(options) +", keeping ",end="")
  for option in options:
    if not (exclusions.__contains__(option) != invertExclusions):
      result.append(option)
#      else:
#        track.discardedOptions["duplicate"] += 1
  if doSort:
    sortedSortByClosest(result, goal)
  if doReverse:
    result.reverse()
#    track.discardedOptions["non"] += len(result)
#    print(str(result))
  return result

 
    
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
        
def browseSegmentedPool(pool,endPoint,drain=False):
  index = len(pool) - 1
  result = [endPoint]
  while index > 1:
    toAdd = optionsFrom(result[-1],100,pool[index-1],int(max(endPoint,pool[1][0])*7),invertExclusions=True)
    if drain:
      pool.__delitem__(len(pool))
    if len(toAdd) > 1:
      print("the step to be added was too long: " + str(toAdd))
    if len(toAdd) < 1:
      print("the step to be added was empty")
      break
    result.append(toAdd[0])
    index -= 1
  result.reverse()
  return result
  
