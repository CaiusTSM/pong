from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from world import *

class PongPaddle(Widget):
	score = NumericProperty(0)

	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			bounced = Vector(-1 * vx, vy)
			vel = bounced * 1.1
			ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def __init__(self, world, **kwargs):
		super(PongGame, self).__init__(**kwargs)
		self.world = world
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self.time_passed = 0.0
		self.ticks = 0

	def serve_ball(self, vel=(4, 0)):
		self.ball.center = self.center
		self.ball.velocity = vel
	
	def tick(self, dt):
		self.world.tick(dt)
	
	def render(self, dt):
		self.canvas.clear()
		self.world.render(self.canvas, self.size, dt)

	def update(self, dt):
		self.time_passed += dt

		while self.time_passed >= 1.0 / 60.0:
			self.tick(1.0 / 60)
			self.time_passed -= 1.0 / 60.0

		self.render(dt)

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'w':
			self.world.player1.vy = 10
		elif keycode[1] == 's':
			self.world.player1.vy = -10
		elif keycode[1] == 'up':
			self.world.player2.vy = 10
		elif keycode[1] == 'down':
			self.world.player2.vy = -10
		return True

	def on_touch_move(self, touch):
		if touch.x < self.width / 3:
			self.player1.center_y = touch.y
		if touch.x > self.width - self.width / 3:
			self.player2.center_y = touch.y


class PongApp(App):
	def __init__(self, world, **kwargs):
		super(PongApp, self).__init__(**kwargs)
		self.world = world

	def build(self):
		game = PongGame(self.world)
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0 / 240.0)
		return game


if __name__ == '__main__':
	world = World()
	PongApp(world).run()