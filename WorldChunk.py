#Handle the actual block data.

#ID Constants
IDPedestal = 1
IDAspectSource = 2
IDSkull = 3
IDCandle = 4
IDCrystal = 5
#/ID Constants


import numpy

#TODO: get logging support in here

class WorldChunk:
  blocks = numpy.zeros( ( (12+12+1), (10+5), (12+12+1) ),dtype=int ) #Structure to hold all block IDs

  def __init__(self, fileName):
    #TODO: implement
    
    if fileName is None:
      #Dummy world for testing.
      return
    else:
      print "Not implemented."
    return
  
  def blockAt(self, x,y,z):
    return Block(x,y,z, self.blocks[x,y,z],0)
  def setBlock(self,x,y,z,id):
    self.blocks[x,y,z] = id
  
#TODO: replace with named tuple?
class WorldCoord:
  x=0
  y=0
  z=0
  def __init__(self,x,y,z):
    self.x = x
    self.y = y
    self.z = z
    
class Block:
  id=0
  meta=0
  x=0
  y=0
  z=0
  def __init__(self,x,y,z,id, meta):
    self.id = id
    self.meta = meta
    
    self.x = x
    self.y = y
    self.z = z
  def coords(self):
    return (self.x,self.y,self.z)
  def isPedestal(self):
    return (self.id == IDPedestal)
  def isAspectSource(self):
    return (self.id == IDAspectSource)
  def isParaphernalia(self):
    if (self.id == IDSkull or self.id == IDCandle or self.id == IDCrystal):
      return True
    return False