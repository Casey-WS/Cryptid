# CryptidMain.py
#
# A wrapper for the Cryptid Game for
# running a simulation
import Cryptid as g
import random
import time

# A basic cryptid which purely returns a random
# move
class RandomCryptid:
  def __init__(self):
    self.a = 1
  def getMove(self, metadata):
    return random.randint(0,3)
  def __str__(self):
    return 'A'

# A cryptid which will attack enemies in front,
# but behaves randomly otherwise
class Triffid:
  def __init__(self):
    self.a = 1
  def getMove(self, metadata):
    if metadata.getFront() == 3:
      return 1
    return random.randint(0,3)
  def __str__(self):
    return 'B'

# A cryptid which will turn to attack enemies nearby,
# but moves randomly otherwise
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
    return random.randint(0, 3)
  def __str__(self):
    return 'C'

# Set up a simple game with 30 of each
cg = g.Game(width = 40, height = 30)
cg.add(30, RandomCryptid)
cg.add(30, Triffid)
cg.add(30, Afanc)

# Run the simulation and print the board after each update
print(cg)
while True:
  cg.update()
  print(cg)
  time.sleep(0.01)
