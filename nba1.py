from teams import chicago, jersey, wizards, warriors, rockets, cavs, thunder, spurs

import sys
import pygame
import os
import math
import zlib
import cPickle as pickle
from pygame.compat import geterror
from pygame.locals import *
import random

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall

SERVER_PORT = 40053

#hello there
class GameSpace:
	def __init__(self):
        	pygame.init()
		self.size = self.width, self.height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("NBA 2K18")
		# set game objects
		self.clock = pygame.time.Clock()
		self.menu = Menu(self)
		# set variables in gs
		self.counter = 0
		self.pressedKey = 0
		self.connected = False
		self.quit = 0
		self.counted = False
		self.team = None
		self.waitString = "Waiting for player 2 to connect brah"
		self.gameOver = 0

        def setup(self):
		self.score1 = 0
		self.score2 = 0
		self.scoreCount = 0
		self.shot = Shot(self)
		self.player1 = Player1(self)
		self.player2 = Player2(self)
		self.endGame = GameOver(self)

		# background image
		self.bg = pygame.image.load("images/" + self.team['background_image'])
		self.bg = pygame.transform.scale(self.bg, self.team['background_scale'])

	def game_loop(self):
		if self.gameOver == 1:
			self.write(zlib.compress(pickle.dumps([self.player1.rect.center, self.player1.box.rect.center, self.score1, pickle.dumps([]), pickle.dumps([]), self.score2])))
			if self.score1 >= 7:
				self.endGame.display(1)
			else:
                            self.endGame.display(2)
			pygame.display.flip()
		elif self.connected and self.team != None:
			self.counter+=1
                        self.screen.blit(self.bg,(0,0))
			for bullet in self.player2.tears:
				for ball in self.shot.drops:
					if collision(ball.rect.center, bullet.rect.center):
						self.shot.drops.remove(ball)
						self.player2.tears.remove(bullet)
                                                if ball.val == 0:
						    self.score2 += 1
                                                else:
                                                    self.score2 -= 2
						break
			for ball in self.shot.drops:
				if collision(ball.rect.center, [self.player1.rect.center[0], self.player1.rect.center[1]]):
					self.shot.drops.remove(ball)
                                        if ball.val == 0:
                                            self.score1 += 1
                                        else:
                                            self.score1 -= 1
			# frame rate with tick
			self.clock.tick(60)
			# user inputs for slick controls
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				if event.type == KEYDOWN:
					if event.key == 275:
						self.player1.Moving = "R"
					elif event.key == 276:
						self.player1.Moving = "L"
					self.pressedKey += 1
				if event.type == KEYUP:
					self.pressedKey -= 1
					if self.pressedKey == 0:
						self.player1.Moving = "N"
			self.shot.tick()
			self.player1.tick()
			self.player2.tick()
			for tear in self.player2.tears:
				tear.tick()
			if self.counted and self.counter%3 == 0:
				shotx = []
                                value = []
				shoty = []
				#list of shot drop to player 2
				for drop in self.shot.drops:
					shotx.append(drop.rect.center[0])
					shoty.append(drop.rect.center[1])
                                        try:
                                            value.append(drop.val)
                                        except Exception as err:
                                            print err
				self.write(zlib.compress(pickle.dumps([self.player1.rect.center, self.player1.box.rect.center, self.score1, pickle.dumps(shotx), pickle.dumps(shoty), self.score2, pickle.dumps(value)])))
			self.counted = True

			#display game object
			self.screen.blit(self.bg, (0,0))
			self.screen.blit(self.player1.image, self.player1.rect)
			# show tears
			for tear in self.player2.tears:
				self.screen.blit(tear.image, tear.rect)
			self.screen.blit(self.player2.image, self.player2.rect)
			# text display, theres only 1 font?
			lt = pygame.font.Font('freesansbold.ttf', 70)
			TextS = lt.render(str(self.score1), True, (255, 0, 0))
			TextR = TextS.get_rect()
			TextS2 = lt.render(str(self.score2), True, (0, 0, 255))
			TextR2 = TextS2.get_rect()
			if self.score1 > self.score2:
				TextR.center = [TextR.size[1]/2, 50]
				TextR2.center = [TextR2.size[1]/2, 150]
			else:
				TextR.center = [TextR.size[1]/2, 150]
				TextR2.center = [TextR2.size[1]/2, 50]
			self.screen.blit(TextS2, TextR2)
			self.screen.blit(TextS, TextR)
			# player box
			self.screen.blit(self.player1.box.image, self.player1.box.rect)
			# bballs
			for ball in self.shot.drops:
				self.screen.blit(ball.image, ball.rect)
			pygame.display.flip()
			# end of kobe's game
			if self.score1 >= 7 or self.score2 >= 10:
				self.gameOver = 1
                        pygame.display.update()
		else: # waiting to connect to p2
			self.menu.display()
			pygame.display.flip()
	def write(self,data):
		pass
	def quit(self):
		pass

