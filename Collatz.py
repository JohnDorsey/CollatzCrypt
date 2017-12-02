
from __future__ import print_function

import time
from SortedList import *
from ListTools import *
from SparseList import *
print("Collatz.py initialized")

def solve(start,goal,upperBound,log=False,preview=None):
  while True:
    pools = meetPools(start,goal,upperBound,sparse=(max(start,goal)>2**16),log=log)
    if len(pools[2]) < 1:
      print("raising upperBound from " + str(upperBound),end="")
      upperBound += int(upperBound * 0.75)
      print(" to " + str(upperBound))
      continue
    break
  meetingPoint = max(pools[2])
  print("midpoint" + ("s are " + str(pools[2]) + ", choosing " if len(pools[2]) > 1 else " is ") + str(meetingPoint))
  if preview:
    lengths = [(item.totalLength()-2 if isinstance(item,SparseList) else len(item)) for item in pools[0:3]]
    path = [start] + ([-1] * lengths[0]) + [meetingPoint] + ([-1] * lengths[1]) + [goal]
    preview(path)
  path = browseSegmentedPool(pools[0],meetingPoint,drain=True)
  path.reverse()
  return path[:-1] + browseSegmentedPool(pools[1],meetingPoint,drain=True), upperBound
  
def meetPools(start,goal,upperBound,sparse=False,log=False):
  startPool = [SortedList([]),SortedList([start])]
  goalPool = [SortedList([]),SortedList([goal])]
  if sparse:
    startPool = SparseList(startPool,length=8)
    goalPool = SparseList(goalPool,length=8)
  overlapByStart = []
  overlapByGoal = []
  overlapCenter = []
  startFull = False
  goalFull = False
  while True:
    if log: print("s",end="")
    startFull = expandSegmentedPool(start,startPool,upperBound,log=log)
    if log: print("i",end="")
    overlapByStart = intersect(startPool[-1],goalPool[-1])
    if len(overlapByStart) > 0: break
    if log: print("g",end="")
    goalFull = expandSegmentedPool(goal,goalPool,upperBound,log=log)
    if log: print("i",end="")
    overlapByGoal = intersect(startPool[-2],goalPool[-1])
    if len(overlapByGoal) > 0: break
    if log: print("i",end="")
    overlapCenter = intersect(startPool[-1],goalPool[-1])
    if len(overlapCenter) > 0: break
    if goalFull or startFull:  break
  #return (startPool, goalPool, [relevant for relevant in [overlapByStart,overlapByGoal,overlapCenter] if len(relevant) > 0])
  return (startPool, goalPool, [item for test in [overlapByStart,overlapByGoal,overlapCenter] for item in test])

def generatePoolEdgewise(around,numItems,upperBound,numIters=-1,sparse=False,log=True):
  startTime = time.clock()
  pool = [SortedList([]),SortedList([around])]
  if sparse:
    pool = SparseList(pool)
  poolSize = lambda: sum(len(generation) for generation in pool)
  while (poolSize() < numItems) if numIters < 0 else ((pool.totalLength() if sparse else len(pool))-2 < numIters):
    shouldStop = expandSegmentedPool(around,pool,upperBound,log=log)
    if shouldStop:
      break
  #result = desegment(pool,drain=True)
  if log: print("generatePoolEdgewise took " + str(time.clock() - startTime) + " seconds")
  return pool
  
def desegment(pool,drain=False,doDedupe=True):
  result = []
  i = len(pool) -1
  while i >= 0:
    result.extend(pool[i])
    if drain:
      pool.__delitem__(len(pool)-1)
    i -= 1
  result.sort()
  preDedupeLength = len(result)
  if doDedupe:
    dedupe(result)
  print("deseg removed " + str(preDedupeLength - len(result)) + " items")
  return result
  
  
def expandSegmentedPool(around,pool,upperBound,log=False):
  pool.append(poolExpansion(pool[-1],around,pool[-2],upperBound))
  if len(pool[-1]) == 0:
    if log: print("xseg ful " + str(len(pool)-2))
    return True
  #pool[-1].sort()
  #dedupe(pool[-1])
  if log: print("iteration " + str(len(pool)-2) + ": added " + str(len(pool[-1])) + " items to pool")
  return False
  
    
def generatePool(around,numItems,upperBound,numIters=-1):
  startTime = time.clock()
  pool = SortedList([around])
  extension = SortedList([around])
  iter = 0
  lastLength = 0
  while (len(pool) < numItems and numIters < 0) or iter < numIters:
    extension =  poolExpansion(extension,around,pool,upperBound) #iterating on only the last iteration's extension decreases work complexity
    if len(extension) == 0:
      print("pool full at " + str(len(pool)) + " items")
      numItems = -1
    lastLength = len(pool)
    print(".",end="")
    pool.extend(extension)
    pool.sort()
    dedupe(pool)
    print("iter " + str(iter) + ": added " + str(len(pool)-lastLength) + "/" + str(len(extension)) + " items to pool, it now has " + str(len(pool)) + "/" + str(numItems))
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
  #print("/",end="")
  result.sort()
  #print("&",end="")
  dedupe(result)
  return result
  
def optionsFrom(here,goal,exclusions,upperBound,doSort=False,doReverse=False,invertExclusions=False):
#    print("options for " + str(here) + ": ",end="")
  if here > upperBound:
    print("starting point greater than upperBound")
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
    if here * 3 + 1 < upperBound:
      options.append(here * 3 + 1)
#      else:
#        track.discardedOptions["overshoot3"] += 1
#    else:
#      track.discardedOptions["overshoot2"] += 1
#      track.discardedOptions["overshoot3"] += 1
  result = []
#    print(str(options) +", keeping ",end="")
  for option in options:
    if (exclusions.__contains__(option) == invertExclusions):
      result.append(option)
#      else:
#        track.discardedOptions["duplicate"] += 1
  if doSort:
    result = sorted(result, key = lambda n: abs(goal-n), reverse=doReverse)
  elif doReverse:
    result.reverse()
#    track.discardedOptions["non"] += len(result)
#    print(str(result))
  return result

        
def browseSegmentedPool(pool,endPoint,drain=False,depth=1,log=False):
  index = len(pool) - 1
  result = [endPoint]
  sparse = isinstance(pool,SparseList)
  if log: id = ("  " * depth) + "(" + str(pool) + "<-" + str(endPoint) + ")"
  while index > 1:
    if sparse:
      tree = generatePoolEdgewise(result[-1],-1,result[-1]*(7**pool.spacings[index]),numIters=pool.spacings[index],log=False)
      if log: print(id + " tree:" + str(tree))
      intersections = intersect(tree[-1],pool[index-1])
      if len(intersections) == 0:
        toAdd = []
      else:
        toAdd = browseSegmentedPool(tree,min(intersections),drain=False,depth=depth+1)
        toAdd.reverse()
        toAdd = toAdd[1:]
      if log: print(id + " tree toAdd:" + str(result) + "+" + str(toAdd))
    else:
      toAdd = optionsFrom(result[-1],1,pool[index-1],int(max(endPoint,pool[1][0])*99999),invertExclusions=True)
      if log: print(id + " toAdd:" + str(result) + "+" + str(toAdd))
    if len(toAdd) < 1:
      if index > 2:
        print("browseSegementedPool (sparse="+str(sparse)+") failed at index " + str(index) + " of " + str(len(pool)))
      break
    if sparse:
      result.extend(toAdd)
    else:
      result.append(min(toAdd))
    if drain:
      pool.__delitem__(len(pool)-1)
    index -= 1
  #result.reverse()
  if result == None:
    raise TypeError
  return result
  
