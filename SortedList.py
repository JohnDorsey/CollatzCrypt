from __future__ import print_function

import bisect


class SortedList(list):
  def __init__(self,inputList):
    list.__init__(self,inputList)
    self.sorted = False
    self.warnings = False
    if len(inputList) <= 1:
      self.sorter = True
  
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
    if self.sorted:
      #return len(self) > 0 and value >= self[0] and value <= self[-1] and (lambda s, index: index != len(s) and s[index] == value)(self,bisect.bisect_left(self,value))
      index = bisect.bisect_left(self,value)
      return len(self) > 0 and value >= self[0] and value <= self[-1] and (index != len(self) and self[index] == value)
    else:
      if self.warnings:
        print("!",end="")
      return list.__contains__(self,value)
      
  def clear(self):
    del self[:]
    self.sorted = True
