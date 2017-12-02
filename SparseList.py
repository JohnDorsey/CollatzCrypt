

class SparseList(list):
  def __init__(self,inputList,startRun=2,endRun=2,length=10):
    list.__init__(self,inputList)
    self.spacings = [1 for i in range(len(inputList))]
    self.startRun, self.endRun, self.length = startRun, endRun, length
    
  def append(self,item):
    list.append(self,item)
    self.spacings.append(1)
    while len(self) > self.length:
      self.adjust()
    
  def bestToRemove(self):
    recordLowIndex = self.startRun
    space = self.spacings[recordLowIndex] + self.spacings[recordLowIndex+1]
    recordLow = space
    for i in range(self.startRun+1,len(self)-self.endRun):
      space = self.spacings[i] + self.spacings[i+1]
      if space < recordLow:
        recordLow = space
        recordLowIndex = i
    return recordLowIndex
  
  def totalLength(self):
    return sum(self.spacings)
    
  def __delitem__(self,index):
    if index < len(self.spacings) - 1:
      self.spacings[index+1] += self.spacings[index]
    self.spacings.__delitem__(index)
    list.__delitem__(self,index)
    
  def adjust(self):
    if len(self) < self.startRun + self.endRun:
      print("SparseList cannot be made any smaller")
      return
    self.__delitem__(self.bestToRemove())
    
    