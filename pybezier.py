import pygame, time, sys, math
import random

xres = 1000
yres = 800

LEFT = 1
pygame.init()
pygame.font.init()
win = pygame.display.set_mode((xres, yres), pygame.SRCALPHA)

SHIFT = False
CTRL = False
ALT = False
SPACE = False
red = False
green = False
blue = False
textView = False
layerView = False

class slider(object):
	def __init__(self, name, value, size, pos):
		self.size = size
		self.name = name
		self.value = value
		self.xpos = pos[0]
		self.ypos = pos[1]

	def draw (self):
		pass	

	def update (self, pos):
		pass

class point2d(object):
	xpos = 0
	ypos = 0
	clicked = False
	def __init__(self, xpos, ypos):
		self.xpos = xpos
		self.ypos = ypos

	def draw(self, color):
		pygame.draw.circle(win, color, (self.xpos, self.ypos), 4)

	def update(self, xpos, ypos):
		self.xpos = xpos
		self.ypos = ypos

	def checkClicked(self, xpos, ypos):
		if (abs(ypos - self.ypos) < 10):
			if (abs(xpos - self.xpos) < 10):
				self.clicked = True

	def dump(self):
		print self.xpos, self.ypos

class line(object):
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def interpolate(self, percent):
		dx = 1.*(self.p2.xpos - self.p1.xpos)*percent
		dy = 1.*(self.p2.ypos - self.p1.ypos)*percent
		return point2d(dx+self.p1.xpos, dy+self.p1.ypos)

	def draw(self, color):
		pygame.draw.line(win, color, (self.p1.xpos, self.p1.ypos), (self.p2.xpos, self.p2.ypos), 4)

	def dump(self):
		print self.p1.xpos, self.p1.ypos, self.p2.xpos, self.p2.ypos

class graphicObject(object):
	def __init__(self):
		self.isVisible = True
		self.filled = True
		self.handles = []
		self.TYPE = ""
		selfblines = []
		self.red = random.randint(60, 190)
		self.green = random.randint(60, 190)
		self.blue = random.randint(60, 19)
		self.dark = (self.red-20, self.green-20, self.blue-20)		
		self.light = (self.red + (255-self.red)*0.8, self.green + (255-self.green)*0.8, self.blue + (255-self.blue)*0.8)
		self.color = (self.red, self.green, self.blue)
		
	def draw(self, selected, nothingselected):
		pass

	def update(self):
		pass
				
class regularpoly(graphicObject):
	def __init__(self):
		self.xsize = 0
		self.ysize = 0
		self.xpos = 0
		self.ypos = 0

	def draw(self, selected, nothingselected):
		pass
	
	def update(self):
		self.handles[0] = xpos
		self.handles[1] = xpos + xsize
#		self.handles[2] = 
#		self.handles[3] = 

class poly(object):
	def __init__(self):
		self.isVisible = True
		self.filled = True
		self.handles = []
		self.TYPE = "POLYGON"
		self.lines = []
		self.red = random.randint(60, 190)
		self.green = random.randint(60, 190)
		self.blue = random.randint(60, 190)
		self.dark = (self.red-20, self.green-20, self.blue-20)
		self.light = (self.red + (255-self.red)*0.8, self.green + (255-self.green)*0.8, self.blue + (255-self.blue)*0.8)
		self.color = (self.red, self.green, self.blue)
		self.pointList = []

	def draw(self, selected, nothingselected):
		if (len(self.pointList)>2):
			pygame.draw.polygon(win, self.color, self.pointList)
		
		if selected:
			self.color = (self.red, self.green, self.blue)
			for p in self.handles:
					p.draw(self.dark)
			for i in range(len(self.handles)):
					line(self.handles[i], self.handles[i-1]).draw(self.dark)
		elif nothingselected:
			self.color = (self.red, self.green, self.blue)
		else:
			self.color = self.light 


	def update(self):
		self.lines = []
		self.pointList = []
		for i in range(1, len(self.handles)):
				self.lines.append(line(self.handles[i-1], self.handles[i]))
		for h in self.handles:
				self.pointList.append((h.xpos, h.ypos))
	def colorUpdate(self):
		self.color = (self.red, self.green, self.blue)
		self.dark = (self.red-20, self.green-20, self.blue-20)
		self.light = (self.red + (255-self.red)*0.8, self.green + (255-self.green)*0.8, self.blue + (255-self.blue)*0.8)
	
