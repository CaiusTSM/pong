from kivy.graphics import Color, Rectangle, Ellipse

class Ball:
	def __init__(self):
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
		elif self.x > 19.0:
			self.x = 19.0
			self.vx = -self.vx

		if self.y < 0.0:
			self.y = 0.0
			self.vy = -self.vy
		elif self.y > 19.0:
			self.y = 19.0
			self.vy = -self.vy
	
	def render(self, canvas, ratio, dt):
		with canvas:
			Color(0.2, 0.5, 0.7, 1.0)
			Ellipse(pos=(self.x * ratio, self.y * ratio), size=(self.radius * 2.0 * ratio, self.radius * 2.0 * ratio))

class Player:
	def __init__(self):
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
		elif self.y + 3.0 > 20.0:
			self.y = 17.0
			self.vy = 0.0
		
	def render(self, canvas, ratio, dt):
		with canvas:
			Color(0.5, 0.5, 0.5, 1.0)
			Rectangle(pos=(self.x * ratio, self.y * ratio), size=(self.width * ratio, self.height * ratio))

class World:
	def __init__(self):
		self.root = 20.0
		self.ball = Ball()
		self.player1 = Player()
		self.player2 = Player()
		self.player2.x = 19.2
		self.ball.vx = 5.0
		self.ball.vy = 7.0

	def tick(self, dt):
		self.player1.tick(dt)
		self.player2.tick(dt)
		self.ball.tick(dt)

	def render(self, canvas, size, dt):
		ratio = 1.0
		if size[0] > size[1]:
			ratio = size[1] / self.root
		else:
			ratio = size[0] / self.root
		self.player1.render(canvas, ratio, dt)
		self.player2.render(canvas, ratio, dt)
		self.ball.render(canvas, ratio, dt)