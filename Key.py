




import math

NUMSTART = ord("0")
NUMEND = ord("9")
ALSTART = ord("a")
ALEND = ord("z")
AUSTART = ord("A")
AUEND = ord("Z")
PRINTSTART = ord(" ")
PRINTEND = ord("~")

B26 = [chr(item) for item in range(ALSTART,ALEND+1)]
B36 = [chr(item) for item in range(NUMSTART,NUMEND+1)] + B26
B62 = B36 + [chr(item) for item in range(AUSTART,AUEND+1)]
B64 = B62 + ["-","_"]

def toCharRun(num,a,b):
  if type(a) == str:
    a = ord(a)
  if type(b) == str:
    b = ord(b)
  return toCharRange(num,a,a+b)

def toCharRange(num,a,b):
  if type(a) == str:
    a = ord(a)
  if type(b) == str:
    b = ord(b)
  base = b - a
  chars = []
  for i in range(int(math.log(num+1,base+1)+1))[::-1]:
    toAppend = num // (base**i)
    if toAppend == 0 and len(chars) == 0:
      #skipping 0
      continue
    chars.append(chr(toAppend+a))
    num -= toAppend * (base**i)
  if num < 0:
    print("NUM IS " + str(num))
  return "".join(chars)
  
def toCharArr(num,charArr):
  if num < len(charArr):
    return charArr[num]
  base = len(charArr)
  chars = []
  for i in range(int(math.log(num+1,base+1)+2))[::-1]:
    toAppend = int(math.floor(num // (base**i)))
    if toAppend == 0 and len(chars) == 0:
      #skipping 0
      continue
    chars.append(charArr[toAppend])
    num -= toAppend * (base**i)
  if num < 0:
    print("NUM IS " + str(num))
  return "".join(chars)

def fromCharRange(string,a,b):
  if type(a) == str:
    a = ord(a)
  if type(b) == str:
    b = ord(b)
  base = b - a
  result = 0
  for i, char in enumerate(string[::-1]):
    result += (ord(char)-a)*(base**i)

 
def fromCharArr(string,charArr):
  base = len(charArr)
  result = 0
  for i, val in enumerate(charArr.index(char) for char in string[::-1]):
    result += val*(base**i)
  return result
  
def conform(text,alphabet):
  result = ""
  for char in text:
    if alphabet.__contains__(char):
      result += char
    else:
      if char != char.lower():
        if alphabet.__contains__(char.lower()):
          result += char.lower()
      elif char != char.upper():
        if alphabet.__contains__(char.upper()):
          result += char.upper()
  return result