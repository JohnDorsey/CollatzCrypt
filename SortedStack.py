


from SortedList import *
    
class SortedStack:
  def __init__(self,inputList,lag=16):
    self.lag = lag
    self.base = SortedList(inputList)
    #self.base = SortedList.__init__(inputList)
   # if self.lag > 8:
    #  self.hat = SortedStack([],lag=self.lag//2)
   # else:
    self.hat = []
    
  def __len__(self):
    return len(self.base) + len(self.hat)
    
  def __str__(self):
    return str(self.base)[:-1] + ", " + str(self.hat)[1:]
    
  def __getitem__(self,index):
    if index < 0:
      return self[len(self)+index]
    return self.base[index] if index < len(self.base) else self.hat[index-len(self.base)]
    
  def __setitem__(self,index,value):
    #if type(value) != int:
    #  raise TypeError
    if index < 0:
      self[len(self)+index] = value
    if index < len(self.base):
      self.base[index] = value
    else:
      self.hat[index-len(self.base)] = value
      
  def __delitem__(self,index):
    if index < len(self.base):
      self.base.__delitem__(index)
    else:
      self.hat.__delitem__(index-len(self.base))
      if len(self.hat) == 0:
        print("SortedStack hat is gone, base length is " + str(len(self.base)))
  
  def append(self,item):
    #if type(item) != int:
    #  raise TypeError
    if len(self.base)==0 or self.base[-1] < item:
      self.base.append(item)
    else:
      self.hat.append(item)
      
  def extend(self,items):
    for item in items:
      self.append(item)
    
  def sort(self):
    #print("SortedStack.sort() - only the hat of this stack will be sorted;"),
    self.hat.sort()
    #print(" the hat was sorted")
    
  def __contains__(self,value):
    self.adjust()
    if len(self.base) < 1:
      return self.hat.__contains__(value)
    if value > self.base[-1]:
      return False
    return self.hat.__contains__(value) or self.base.__contains__(value)
    
  def adjust(self):
    if len(self.hat) > self.lag:
      #self.hat.sort()
      self.base.extend(self.hat)
      del self.hat[:]
      self.base.sort()
  
  def clear(self):
    self.base.clear()
    del self.hat[:]