'''bezier curve object'''
	
def triangle(n):
	return 1.*n*(n+1)/2

class bezier(object):
	def __init__(self):
		self.isVisible = True
		self.filled = False
		self.TYPE = "BCURVE"
		self.handles = []
		self.points = []
		self.handleLines = []
		self.lines = []
		self.red = random.randint(60, 190)
		self.green = random.randint(60, 190)
		self.blue = random.randint(60, 190)
		self.color = (self.red, self.green, self.blue)
		self.dark = (self.red-20, self.green-20, self.blue-20)
		self.light = (self.red + (255-self.red)*0.8, self.green + (255-self.green)*0.8, self.blue + (255-self.blue)*0.8)
	def draw(self, selected, nothingselected):
		if selected:
			self.color = self.red, self.green, self.blue
			for h in self.handles:
				h.draw(self.dark)
			for i in range(1, len(self.handles)):
				line(self.handles[i], self.handles[i-1]).draw(self.dark)
		elif nothingselected:
			self.color = (self.red, self.green, self.blue)	
		else:
			self.color = self.light
		for l in self.lines:
			l.draw(self.color)
		if (self.filled):
			pointlist = []
			for h in self.points:
					pointlist.append((h.xpos, h.ypos))
			if selected or nothingselected:
					pygame.draw.polygon(win, self.color, pointlist)
			else:
					pygame.draw.polygon(win, self.light, pointlist)
			
	def update(self):
		self.lines = []
		self.points = []
		self.handleLines = []
		for i in range(0, len(self.handles)-1):
			self.handleLines.append(line(self.handles[i], self.handles[i+1]))
		if (len(self.handles) > 1):
			for i in range(100):
				npoints = len(self.handles)
				nrows = npoints - 1
				percent = i/100.
				layer = 1
				layerindex = 0
				layersize = nrows-2
				while(layer <= nrows-1):
					i1 = len(self.handleLines)-nrows+layer-1
					i2 = i1+1
					self.handleLines.append(line(self.handleLines[i1].interpolate(percent), self.handleLines[i2].interpolate(percent)))
					if (layerindex == layersize):
							layersize -= 1
							layer +=1
							layerindex = 0
					else:
							layerindex += 1
				self.points.append(self.handleLines[len(self.handleLines)-1].interpolate(percent))
				del self.handleLines[:]	
				for h in range(0, len(self.handles)-1):
					self.handleLines.append(line(self.handles[h], self.handles[h+1]))

				for p in range(1, len(self.points)):
					self.lines.append(line(self.points[p-1], self.points[p]))
		if abs(self.handles[len(self.handles)-1].xpos - self.handles[0].xpos) < 10 and abs(self.handles[len(self.handles)-1].ypos - self.handles[0].ypos) < 10 and len(self.handles) > 2:
			self.filled = True
		if (self.filled):
			pointlist = []
			for h in self.points:
					pointlist.append((h.xpos, h.ypos))
					
	def colorUpdate(self):
		self.color = (self.red, self.green, self.blue)
		self.dark = (self.red-20, self.green-20, self.blue-20)
		self.light = (self.red + 40, self.green + 40, self.blue + 40)
		
class freeHand(object):
	def __init__(self):
		self.TYPE = "FREE"
		self.lines = []
		self.filled = False
		self.handles = []
		self.red = random.randint(60, 190)
		self.green = random.randint(60, 190)
		self.blue = random.randint(60, 190)
		self.color = (self.red, self.green, self.blue)
		self.light = (self.red + (255-self.red)*0.8, self.green + (255-self.green)*0.8, self.blue + (255-self.blue)*0.8)
		self.dark = (self.red-20, self.green-20, self.blue-20)
		self.clicked = False
		self.isVisible = True
				
	def draw(self, selected, nothingselected):
		if len(self.lines) > 1:
			for l in self.lines:
				if selected or nothingselected:
					l.draw(self.color)
				else:
					l.draw(self.light)
		if self.filled:
		  	pointlist = []
			for h in self.handles:
				pointlist.append((h.xpos, h.ypos))
			if selected or nothingselected:
				pygame.draw.polygon(win, self.color, pointlist)
			else:
				pygame.draw.polygon(win, self.light, pointlist)
		
	def grow(self, pos):
		if not self.filled:
			self.handles.append(point2d(pos[0], pos[1]))
		if (abs(pos[0] - self.handles[0].xpos) < 10 and abs(pos[1] -  self.handles[0].ypos) < 10 and len(self.handles) > 15):
			self.handles.append(self.handles[0])
			self.filled = True
		
	def update(self):
		self.lines = []
		if len(self.handles) > 0:
			for i in range(1, len(self.handles)):
				self.lines.append(line(self.handles[i], self.handles[i-1]))
					
	def colorUpdate(self):
		self.color = (self.red, self.green, self.blue)
		self.dark = (self.red-20, self.green-20, self.blue-20)
		self.light = (self.red + 40, self.green + 40, self.blue + 40)


