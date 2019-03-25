from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from world import *

class PongGame(Widget):
	def __init__(self, world, **kwargs):
		super(PongGame, self).__init__(**kwargs)
		self.world = world
		self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
		self.keyboard.bind(on_key_down=self.on_keyboard_down)
		self.keyboard.bind(on_key_up=self.on_keyboard_up)
		self.time_passed = 0.0
		self.ticks = 0
	
	def tick(self, dt):
		self.world.tick(dt)
	
	def render(self, dt):
		self.canvas.clear()
		self.world.render(self.canvas, self.size, dt)

	def update(self, dt):
		self.time_passed += dt

		self.ticks = 0
		while self.time_passed >= 1.0 / 60.0:
			self.tick(1.0 / 60)
			self.time_passed -= 1.0 / 60.0
			self.ticks += 1
			if self.ticks >= 6:
				self.time_passed = 0.0

		self.render(dt)

	def keyboard_closed(self):
		self.keyboard.unbind(on_key_down=self.on_keyboard_down)
		self.keyboard = None

	def on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'w':
			self.world.player1.vy = 10
		elif keycode[1] == 's':
			self.world.player1.vy = -10
		elif keycode[1] == 'up':
			self.world.player2.vy = 10
		elif keycode[1] == 'down':
			self.world.player2.vy = -10
		return True

	def on_keyboard_up(self, keyboard, keycode):
		if keycode[1] == 'w':
			self.world.player1.vy = 0.0
		elif keycode[1] == 's':
			self.world.player1.vy = 0.0
		elif keycode[1] == 'up':
			self.world.player2.vy = 0.0
		elif keycode[1] == 'down':
			self.world.player2.vy = 0.0
		return True


class PongApp(App):
	def __init__(self, world, **kwargs):
		super(PongApp, self).__init__(**kwargs)
		self.world = world

	def build(self):
		game = PongGame(self.world)
		Clock.schedule_interval(game.update, 1.0 / 240.0)
		return game


if __name__ == '__main__':
	world = World()
	PongApp(world).run()