class Menu(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		self.gs = gs
		# choosing teams
		self.chicagoButton = pygame.image.load("images/chiBulls.png")
		self.jerseyButton = pygame.image.load("images/bklNets.png")
                self.warButton = pygame.image.load("images/warriors.png")
                self.wizButton = pygame.image.load("images/wizards.png")
                self.thunderButton = pygame.image.load("images/thunder.png")
                self.cavsButton = pygame.image.load("images/cavs.png")
                self.spursButton = pygame.image.load("images/spurs.png")
                self.rocketsButton = pygame.image.load("images/rockets.png")

		self.chicagoRect = self.chicagoButton.get_rect()
		self.jerseyRect = self.jerseyButton.get_rect()
                self.warRect = self.warButton.get_rect()
                self.wizRect = self.wizButton.get_rect()
                self.thunderRect = self.thunderButton.get_rect()
                self.cavsRect = self.cavsButton.get_rect()
                self.spursRect = self.spursButton.get_rect()
                self.rocketsRect = self.rocketsButton.get_rect()

		self.chicagoRect.center = [150, 300]
		self.jerseyRect.center = [350, 300]
                self.warRect.center = [150,150]
                self.wizRect.center = [350,150]
                self.cavsRect.center = [250,150]
                self.thunderRect.center =[250,300]
                self.spursRect.center = [450,300]
                self.rocketsRect.center = [450,150]
		self.circleCenter = None

	def display(self):
		mx, my = pygame.mouse.get_pos()
		self.gs.screen.fill((0, 0, 0))
		lt = pygame.font.Font('freesansbold.ttf', 50)
		TextS = lt.render("Select your team", True, (255, 255, 255))
		TextR = TextS.get_rect()
		self.gs.screen.blit(TextS, TextR)
		message = pygame.font.Font('freesansbold.ttf', 20)
		messageS = message.render(self.gs.waitString, True, (255, 255, 255))
		messageR = messageS.get_rect()
		messageR.center = 450, 460
		self.gs.screen.blit(messageS, messageR)

		# highlight button
		if dist(mx, my, self.chicagoRect.centerx, self.chicagoRect.centery)<25:
			pygame.draw.circle(self.gs.screen, (0, 255, 0), [self.chicagoRect.centerx, self.chicagoRect.centery], 50, 0)
                elif dist(mx, my, self.wizRect.centerx, self.wizRect.centery)<25:
                        pygame.draw.circle(self.gs.screen, (0,255,0), [self.wizRect.centerx, self.wizRect.centery], 50, 0)
		elif dist(mx, my, self.jerseyRect.centerx, self.jerseyRect.centery)<25:
			pygame.draw.circle(self.gs.screen, (0, 255, 0), [self.jerseyRect.centerx, self.jerseyRect.centery], 50, 0)
                elif dist(mx,my,self.warRect.centerx, self.warRect.centery)<25:
                        pygame.draw.circle(self.gs.screen, (0,255,0), [self.warRect.centerx, self.warRect.centery],50,0)
                elif dist(mx,my,self.cavsRect.centerx, self.cavsRect.centery)<25:
                        pygame.draw.circle(self.gs.screen, (0,255,0), [self.cavsRect.centerx, self.cavsRect.centery],50,0)
                elif dist(mx,my,self.thunderRect.centerx, self.thunderRect.centery)<25:
                        pygame.draw.circle(self.gs.screen, (0,255,0), [self.thunderRect.centerx, self.thunderRect.centery],50,0)
                elif dist(mx,my,self.spursRect.centerx, self.spursRect.centery)<25:
                        pygame.draw.circle(self.gs.screen, (0,255,0), [self.spursRect.centerx, self.spursRect.centery],50,0)
                elif dist(mx,my,self.rocketsRect.centerx, self.rocketsRect.centery)<25:
                        pygame.draw.circle(self.gs.screen, (0,255,0), [self.rocketsRect.centerx, self.rocketsRect.centery],50,0)
                elif self.circleCenter != None:
			pygame.draw.circle(self.gs.screen, self.color, self.circleCenter, 50, 0)
		#display button
		self.gs.screen.blit(self.chicagoButton, self.chicagoRect)
		self.gs.screen.blit(self.jerseyButton, self.jerseyRect)
                self.gs.screen.blit(self.warButton, self.warRect)
                self.gs.screen.blit(self.wizButton, self.wizRect)
                self.gs.screen.blit(self.cavsButton, self.cavsRect)
                self.gs.screen.blit(self.spursButton, self.spursRect)
                self.gs.screen.blit(self.rocketsButton, self.rocketsRect)
                self.gs.screen.blit(self.thunderButton, self.thunderRect)
		# user click check
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gs.quit()
			elif event.type == pygame.MOUSEBUTTONUP:
				if dist(mx, my, self.chicagoRect.centerx, self.chicagoRect.centery) < 25:
					self.circleCenter = [self.chicagoRect.centerx, self.chicagoRect.centery]
					self.color = (255,0,0 )
					self.gs.team = chicago
					self.gs.setup()
					if self.gs.connected:
						self.gs.write('chicago')
				elif dist(mx, my, self.jerseyRect.centerx, self.jerseyRect.centery) < 25:
					self.circleCenter = [self.jerseyRect.centerx, self.jerseyRect.centery]
					self.color = (255, 255, 255)
					self.gs.team = jersey
					self.gs.setup()
					if self.gs.connected:
						self.gs.write('jersey')

				elif dist(mx, my, self.wizRect.centerx, self.wizRect.centery) < 25:
					self.circleCenter = [self.wizRect.centerx, self.wizRect.centery]
					self.color = (255, 0, 0)
                                        try:
                                            self.gs.team = wizards
                                        except Exception as err:
                                            print err
                                        self.gs.setup()
					if self.gs.connected:
						self.gs.write('wizards')

                                elif dist(mx, my, self.warRect.centerx, self.warRect.centery) < 25:
                                        self.circleCenter = [self.warRect.centerx, self.warRect.centery]
                                        self.color = (255, 255, 0)
                                        self.gs.team = warriors
                                        self.gs.setup()
                                        if self.gs.connected:
                                                self.gs.write('warriors')

                                elif dist(mx, my, self.cavsRect.centerx, self.cavsRect.centery) < 25:
                                        self.circleCenter = [self.cavsRect.centerx, self.cavsRect.centery]
                                        self.color = (255, 0, 0)
                                        self.gs.team = cavs
                                        self.gs.setup()
                                        if self.gs.connected:
                                                self.gs.write('cavs')

                                elif dist(mx, my, self.spursRect.centerx, self.spursRect.centery) < 25:
                                        self.circleCenter = [self.spursRect.centerx, self.spursRect.centery]
                                        self.color = (255, 255, 255)
                                        self.gs.team = spurs
                                        self.gs.setup()
                                        if self.gs.connected:
                                                self.gs.write('spurs')

                                elif dist(mx, my, self.thunderRect.centerx, self.thunderRect.centery) < 25:
                                        self.circleCenter = [self.thunderRect.centerx, self.thunderRect.centery]
                                        self.color = (0,0,255)
                                        self.gs.team = thunder
                                        self.gs.setup()
                                        if self.gs.connected:
                                                self.gs.write('thunder')

                                elif dist(mx, my, self.rocketsRect.centerx, self.rocketsRect.centery) < 25:
                                        self.circleCenter = [self.rocketsRect.centerx, self.rocketsRect.centery]
                                        self.color = (255, 0, 0)
                                        self.gs.team = rockets
                                        self.gs.setup()
                                        if self.gs.connected:
                                                self.gs.write('rockets')

# ball drops
class Shot(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		self.gs = gs
		self.drops = []
		self.created = False
                self.val = 0
	def tick(self):
		create = random.randint(1, 80)
		if create == 5:
			self.created = Dropshots(self.gs)
			self.drops.append(self.created)
                elif create == 10:
                     #   print("create a bomb")
                        self.val = 1
                        try:
                            self.created = DropBombs(self.gs)
                        except Exception as err:
                            print err
                        self.drops.append(self.created)
		for ball in self.drops:
			ball.rect = ball.rect.move([0, 1])

class Dropshots(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/bball.png")
		self.rect = self.image.get_rect()
		self.x = random.randint(40, 600)
		self.rect.center = [self.x, -20]
                self.val = 0
class DropBombs(pygame.sprite.Sprite):
        def __init__(self, gs = None):
                pygame.sprite.Sprite.__init__(self)
                self.gs = gs
                self.image = pygame.image.load("images/bomb.png")
                self.rect = self.image.get_rect()
                self.x = random.randint(40,600)
                self.rect.center = [self.x,-20]
                self.val = 1
# Player 1
class Player1(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/" + self.gs.team['player_image'])
		self.rect = self.image.get_rect()
		self.rect.center = self.gs.team['player_start']
		self.Moving = "N"
		self.box = Box(self.rect.center, self.gs)
	def tick(self):
		# move player
		if self.Moving == "R":
			self.rect = self.rect.move([5, 0])
			self.box.rect = self.box.rect.move([5, 0])
		elif self.Moving == "L":
			self.rect = self.rect.move([-5, 0])
			self.box.rect = self.box.rect.move([-5, 0])
		if self.rect.center[0] < self.gs.team['max_player_left']:
			self.rect.center = [self.gs.team['max_player_left'], self.rect.center[1]]
			self.box.rect.center = [self.rect.center[0], self.rect.center[1]]
		elif self.rect.center[0] > self.gs.team['max_player_right']:
			self.rect.center = [self.gs.team['max_player_right'], self.rect.center[1]]
			self.box.rect.center = [self.rect.center[0], self.rect.center[1]]
# the swatter
class Player2(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)
		self.mx = 1
		self.my = 1
		self.gs = gs
		self.image = pygame.image.load("images/" + self.gs.team["hand_image"])
		self.rect = self.image.get_rect()
		self.rect.center = self.gs.team['hand_location']
		self.tears = []
		self.angle = 0
		self.orig_image = self.image
	def tick(self):
		for ball in self.tears:
			if ball.rect.center[0] < -20 or ball.rect.center[0] > 660:
				self.tears.remove(ball)
			elif ball.rect.center[1] < -20 or ball.rect.center[1] > 500:
				self.tears.remove(ball)
		# player 2 rotates
		self.angle = math.atan2(self.my-self.rect.center[1], self.mx - self.rect.center[0])*-180/math.pi + 200
		self.image = pygame.transform.rotate(self.orig_image, self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)

# catching balls lol
class Box(pygame.sprite.Sprite):
	def __init__(self, center, gs = None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("images/" + self.gs.team['box_image'])
		self.rect = self.image.get_rect()
		self.x = center[0]
		self.y = center[1]
		self.rect.center = [self.x, self.y]

class Tear(pygame.sprite.Sprite):
	def __init__(self, x, y, xm, ym, gs = None):
		pygame.sprite.Sprite.__init__(self)
		self.xm = xm
		self.ym = ym
		self.gs = gs
		self.image = pygame.image.load("images/" + self.gs.team['bullet_image'])
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
	def tick(self):
		self.rect = self.rect.move([self.xm, self.ym])

# game over boyyy
class GameOver(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		self.gs = gs
	def display(self, winner):
		self.gs.screen.fill((0,0,0))
		# player 1 winna
		if winner == 1:
			lt = pygame.font.Font('freesansbold.ttf', 30)
                        TextS = lt.render("YOU ARE THE NBA CHAMPION", True, (255, 255, 255))
		elif winner == 2:
			lt = pygame.font.Font('freesansbold.ttf', 30)
			TextS = lt.render("You blew a 3-1 lead", True, (255, 255, 255))
		TextR = TextS.get_rect()
		TextR.center = [320, 300]
		self.gs.screen.blit(TextS, TextR)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gs.quit()

# distance
def dist(x1, y1, x2, y2):
	return ((y2-y1)**2 + (x2-x1)**2)**.5

def collision(ball_center, catcher_point):
	distance = dist(ball_center[0], ball_center[1], catcher_point[0], catcher_point[1])
	if distance <= 30:
		return True
	else:
		return False

class ServerConnection(Protocol):
	def __init__(self, addr, client):
		self.addr = addr
		self.client = client
	def dataReceived(self, data):
		if data == 'player 2 connected':
                        print("player 2 connected")
			self.client.connected = True
			self.client.waitString = "player 2 connected"
			if self.client.team != None:
				self.transport.write(self.client.team['name'])
		else:
			self.client.player2.tears = []
			data = pickle.loads(zlib.decompress(data))
			# player 2's rotatos
			self.client.player2.mx = data[0]
			self.client.player2.my = data[1]
			data[2] = pickle.loads(data[2])
			data[3] = pickle.loads(data[3])
			data[4] = pickle.loads(data[4])
			data[5] = pickle.loads(data[5])
			#sync tear
			i = 0
			for x in data[2]:
				self.client.player2.tears.append(Tear(data[2][i], data[3][i], data[4][i], data[5][i], self.client))
				i += 1
	def connectionLost(self, reason):
		reactor.stop()
	def write(self, data):
		self.transport.write(data)
	def quit(self):
		self.transport.loseConnection()

class ServerConnectionFactory(Factory):
	def __init__(self, client):
		self.client = client
	def buildProtocol(self, addr):
		proto = ServerConnection(addr, self.client)
		self.client.write = proto.write
		self.client.quit = proto.quit
		return proto

if __name__ == '__main__':
	gs = GameSpace()
	lc = LoopingCall(gs.game_loop)
	lc.start(1/60)
	reactor.listenTCP(SERVER_PORT, ServerConnectionFactory(gs))
	reactor.run()
	lc.stop()
