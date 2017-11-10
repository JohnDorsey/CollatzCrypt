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
  
  def verify(self):
    self.sorted = True
    for i in range(len(self)-1):
      if self[i] > self[i+1]:
        self.sorted = False
        return
  
  def __setitem__(self,index,value):
    #if type(value) != int:
    #  raise TypeError
    list.__setitem__(self,index,value)
    if index > 0:
      if not self[index-1] < self[index]:
        self.sorted = False
        return
    if index < len(self)-1:
      if not self[index+1] > self[index]:
        self.sorted = False
        return
  
  def __getitem__(self,index):
    if index < 0:
      return list.__getitem__(self,len(self)+index)
    return list.__getitem__(self,index)
  
  def append(self,item):
    #if type(item) != int:
    #  raise TypeError
    if len(self) > 0 and item < self[-1]:
      self.sorted = False
    list.append(self,item)
  
  def extend(self,items):
    if len(items) < 1:
      return
    '''for item in items:
      if type(item) != int:
        raise ValueError
        return'''
    if self.sorted:
      items.sort()
      if len(self) >= 1:
        if (items[0] < self[-1]):
          self.sorted = False
    list.extend(self,items)
  
  def sort(self,):
    if not self.sorted:
      list.sort(self)
      self.sorted = True
  
  def __contains__(self,value):
    if not self.sorted:
      if self.warnings:
        print("!",end="")
        #raise ValueError
      self.sort()
    if self.sorted:
      #return len(self) > 0 and value >= self[0] and value <= self[-1] and (lambda s, index: index != len(s) and s[index] == value)(self,bisect.bisect_left(self,value))
      index = bisect.bisect_left(self,value)
      return len(self) > 0 and value >= self[0] and value <= self[-1] and (index != len(self) and self[index] == value)
    print("major error")
    raise ValueError
      
  def clear(self):
    del self[:]
    self.sorted = True
