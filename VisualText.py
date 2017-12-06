

import time



class Field:
  def __init__(self,text,value="",default="",maxLength=5):
    self.text = text
    self.default = default
    self.value = value
    self.recent = [self.value]
    self.pointer = 0
    self.focused = False
    self.maxLength = maxLength
    
  def get_value(self):
    return self.value if not self.value == "" else self.default
    
  def __str__(self):
    return self.text+self.value
    
  def terpKey(self,key):
    self.focused = True
    if key == 8: #backspace
      if len(self.value) > 0:
        self.value = self.value[:-1]
    elif key >= 97 and key <= 122: #alphabetical
      self.value += chr(key)
    elif key == 273: #up
      self.pointer -=1
      self.pointer = max(0,self.pointer)
      self.value = self.recent[self.pointer]
    elif key == 274: #down
      self.pointer += 1
      self.pointer = min(len(self.recent),self.pointer)
      if self.pointer >= len(self.recent):
        self.value = ""
      else:
        self.value = self.recent[self.pointer]
    self.value=self.value[:self.maxLength]
    
  def enter(self):
    self.focused = False
    self.recent += [self.get_value()]
    self.pointer = len(self.recent) - 1
    while len(self.recent) > 100:
      self.recent.__delitem__(0)
    
class FixedTerminal:
  def __init__(self,fields,pygame,font,target,blinkRate=0.6):
    self.fields, self.target, self.pygame, self.font = fields, target, pygame, font
    self.blinkRate = blinkRate
    self.lineHeight = int(self.font.size("|")[1] * 1.2)
    self.pos = (0,target.get_size()[1] - len(self.fields)*self.lineHeight)
    
  def get_values(self):
    return [field.get_value() for field in self.fields]
  def get_texts(self):
    return [field.text for field in self.fields]
    
  def set_values(self,inputValues):
    for i, field in enumerate(self.fields):
      field.value = inputValues[i]
      field.enter()
  def set_texts(self,inputTexts):
    for i, field in enumerate(self.fields):
      field.text = inputTexts[i]

      
  def getInputs(self):
    for field in self.fields:
      field.focused = True
      self.draw(self.target)
      self.edit(field)
    
  def draw(self,target):
    i = 0
    for field in self.fields:
      text = str(field) + ("_" if field.focused and time.clock()%self.blinkRate<self.blinkRate*0.499 else "")
      cpos = (self.pos[0],self.pos[1]+i*self.lineHeight)
      self.pygame.draw.rect(target, [80,85,95,255], self.pygame.Rect(cpos,self.font.size(field.text+("m"*(1+field.maxLength)))))
      target.blit(self.font.render(text,False,[255,255,255,255]),cpos)
      i += 1
    self.pygame.display.flip()
  
  def edit(self,field):
    while True:
      time.sleep(0.05)
      self.draw(self.target)
      for event in self.pygame.event.get():
        if event.type == self.pygame.QUIT:
          print("quitting from text loop.")
          self.pygame.display.quit()
          exit()
        if event.type == self.pygame.KEYDOWN:
          if event.key == self.pygame.K_RETURN:
            field.enter()
            self.draw(self.target)
            return
          field.terpKey(event.key)
          self.draw(self.target)