class text(object):
	def __init__(self, pos):
		self.xpos = pos[0]
		self.TYPE = "text"
		self.ypos = pos[1]
		self.handles = []
		self.isVisible = True
		self.red = 0
		self.green = 0
		self.blue = 0
		self.color = (self.red, self.green, self.blue)
		self.light = (self.red + (255-self.red)*0.8, self.green + (255-self.green)*0.8, self.blue + (255-self.blue)*0.8)
		self.dark = (self.red-20, self.green-20, self.blue-20)
		self.myText = ["nothing"]

	def draw(self, selected, nothingselected):
		global win
		for t in range(len(self.myText)):
			textrender = myfont.render(self.myText[t], True, (0, 0, 0), (255, 255, 255))
			textrect = textrender.get_rect()
			textrect.left = self.xpos
			textrect.top = self.ypos + t*myfont.get_height()+1
			win.blit(textrender, textrect)

	def update(self):
		pass

class Layer(object):
	def __init__(self):
		self.objects = [0]

	def draw(self, selected, nothingselected):
		for b in range(1, len(self.objects)):
			if self.objects[b].isVisible or self.objects[0] == b:
				self.objects[b].draw(self.objects[0]==b, self.objects[0] == 0)
		
	def update(self, e):
		global SHIFT, CTRL, ALT, SPACE, red, green, blue, mousePos, win, textView, layerView
		
		if e.type == pygame.MOUSEBUTTONDOWN and e.button == LEFT:
			for b in range(1, len(self.objects)):
				for p in self.objects[b].handles:
					p.checkClicked(e.pos[0], e.pos[1])
					if p.clicked:
						break
		if e.type == pygame.MOUSEMOTION:
			mousePos = e.pos
			if self.objects[0] > 0:
				for i in range(len(self.objects[self.objects[0]].handles)):
					if self.objects[self.objects[0]].handles[i].clicked:
						self.objects[self.objects[0]].handles[i].update(e.pos[0], e.pos[1])
						self.objects[self.objects[0]].update()
						if (self.objects[self.objects[0]].TYPE == "BCURVE" and self.objects[self.objects[0]].filled and i == 0):
							self.objects[self.objects[0]].handles[len(self.objects[self.objects[0]].handles)-1].update(e.pos[0], e.pos[1])
			if SPACE and self.objects[0] > 0 and self.objects[self.objects[0]].TYPE == "FREE":
			  		self.objects[self.objects[0]].grow(e.pos)
			  		self.objects[self.objects[0]].update()
		if e.type == pygame.MOUSEBUTTONUP and e.button == LEFT:
			for b in range(1, len(self.objects)):
				for p in self.objects[b].handles:
					p.clicked = False
		if e.type == pygame.KEYUP:
			if e.key == pygame.K_LSHIFT:
		  		SHIFT = False
			if e.key == pygame.K_LCTRL:
		  		CTRL = False
			if e.key == pygame.K_LALT:
		  		ALT = False
			if e.key == pygame.K_SPACE:
		  		SPACE = False
		if e.type == pygame.KEYDOWN:
			if textView:
				keyname = pygame.key.name(e.key)
				if keyname == 'return':
						self.objects[self.objects[0]].myText.append("")	
				elif keyname == 'space':
						self.objects[self.objects[0]].myText[len(self.objects[self.objects[0]].myText)-1] += " "
				elif keyname == 'backspace':
						if len(self.objects[self.objects[0]].myText) > 0:
								pass
				elif keyname == 'escape':
						self.objects[0] = 0
						textView = False
				else:
						self.objects[self.objects[0]].myText[len(self.objects[self.objects[0]].myText)-1] += keyname
			else:
				if e.key == pygame.K_t:
					self.objects.append(text(mousePos))
					self.objects[0] = len(self.objects)-1
					textView = True
				if e.key == pygame.K_r:
					if self.objects[0] > 0:
							red = True
				if e.key == pygame.K_LSHIFT:
					SHIFT = True
				if e.key == pygame.K_LCTRL:
					CTRL = True
				if e.key == pygame.K_LALT:
					ALT = True
				if e.key == pygame.K_SPACE:
					SPACE = True
					if self.objects[0] > 0 and self.objects[self.objects[0]].TYPE == "FREE" and len(self.objects[self.objects[0]].handles) > 0:
						self.objects.append(freeHand())
						self.objects[0] += 1
					if self.objects[0] > 0:
						if not (self.objects[self.objects[0]].filled and self.objects[self.objects[0]].TYPE == "BCURVE"):
							pos = pygame.mouse.get_pos()
							self.objects[self.objects[0]].handles.append(point2d(pos[0], pos[1]))
							self.objects[self.objects[0]].update()
				elif e.key == pygame.K_c:
					self.objects.append(bezier())
					self.objects[0] = len(self.objects)-1
				elif e.key == pygame.K_p:
					self.objects.append(poly())
					self.objects[0] = len(self.objects)-1
				elif e.key == pygame.K_UP:
					if self.objects[0] > 1:
						if SHIFT:
							self.objects[self.objects[0]], self.objects[self.objects[0]-1] = self.objects[self.objects[0]-1], self.objects[self.objects[0]]
					if self.objects[0] > 0:
						self.objects[0] -= 1
				elif e.key == pygame.K_DOWN:
					if self.objects[0] < len(self.objects)-1 and len(self.objects) > 1 and self.objects[0] > 0:
						if SHIFT:
							self.objects[self.objects[0]+1], self.objects[self.objects[0]] = self.objects[self.objects[0]], self.objects[self.objects[0]+1]
					if self.objects[0] < len(self.objects)-1:
						self.objects[0] +=1
				elif e.key == pygame.K_ESCAPE:
					self.objects[0] = 0
				elif e.key == pygame.K_v:
					if len(self.objects) > 0:
						if SHIFT:
							isIt = self.objects[1].isVisible
							for i in range(1, len(self.objects)):
								self.objects[i].isVisible = not isIt
						else:
							if self.objects[0] != 0:
								self.objects[self.objects[0]].isVisible = not self.objects[self.objects[0]].isVisible
				elif e.key == pygame.K_f:
					self.objects.append(freeHand())
					self.objects[0] += 1
					self.objects[0] = len(self.objects)-1
			if self.objects[0] == 0:
				 layerView = True


