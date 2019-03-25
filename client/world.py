from kivy.graphics import Color, Rectangle, Ellipse
from kivy.graphics.context_instructions import Translate, Scale

class Ball:
	def __init__(self, world):
		self.world = world
		self.x = 0.0
		self.y = 0.0
		self.vx = 0.0
		self.vy = 0.0
		self.radius = 1.0
	
	def tick(self, dt):
		self.x += self.vx * dt
		self.y += self.vy * dt

		if self.x < 0.0:
			self.x = 0.0
			self.vx = -self.vx
		elif self.x > self.world.root - self.radius * 2.0:
			self.x = self.world.root - self.radius * 2.0
			self.vx = -self.vx

		if self.y < 0.0:
			self.y = 0.0
			self.vy = -self.vy
		elif self.y > self.world.root - self.radius * 2.0:
			self.y = self.world.root - self.radius * 2.0
			self.vy = -self.vy
	
	def render(self, canvas, dt):
		with canvas:
			Color(0.2, 0.5, 0.7, 1.0)
			Ellipse(pos=(self.x, self.y), size=(self.radius * 2.0, self.radius * 2.0))

class Player:
	def __init__(self, world):
		self.world = world
		self.x = 0.0
		self.y = 0.0
		self.vy = 0.0
		self.width = 0.8
		self.height = 3.0

	def tick(self, dt):
		self.y += self.vy * dt

		if self.y < 0.0:
			self.y = 0.0
			self.vy = 0.0
		elif self.y + self.height > self.world.root:
			self.y = self.world.root - self.height
			self.vy = 0.0
		
	def render(self, canvas, dt):
		with canvas:
			Color(0.5, 0.5, 0.5, 1.0)
			Rectangle(pos=(self.x, self.y), size=(self.width, self.height))

class World:
	def __init__(self):
		self.root = 20.0
		self.ball = Ball(self)
		self.player1 = Player(self)
		self.player2 = Player(self)
		self.player2.x = self.root - self.player2.width
		self.ball.vx = 5.0
		self.ball.vy = 7.0

	def tick(self, dt):
		self.player1.tick(dt)
		self.player2.tick(dt)
		self.ball.tick(dt)

	def render(self, canvas, size, dt):
		ratio = 1.0
		width_is_bigger = True
		if size[0] > size[1]:
			ratio = size[1] / self.root
		else:
			width_is_bigger = False
			ratio = size[0] / self.root
		with canvas:
			if width_is_bigger:
				Translate(size[0] / 2.0 - self.root / 2.0 * ratio, 0.0)
			else:
				Translate(0.0, size[1] / 2.0 - self.root / 2.0 * ratio)
			Scale(ratio, ratio, 1.0)
			Color(0.6, 0.2, 0.2, 1.0)
			Rectangle(pos=(0, 0), size=(self.root, self.root))
		self.player1.render(canvas, dt)
		self.player2.render(canvas, dt)
		self.ball.render(canvas, dt)