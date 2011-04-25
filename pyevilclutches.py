"""
Game Maker's Apprentice - Evil Clutches 

Ported into PyGame by Mark Sta Ana 

With lots of help from Linux Format Magazine's gaming development articles.
Audio and Graphical resources are part of the fine book The Game Maker's Apprentice written by Jacob Habgood and Mark Overmars.

Changelog
20081208 - Bullets (current)
	002 -- second attempt at code, this time we use a list to track bullets
	001 -- first attempt at code, using a single bullet. as you can imagine
	this doesn't work very well. in some cases the boss bullet never reach
	the dragon and in turn our dragon is a one hit wonder.
20081201 - Animation
20081124 - Sprites
"""

import os, sys, pygame # using os module to keep file names os neutral

from pygame import *

import random

class Sprite:
	"""
	This class was feature in the PyInvaders and PyRacer tutorials
	in the Linux Format Magazine.

	I've annotated the various improvements as i've seen fit.
	"""
	def __init__(self, xpos, ypos, imgPrefix, frmCount):
		self.x = xpos
		self.y = ypos

		# direction of y (default: going down)
		self.dy = 1
		self.imgPrefix = imgPrefix

		self.loadFrames(frmCount)

		# need a default image to render
		self.bitmap = self.frames[0]
		# set transparency based on bottom left pixel ala Game Maker
		self.colorkey = self.bitmap.get_at((0,self.bitmap.get_height()-1))
		self.bitmap.set_colorkey(self.colorkey)

		# animation, needed by new render function
		self.frame = 0
		self.delay = 6
		self.pause = 0

	def render(self):
		# A nice bit of animation code (cowMooDelay.py) written by Jaime Moreno
		self.pause += 1
		if self.pause >= self.delay:
			self.pause = 0
			self.frame += 1
			if self.frame >= len(self.frames):
				self.frame = 0
			self.bitmap = self.frames[self.frame]

			# own little bit to transparentimatize :D  each frame based on
			# the colour of the bottom left pixel
			self.colorkey = self.bitmap.get_at((0,self.bitmap.get_height()-1))
			self.bitmap.set_colorkey(self.colorkey)

		screen.blit(self.bitmap, (self.x, self.y))

	def loadFrames(self, numFrames):
		# More code from Jaime
		self.frames = []
		if numFrames == 1:
			imgName = os.path.join("data", self.imgPrefix)
			self.frames.append(image.load(imgName))
		else:
			for i in range(1,numFrames):
				imgName = os.path.join("data",self.imgPrefix + "-10%d.gif" % i)
				tmpImage = image.load(imgName)
				self.frames.append(tmpImage.convert())

# initialisation
init()
screen = display.set_mode((640,400))
key.set_repeat(1, 1)
display.set_caption('PyEvilClutches')

backdrop = image.load(os.path.join('data', 'Background.bmp'))
backdrop = backdrop.convert() # another tweak

dragon = Sprite(20, 200, 'Dragon',6)
boss = Sprite(500, 200, 'Boss', 4)
#fireball = Sprite(0,480, 'Fireball.gif', 1) # single frame Sprite test

# boss' bullets
# demon = Sprite(0,480, 'Demon',4)
# baby = Sprite(0,480, 'Baby',2)

quit = 0
clock = pygame.time.Clock()
demonDir = 2 

demons = []
babies = []
fireballs = []

# main loop
while quit == 0:
	clock.tick(30) # set frame rate (60 for normal, 30 for testing)

	screen.blit(backdrop, (0, 0))

	for ourevent in event.get():
		if ourevent.type == QUIT:
			quit = 1

		# controls for our dragon + escape event
		if ourevent.type == KEYDOWN:
			if ourevent.key == K_DOWN and dragon.y < 370:
				dragon.y += 5
			if ourevent.key == K_UP and dragon.y > 10:
				dragon.y -= 5
			if ourevent.key == K_ESCAPE: # quit game if escape is hit
				quit = 1				 # default behaviour for game maker
			if ourevent.key == K_SPACE:
				# NEW: 26/11 HAEDOKEN!
				# noticed that this routine blocks i.e. you fire and
				# you stop moving...
				fireball = Sprite(0,480, 'Fireball.gif', 1) # single frame Sprite test
				fireball.x = dragon.x + 100
				fireball.y = dragon.y + 10
				fireballs.append(fireball)

	# This should really all go into a boss object that extends our existing
	# Sprite class.
	if boss.dy:
		boss.y += 5
	else:
		boss.y -= 5

	if boss.y > 250:
		boss.dy = 0
	if boss.y < 0:
		boss.dy = 1

	if random.randint(1,50) == 50: # test chance 1 in 50 to fire demon
		# create a new demon
		demon = Sprite(boss.x - 10, boss.y - 10, 'Demon',4)
		demon.x = boss.x - 10
		demon.y = boss.y - 10

		# which direction is demon going nw(1), w(2), sw(3)?
		demonDir = random.randint(1,3)
		if demonDir == 1: # nw x-,y-
			demon.dy = 1
		if demonDir == 3: # sw x-,y+
			demon.dy = 0
		# no check for 2, because at the end of the day we're always west

		demons.append(demon)

	if random.randint(1,100) == 100: # test chance 1 in 100 to fire baby dragon
		# create a new baby dragon
		baby = Sprite(boss.x - 10, boss.y - 10, 'Baby',2)
		#baby.x = boss.x - 10
		#baby.y = boss.y - 10

		babies.append(baby)

	for index, demon in enumerate(demons):
		# time to remove demons?
		if demon.x < -100:
			del demons[index]

		demon.x -= 10

		if demon.dy:
			demon.y += 10
		else:
			demon.y -= 10
		# has demon reached the top or bottom of screen?
		if demon.y > 290:
			demon.dy = 0
		if demon.y < -10:
			demon.dy = 1

		demon.render()

		#print "demon %d / %d" % (index,len(demons))

	# NEW 26/11
	for index, fireball in enumerate(fireballs):
		if fireball.x > 640:
			del fireballs[index]

		fireball.x += 10
		fireball.render()

		#print "fireball %d / %d" % (index,len(fireballs))

	# NEW 28/11
	for index, baby in enumerate(babies):
		if baby.x < -100:
			del babies[index]

		baby.x -= 8
		baby.render()

		#print "baby %d / %d" % (index,len(babies))

	# Should think about using Sprite groups...
	dragon.render()
	boss.render()

	display.update()