objects = [0]
layers = [1, Layer()]
# just use a 2d array
# figure out how to move stuff up layers

black = (0, 0, 0)
black80 = (0x42, 0x42, 0x42)
black60 = (0x75, 0x75, 0x75)
black40 = (0xbd, 0x42, 0x42)
black20 = (0xee, 0xee, 0xee)
white = (0xff, 0xff, 0xff)
def GUI():
	pygame.draw.rect(win, black, pygame.Rect(0, 0, 40, yres))
	pygame.draw.rect(win, black80, pygame.Rect(5, 5, 30, 80))
	if layers[0] > 0:
		if (layers[layers[0]].objects[0] > 0):
			pygame.draw.circle(win, layers[layers[0]].objects[layers[layers[0]].objects[0]].color, (20,20), 10)

'''main declaration lol'''


#font= Font("~/Downloads/")

mousePos = [0, 0]

def event(e):
	layers[layers[0]].update(e)
	if layerView:
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_l:
				layers.append(Layer())
				layers[0] += 1
			elif e.key == pygame.K_DOWN:
				if layers[0] > 1:
					layers[0] -= 1
			elif e.key == pygame.K_UP:
				if layers[0] < len(layers):
					layers[0] += 1
					
	if e.type == pygame.QUIT:
			sys.exit(0)

def draw():
	for i in range(1, len(layers)):
		layers[i].draw(True, True)

	GUI()
	pygame.display.update()
	pygame.display.flip()

pygame.init()
pygame.font.init()
myfont = pygame.font.Font("RobotoTTF/Roboto-Light.ttf", 42)

while True:
	win.fill((255, 255, 255))

	for e in pygame.event.get():
		event(e)
	draw()
