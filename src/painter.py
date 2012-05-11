import sys
import math
import numpy as np
from PIL import Image
from multiprocessing import Process, Queue
from Queue import Empty
import pygame
from pygame.locals import *

import query
import metadata

small_size = 200, 200

class Brush():
	def __init__(self, screen, im):
		self.screen = screen
		self.color = (0, 0, 0)
		self.size  = 1
		self.drawing = False
		self.last_pos = None
		self.space = 1
		# if style is True, normal solid brush
		# if style is False, png brush
		self.style = False
		# load brush style png
		self.brush = pygame.image.load("../resource/brush.png").convert_alpha()
		# set the current brush depends on size
		self.brush_now = self.brush.subsurface((0,0), (1, 1))

		self.im = im

	def start_draw(self, pos):
		self.drawing = True
		self.draw_point(pos)
		self.last_pos = pos
	def end_draw(self):
		self.drawing = False

	def set_brush_style(self, style):
		print "* set brush style to", style
		self.style = style
	def get_brush_style(self):
		return self.style

	def get_current_brush(self):
		return self.brush_now

	def set_size(self, size):
		if size < 1: size = 1
		elif size > 32: size = 32
		print "* set brush size to", size
		self.size = size
		self.brush_now = self.brush.subsurface((0,0), (size*2, size*2))
	def get_size(self):
		return self.size

	def set_color(self, color):
		self.color = color
		for i in xrange(self.brush.get_width()):
			for j in xrange(self.brush.get_height()):
				self.brush.set_at((i, j),
						color + (self.brush.get_at((i, j)).a,))
	def get_color(self):
		return self.color

	def draw(self, pos):
		if self.drawing:
			for p in self._get_points(pos):
				self.draw_point(p)

			self.last_pos = pos

	def draw_point(self, p):
		self.im.draw(p)
		# draw eveypoint between them
		if self.style == False:
			pygame.draw.circle(self.screen, self.color, p, self.size)
		else:
			self.screen.blit(self.brush_now, p)

	def _get_points(self, pos):
		""" Get all points between last_point ~ now_point. """
		points = [ (self.last_pos[0], self.last_pos[1]) ]
		len_x = pos[0] - self.last_pos[0]
		len_y = pos[1] - self.last_pos[1]
		length = math.sqrt(len_x ** 2 + len_y ** 2)
		step_x = len_x / length
		step_y = len_y / length
		for i in xrange(int(length)):
			points.append((points[-1][0] + step_x, points[-1][1] + step_y))
		points = map(lambda x:(int(0.5+x[0]), int(0.5+x[1])), points)
		# return light-weight, uniq integer point list
		return list(set(points))

