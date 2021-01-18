# CryptidMain.py
#
# A wrapper for the Cryptid Game for
# running a simulation
import Cryptid as g
import random
import time

class CryptidA:
  def __init__(self):
    self.a = 1
  def getMove(self, metadata):
    return random.randint(0,3)
  def __str__(self):
    return 'A'

class CryptidB:
  def __init__(self):
    self.a = 1
  def getMove(self, metadata):
    if metadata.getFront() == 3:
      return 1
    return random.randint(0,3)
  def __str__(self):
    return 'B'

class Afanc:
  def __init__(self):
    self.a = 1
  def getMove(self, metadata):
    if metadata.getLeft() == 3:
      return 2
    if metadata.getRight() == 3:
      return 3
    if metadata.getFront() == 3:
      return 1
    if metadata.getBack() == 3:
      return 2
    return 2
  def __str__(self):
    return 'C'

cg = g.Game(width = 40, height = 30)
cg.add(30, CryptidA)
cg.add(30, CryptidB)
cg.add(50, Afanc)
print(cg)
while True:
  cg.update()
  print(cg)
  time.sleep(0.01)
