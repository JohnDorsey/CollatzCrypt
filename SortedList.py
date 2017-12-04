#The SortedList class extends the list type, but also keeps track of whether its contents have been sorted. It allows certain items to be appended without disturbing the sorted state.
#If it is sorted, it will use a fast O(log n) search for its __contains__ method. otherwise, it will use a slow O(n) search and give a warning.




from __future__ import print_function

import bisect


class SortedList(list):
  def __init__(self,inputList,warnings=True):
    list.__init__(self,inputList)
    self.warnings = warnings
    self.sorted = len(inputList) <= 1
    if not self.sorted:
      self.verify()
    if not self.sorted:
      self.sort()
  
  """Check whether list is sorted, update self.sorted"""
  def verify(self):
    self.sorted = True
    for i in range(len(self)-1):
      if self[i] > self[i+1]:
        self.sorted = False
        return
  
  """implements __setitem__ to assign a value to an index"""
  def __setitem__(self,index,value):
    list.__setitem__(self,index,value)
    if index > 0:
      if not self[index-1] < self[index]:
        self.sorted = False
        return
    if index < len(self)-1:
      if not self[index+1] > self[index]:
        self.sorted = False
        return
  
  """implements __getitem__ to get a value from an index"""
  def __getitem__(self,index):
    if index < 0:
      return list.__getitem__(self,len(self)+index)
    return list.__getitem__(self,index)
  
  """append and make sure the SortedList is still sorted"""
  def append(self,item):
    if len(self) > 0 and item < self[-1]:
      self.sorted = False
    list.append(self,item)
  
  """extend and make sure the SortedList is still sorted"""
  def extend(self,items):
    if len(items) < 1:
      return
    if self.sorted:
      items.sort()
      if len(self) >= 1:
        if (items[0] < self[-1]):
          self.sorted = False
    list.extend(self,items)
  
  """sort and update self.sorted"""
  def sort(self,):
    if not self.sorted:
      list.sort(self)
      self.sorted = True
  
  """use a fast search if sorted. if not sorted, give a warning if warnings are enabled"""
  def __contains__(self,value):
    if not self.sorted:
      if self.warnings:
        print("!",end="")
      self.sort()
    if self.sorted:
      index = bisect.bisect_left(self,value)
      return len(self) > 0 and value >= self[0] and value <= self[-1] and (index != len(self) and self[index] == value)
    print("major error")
    raise ValueError
      
  """empty the SortedList"""
  def clear(self):
    del self[:]
    self.sorted = True