class Menu():
	def __init__(self, screen):
		self.screen = screen
		self.brush  = None
		self.colors = [
				(0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
				(0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
				(0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
				(0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
				(0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
				(0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
				(0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
				(0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
			]
		self.colors_rect = []
		for (i, rgb) in enumerate(self.colors):
			rect = pygame.Rect(10 + i % 2 * 32, 254 + i / 2 * 32, 32, 32)
			self.colors_rect.append(rect)

		self.pens = [
				pygame.image.load("../resource/pen1.png").convert_alpha(),
				pygame.image.load("../resource/pen2.png").convert_alpha()
			]
		self.pens_rect = []
		for (i, img) in enumerate(self.pens):
			rect = pygame.Rect(10, 10 + i * 64, 64, 64)
			self.pens_rect.append(rect)

		self.sizes = [
				pygame.image.load("../resource/big.png").convert_alpha(),
				pygame.image.load("../resource/small.png").convert_alpha()
			]
		self.sizes_rect = []
		for (i, img) in enumerate(self.sizes):
			rect = pygame.Rect(10 + i * 32, 138, 32, 32)
			self.sizes_rect.append(rect)

	def set_brush(self, brush):
		self.brush = brush

	def draw(self):
		pygame.draw.rect(self.screen, self.colors[3], (2, 2, 80 - 2, 600 - 2), 3)
		# draw pen style button
		for (i, img) in enumerate(self.pens):
			self.screen.blit(img, self.pens_rect[i].topleft)
		# draw < > buttons
		for (i, img) in enumerate(self.sizes):
			self.screen.blit(img, self.sizes_rect[i].topleft)
		# draw current pen / color
		self.screen.fill((255, 255, 255), (10, 180, 64, 64))
		pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
		size = self.brush.get_size()
		x = 10 + 32
		y = 180 + 32
		if self.brush.get_brush_style():
			x = x - size
			y = y - size
			self.screen.blit(self.brush.get_current_brush(), (x, y))
		else:
			pygame.draw.circle(self.screen,
					self.brush.get_color(), (x, y), size)
		# draw colors panel
		for (i, rgb) in enumerate(self.colors):
			pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

	def click_button(self, pos):
		# pen buttons
		for (i, rect) in enumerate(self.pens_rect):
			if rect.collidepoint(pos):
				self.brush.set_brush_style(bool(i))
				return True
		# size buttons
		for (i, rect) in enumerate(self.sizes_rect):
			if rect.collidepoint(pos):
				if i:   # i == 1, size down
					self.brush.set_size(self.brush.get_size() - 1)
				else:
					self.brush.set_size(self.brush.get_size() + 1)
				return True
		# color buttons
		for (i, rect) in enumerate(self.colors_rect):
			if rect.collidepoint(pos):
				self.brush.set_color(self.colors[i])
				return True
		return False

class Board():
	def __init__(self, screen):
		self.screen = screen
		self.rects = [(680 + i % 2 * 100, i / 2 * 100) for i in range(12)]
		self.imnames = None
		self.ims = None

	def update(self, imnames):
		self.imnames = imnames[:12]
		self.ims = [pygame.transform.scale(pygame.image.load(imname), (100, 100)) for imname in self.imnames]

	def draw(self):
		pygame.draw.rect(self.screen, (0, 0, 0), (680, 0, 200, 600), 1)
		if self.ims is not None:
			for i, im in enumerate(self.ims):
				self.screen.blit(im, self.rects[i])

class CImage():
	def __init__(self, mData, size = (600, 600)):
		self.mData = mData
		self.size = size
		self.im = np.zeros(self.size, dtype = np.uint8)

	def clear(self):
		self.im = np.zeros(self.size, dtype = np.uint8)

	def draw(self, p):
		self.im[p[1], p[0] - 80] = 1

	def convert(self, imname = 'test.jpg'):
		t_im = Image.fromarray(255 - self.im * 255)
		t_im.thumbnail(small_size, Image.ANTIALIAS)
		t_im.save(imname)
		d = (255 - np.array(t_im)) / 255.0
		return d

def do_query(mData, d, queue):
	queue.put(query.query(mData, d))

class Painter():
	def __init__(self):
		self.mData = metadata.MetaData()
		self.mData.load()
		size = (880, 600)
		self.screen = pygame.display.set_mode(size)
		pygame.display.set_caption("Painter")
		self.clock = pygame.time.Clock()
		self.im = CImage(self.mData)
		self.brush = Brush(self.screen, self.im)
		self.menu  = Menu(self.screen)
		self.menu.set_brush(self.brush)
		self.board = Board(self.screen)
		self.process = None
		self.queue = Queue()

	def run(self):
		self.screen.fill((255, 255, 255))
		while True:
			# max fps limit
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit(0)
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						sys.exit(0)
					# press c to clear screen
					elif event.key == K_c:
						self.screen.fill((255, 255, 255))
						self.im.clear()
					elif event.key == K_s:
						self.update()
				elif event.type == MOUSEBUTTONDOWN:
					# coarse judge here can save much time
					if event.pos[0] < 80:
						self.menu.click_button(event.pos)
					elif event.pos[0] < 680:
						self.brush.start_draw(event.pos)
				elif event.type == MOUSEMOTION:
					if event.pos[0] < 80 or event.pos[0] >= 680:
						self.brush.end_draw()
						self.update()
					else:
						self.brush.draw(event.pos)
				elif event.type == MOUSEBUTTONUP or event.type == ACTIVEEVENT and event.gain == 0:
					self.brush.end_draw()

			self.menu.draw()
			try:
				self.board.update(self.queue.get_nowait())
			except Empty:
				pass
			self.board.draw()
			pygame.display.update()

	def update(self):
		d = self.im.convert()
		#query.query(self.mData, d)
		#thread.start_new_thread(query.query, (self.mData, d))
		if self.process is not None and self.process.is_alive():
			self.process.terminate()
		self.process = Process(target = do_query, args = (self.mData, d, self.queue))
		self.process.start()

if __name__ == '__main__':
	app = Painter()
	app.run()
