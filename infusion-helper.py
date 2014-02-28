from collections import namedtuple

import logging
logging.basicConfig(level=logging.DEBUG, filename="infusion-helper.log",format="%(asctime)s - %(levelname)s: %(message)s", datefmt='%I:%M:%S %p', filemode='w')
logging.debug("Log Start")

from WorldChunk import *

#ID Constants
IDPedestal = 1
IDAspectSource = 2
IDSkull = 3
IDCandle = 4
IDCrystal = 5
#/ID Constants

#Re-written function to get surroundings.
#Attempting to use numpy instead of manual iteration
def generateLists(worldChunk):
  if worldChunk is None:
    logging.critical("generateLists called with nil worldChunk")
  if not isinstance(worldChunk, WorldChunk):
    logging.critical("generateLists called with something other than a WorldChunk")
    
  x,y = (numpy.where( worldChunk == IDPedestal) )
  allPedestals = zip(x,y)
  #TODO finish writing this
  return

#pedestals, sources, stuff = getSurroundings()
def getSurroundings(world):
  
  if world is None:
    logging.critical("getSurroundings: world is None?!")
  if not isinstance(world, WorldChunk):
    logging.critical("getSurroundings: world isn't a WorldChunk?!")
  stuff = []
  sources = []
  pedestals = []
  
  for x_offset in xrange(-12,13): #-12, -11, ... , 11, 12
    for z_offset in xrange(-12,13): # ' ' '
      skip  = False
      for y_offset in xrange(-5,11): #-5, -4 .. 9, 10
	if ((x_offset != 0) and (z_offset != 0)):
	  block = world.blockAt(x_offset,-y_offset,z_offset)
	  if (not skip):
	    if (y_offset > 0):
	      if (abs(x_offset) <= 8 and abs(z_offset) <= 8):
		if block.isPedestal():
		  pedestals.append( block.coords() )
		  logging.debug("[!] Pedestal added @ %d,%d,%d", block.x,block.y,block.z)
		  skip = True
	  elif block.isAspectSource():
	    sources.append( block.coords())
	    logging.debug("[!] AspectSource added @ %d,%d,%d", block.x,block.y,block.z)
	  elif block.isParaphernalia():
	    stuff.append( block.coords())
	    logging.debug("[!] Paraphenalia added @ %d,%d,%d", block.x,block.y,block.z)
	  
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
    
if __name__ == "__main__":
  
  print "Testing only, don't expect this to work."
  
  #dummy world for now, all block IDs are zero.
  world = WorldChunk(None)
  
  #Create pedestal that should be detected
  world.setBlock(-5,-4,-5,IDPedestal)
  
  pedestals,sources,stuff = getSurroundings(world)  