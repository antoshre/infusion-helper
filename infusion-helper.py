import math

altar_x = 0	#Global coords
altar_y = 0	# ' ' 
altar_z = 0	# ' '

def test():
  for x in xrange(-2,3):
    for z in xrange(-2,3):
      for y in xrange(-5,11):
	print x,-y,z

def getSurroundings():
  stuff = []
  
  sources = []
  pedestals = []
  
  for x_offset in xrange(-12,13): #-12, -11, ... , 11, 12
    for z_offset in xrange(-12,13): # ' ' '
      skip  = False
      for y_offset in xrange(-5,11): #-5, -4 .. 10, 11
	if ((x_offset != 0) and (z_offset != 0)):
	  x = altar_x + x_offset
	  y = altar_y - y_offset
	  z = altar_z + z_offset
	  block = getBlockAtWorldCoords(x,y,z)
	  if ((not skip) and (y_offset > 0) and (abs(x_offset) <= 8) \
	     and (abs(z_offset) <= 8) and (isinstance(block, TCPedestal))):
	    pedestals.append( WorldCoord(x,y,z) )
	    skip = True
	  elif (isinstance(block, AspectSource)):
	    sources.append( WorldCoord(x,y,z) )
	  else:
	    if (isinstance(block, TCObject)):
		stuff.append( WorldCoord(x,y,z) )
  return pedestals, sources, stuff

def getSymmetry(pedestals, sources, stuff):
  symmetry = 0
  
  for coord in pedestals:
    items = False
    x = altar_x - coord.x
    z = altar_z - coord.z
    
    block = getBlockAtWorldCoords(coord.x,coord.y,coord.z)
    
    if (isinstance(block, TCPedestal)):
      symmetry += 2
      if block.hasItem:
	symmetry += 1
	items = True
    
    x2 = altar_x + x
    z2 = altar_z + z
    
    block = getBlockAtWorldCoords(x2,coord.y,z2)
    
    if (isinstance(block, TCPedestal)):
      symmetry -= 2
      if (block.hasItem and items):
	symmetry -= 1
	
  for coord in stuff:
    x = altar_x - coord.x
    z = altar_z - coord.z
    
    block = getBlockAtWorldCoords(coord.x,coord.y,coord.z)
    
    if (isinstance(block, TCObject)):
      symmetry += 0.1
    x2 = altar_x + x
    z2 = altar_z + z
    
    block = getBlockAtWorldCoords(x2, coord.y, z2)
    
    if (isinstance(block, TCObject)):
      symmetry -= 0.2
  
  return symmetry

  
def getBlockAtWorldCoords(x,y,z):
  return TCCandle()



class TCPedestal:
  hasItem = False
  def __init__(self,hasItem):
    self.hasItem = hasItem
    

class TCObject: #All the stuff that gets picked up that isn't a pedestal
  instability = 0

class TCCandle(TCObject): #Candles
  def __init__(self):
    instability = 1
class TCCrystal(TCObject): #Crystal Clusters
  def __init__(self):
    instability = 1
class TCAiry(TCObject): #Aura Node (blockID 2416)
  def __init__(self):
    instability = 1
class TCHead(TCObject): #field_82512_cj.field_71990_ca in source, pretty sure it's a skull
  def __init__(self):
    instability = 1

class AspectSource:
  eType = ''
  q = 0
  def __init__(self, eType, q):
   self.eType = eType
   self.q = q

class WorldCoord:
  x=0
  y=0
  z=0
  def __init__(self,x,y,z):
    self.x = x
    self.y = y
    self.z = z
    
    
if __name__ == "__main__":
  pedestals,sources,stuff = getSurroundings()
  symmetry = getSymmetry(pedestals, sources, stuff)
  
  print symmetry