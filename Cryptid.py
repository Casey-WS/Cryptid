"""
Cryptid.py

An instance of a Cryptid game environment
"""

import random

NeighborEmpty = 0
NeighborSame = 1
NeighborWall = 2
NeighborOther = 3

DirectionNorth = 0
DirectionWest = 1
DirectionSouth = 2
DirectionEast = 3

ActionHop = 0
ActionInfect = 1
ActionLeft = 2
ActionRight = 3

class Game:
  def __init__(self, width=400, height=300):
    self.height = height
    self.width = width
    self.simulationCount = 0
    # grid represents the game board. 2D array of objects
    self.grid = [[None for i in range(height)] for j in range(width)]
    # pieces maps a cryptid to its relevant metadata
    self.pieces = dict()
    self.cryptidCount = dict()
    self.debugView = False
    pass

  # Helper class that stores metadata about each cryptid in play
  # Is passed in a cryptid's getAction method
  class CryptidMetadata:
    def __init__(self, x, y, direction, neighbors, infectCount):
      # Critter's column and row in the grid
      self.x = x
      self.y = y
      # Direction this cryptid is facing
      self.direction = direction
      # List of neighbors accessed via helper methods
      self.neighbors = neighbors
      # Number of times this cryptid has infected another
      # Only changed by the Game, and used to give underdogs an advantage
      self.infectCount = infectCount
      #Not implemented yet
      #self.neighborThreats = neighborThreats
    def getFront(self):
      return self.neighbors[0]
    def getBack(self):
      return self.neighbors[2]
    def getLeft(self):
      return self.neighbors[3]
    def getRight(self):
      return self.neighbors[1]
    def getDirection(self):
      return self.direction
    def getInfectCount(self):
      return self.getInfectCount

  # Instantiates <number> objects of type cryptidClass and places them in the board
  # Gives them random locations and directions
  def add(self, number, cryptidClass):
    
    for i in range(number):
      direction = random.randint(0,3)
      c = cryptidClass()
      X = random.randint(0, self.width-1)
      Y = random.randint(0, self.height-1)
      while self.grid[X][Y] is not None:
        X = random.randint(0, self.width-1)
        Y = random.randint(0, self.height-1)
      self.grid[X][Y] = c
      self.pieces[c] = Game.CryptidMetadata(X, Y, direction, None, 0) # Won't have up-to-date neighbors until update()
    
    # Update the count in map
    cryptidName = cryptidClass.__name__
    if cryptidName not in self.cryptidCount:
      self.cryptidCount[cryptidName] = number
    else:
      self.cryptidCount[cryptidName] += number

  def inBounds(self, point):
    return (point[0] >= 0 and point[0] < self.width and point[1] >= 0 and point[1] < self.height)

  def pointAt(self, point, direction):
    if (direction == DirectionNorth):
      return (point[0], point[1]-1)
    elif (direction == DirectionSouth):
      return (point[0], point[1]+1)
    elif (direction == DirectionEast):
      return (point[0]+1, point[1])
    elif (direction == DirectionWest):
      return (point[0]-1, point[1])

  # Roate a direction 90 degrees clockwise
  def rotateDir(self, d):
    if (d == DirectionNorth):
        return DirectionEast
    elif (d == DirectionEast):
        return DirectionSouth
    elif (d == DirectionSouth):
        return DirectionWest
    elif (d == DirectionWest):
        return DirectionNorth

  # Returns what the piece at nPoint is to the piece at point
  def getNeighborRelation(self, point, nPoint):
    if not self.inBounds(nPoint):
      return NeighborWall
    elif self.grid[nPoint[0]][nPoint[1]] is None:
      return NeighborEmpty
    elif self.grid[point[0]][point[1]].__class__ == self.grid[nPoint[0]][nPoint[1]].__class__:
      return NeighborSame
    else:
      return NeighborOther

  # Populate an array with Neighbor values based on where they are in relation to this cryptid
  # retval[0] is in front of the cryptid, then subsequent values are going clockwise
  def getNeighbors(self, metadata):
    currDirection = metadata.direction
    neighborPoint = self.pointAt((metadata.x, metadata.y), currDirection)
    neighbors = []
    for i in range(4):
      neighbors.append(self.getNeighborRelation((metadata.x, metadata.y), neighborPoint))
      currDirection = self.rotateDir(currDirection)
      neighborPoint = self.pointAt((metadata.x, metadata.y), currDirection)
      # Could populate neighborThreats here too if implemented
    return neighbors

  # Every cryptid on the board gets to move once, in random order
  # Each Cryptid will be given some info about their surroundings and asked
  # to make a move
  # Returns a boolean on whether an infection or hop occurred this update (to check for stagnation)
  def update(self):
    self.simulationCount+=1
    stagnated = True

    pieces = list(self.pieces)
    random.shuffle(pieces)
    # TODO: Sort the pieces so those with less infections, with a minimum of 10, go first
    #       Probably should do this with the __lt__ method, or maybe a lambda returning the min of the infection count and 10?

    for i, p in enumerate(pieces):
      if (p not in self.pieces.keys()):
        # Happens in the case where a critter was infected and removed
        continue
      metadata = self.pieces[p]
      point = (metadata.x, metadata.y)
      targetPoint = self.pointAt(point, metadata.direction)
      neighbors = self.getNeighbors(metadata)  # It might be faster to update this each move, instead of recreate each time
      metadata.neighbors = neighbors
      action = p.getMove(metadata)

      if action == ActionLeft:
        metadata.direction = self.rotateDir(self.rotateDir(self.rotateDir(metadata.direction)))
      elif action == ActionRight:
        metadata.direction = self.rotateDir(metadata.direction)
      elif action == ActionInfect:
        if (self.inBounds(targetPoint) and
            self.grid[targetPoint[0]][targetPoint[1]] is not None and
            self.grid[targetPoint[0]][targetPoint[1]].__class__.__name__ is not p.__class__.__name__):
          stagnated = False
          other = self.grid[targetPoint[0]][targetPoint[1]]
          otherMetadata = self.pieces[other]
          del self.pieces[other]
          self.cryptidCount[other.__class__.__name__] -= 1
          self.cryptidCount[p.__class__.__name__] += 1
          self.grid[targetPoint[0]][targetPoint[1]] = p.__class__()
          # NOTE: This is copying the old critters infection count, which seems wrong
          self.pieces[self.grid[targetPoint[0]][targetPoint[1]]] = otherMetadata
          metadata.infectCount+= 1
      elif action == ActionHop:
        if (self.inBounds(targetPoint) and self.grid[targetPoint[0]][targetPoint[1]] is None):
          self.grid[targetPoint[0]][targetPoint[1]] = p
          self.grid[point[0]][point[1]] = None
          metadata.x = targetPoint[0]
          metadata.y = targetPoint[1]

    return stagnated

  def getSimulationCount(self):
    return 0

  # handles displaying critters when debug mode is on
  def getAppearance(self, c):
    if not self.debugView:
        return str(c)
    else:
        # If debug is on then we display arrows correspondiong to direction
        data = self.pieces[c]
        if (data.direction == DirectionNorth):
            return '^'
        elif (data.direction == DirectionSouth):
            return 'v'
        elif (data.direction == DirectionEast):
            return '>'
        else:
            return '<'

  def __str__(self):
    s = "*"
    for i in range(self.width):
      s += "-"
    s += "*\n"
    for i in range(self.height):
      s += "|"
      for j in range(self.width):
        if self.grid[j][i] != None:
          s += self.getAppearance(self.grid[j][i])
        else:
          s += " "
      s += "|\n"
    s += "*"
    for i in range(self.width):
      s += "-"
    s += "*\n"
    for name in self.cryptidCount.keys():
      s += name + ": " + str(self.cryptidCount[name]) + "  "
    return s

  def toggleDebug(self):
    self.debugView = not self.debugView
