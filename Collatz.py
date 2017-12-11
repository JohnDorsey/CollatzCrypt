
from __future__ import print_function

import time
from SortedList import *
from ListTools import *
from SparseList import *
print("Collatz.py initialized")

"""Choose a mathod to solve between two numbers, and return the path"""
def solve(start,goal,upperBound,log=False,preview=None):
  while True:
    pools = meetPools(start,goal,upperBound,sparse=(max(start,goal)>2**16),log=log)
    if len(pools[2]) < 1:
      print("raising upperBound from " + str(upperBound),end="")
      upperBound += int(max(upperBound,3) * 0.75)
      print(" to " + str(upperBound))
      continue
    break
  meetingPoint = max(pools[2])
  print("segments of sizes " + str(len(pools[0][-1])) + " and " + str(len(pools[1][-1])) + " have met.")
  print("midpoint" + ("s are " + str(pools[2]) + ", choosing " if len(pools[2]) > 1 else " is ") + str(meetingPoint))
  if preview:
    lengths = [(item.totalLength()-2 if isinstance(item,SparseList) else len(item)) for item in pools[0:3]]
    path = [start] + ([-1] * lengths[0]) + [meetingPoint] + ([-1] * lengths[1]) + [goal]
    preview(path)
  path = browseSegmentedPool(pools[0],meetingPoint,drain=True)
  path.reverse()
  return path[:-1] + browseSegmentedPool(pools[1],meetingPoint,drain=True), upperBound
  
"""expand two segmented pools outward from two starting points until they overlap, then return both pools and the values shared between their last iterations. If multiple values are shared, then they are all parts of valid paths between the points, and all those paths have equal lengths. Any of these paths is gauranteed to be the shortest possible path between the two points which does not include any numbers above upperBound"""
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
  return (startPool, goalPool, [item for test in [overlapByStart,overlapByGoal,overlapCenter] for item in test])

"""generate a segmented pool to the specified number of iterations, or the specified number of total items if no iteration count is given."""
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
  if log: print("generatePoolEdgewise took " + str(time.clock() - startTime) + " seconds")
  return pool

"""merge a list of lists into one list, returning it, with options to delete from (drain) the original and remove duplicates"""
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
  
"""take a segmented pool (a list of lists where each list contains all numbers added in that iteration) and add a new segment based on the last 2"""
def expandSegmentedPool(around,pool,upperBound,log=False):
  pool.append(poolExpansion(pool[-1],around,pool[-2],upperBound))
  if len(pool[-1]) == 0:
    if log: print("xseg ful " + str(len(pool)-2))
    return True
  if log: print("iteration " + str(len(pool)-2) + ": added " + str(len(pool[-1])) + " items to pool")
  return False
  
"""generate a pool, limiting the inputs for each iteration to those found in the previous iteration, but not remembering this information (it is continuously desegmented)"""
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

"""All items that can be added in this iteration, given the starting points and a list of exclusions (to avoid duplicates)"""
def poolExpansion(startBatch,goal,exclusions,upperBound):
  stopAt = len(startBatch)
  result = SortedList([])
  i = 0
  while i < stopAt:
    result.extend(optionsFrom(startBatch[i],goal,exclusions,upperBound))
    i += 1
  result.sort()
  dedupe(result)
  return result
  
"""generate all positive bounded integer outcomes of performing the 4 operations on the input number"""
def optionsFrom(here,goal,exclusions,upperBound,doSort=False,doReverse=False,invertExclusions=False):
  if here > upperBound:
    print("starting point greater than upperBound")
  options = []
  if here > 1:
    if ((here - 1.0) / 3.0) % 1.0 == 0.0:
      options.append((here - 1) // 3)
    if (here % 2.0 == 0):
      options.append(here // 2)
  if here * 2 < upperBound:
    options.append(here * 2)
    if here * 3 + 1 < upperBound:
      options.append(here * 3 + 1)
  result = []
  for option in options:
    if (exclusions.__contains__(option) == invertExclusions):
      result.append(option)
  if doSort:
    result = sorted(result, key = lambda n: abs(goal-n), reverse=doReverse)
  elif doReverse:
    result.reverse()
  return result

"""given any item in the final iteration of a segmented pool, select the item from the last iteration which came before it, traveling backwards through the segmented pool until the beginning is reached. Then return the path that was taken"""
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
  if result == None:
    raise TypeError
  return result
  
