import pygame
import random
from analyze import parseSourceText
import math

w = 1455
height_width_ratio = 1
win = pygame.display.set_mode((w, 900* height_width_ratio))

red = (255,0,0)
green = (22, 88, 2)
blue = (51,153,255)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
purple = (153,51,255)
orange = (255,165,0)
grey = (192,192,192)
turquoise = (0,153,153)
brown = (122, 87, 4)

letterToColorMap = {
	"a" : (225, 45, 45),
	"b" : (45, 131, 243),
	"c" : (74, 191, 250),
	"d" : (101, 174, 37),
	"e" : (228, 186, 18),
	"f" : (255, 153, 51),
	"g" : (255, 129, 3),
	"h" : (3, 53, 255),
	"i" : (218, 225, 249),
	"j" : (237, 218, 255),
	"k" : (159, 94, 10),
	"l" : (250, 232, 114),
	"m" : (122, 87, 4),
	"n" : (4, 32, 122),
	"o" : (255, 240, 209),
	"p" : (142, 100, 206),
	"q" : (109, 72, 165),
	"r" : (255, 102, 0),
	"s" : (41, 39, 2),
	"t" : (22, 88, 2),
	"u" : (255, 248, 181),
	"v" : (191, 126, 247),
	"w" : (58, 70, 182),
	"x" : (86, 4, 127),
	"y" : (242, 237, 172),
	"z" : (0, 0, 0),
	" " : (255, 255, 254)
}

def selectColor(letter):
	# idx = randrange(26)
	# return list(letterToColorMap.values())[idx] random choice
	return letterToColorMap[letter]

class Square:
	def __init__(self, row, col, width, height, totalRows, letter):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * height
		self.letter = letter
		self.color = selectColor(self.letter)
		self.width = width
		self.height = height
		self.totalRows = totalRows

	def draw(self, win):
		color = self.color
		try:
			pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))
		except:
			print(color)
			print(self.letter)
		# pygame.draw.circle(win, self.color, (self.x, self.y), self.width / 2)
	
	def setColor(self, color = white):
		self.color = color

	def getColor(self):
		return self.color

	def getLetter(self):
		return self.letter

	def restoreColor(self):
		self.color = selectColor(self.letter)

	def invertColor(self):
		if self.color == white:
			self.restoreColor()
		else:
			self.setColor()

	def __lt__(self, other):
		return False

def makeGrid(rows, screen_width, content):
	grid = []
	width = 3
	height = 3
	print(width)
	index = 0
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			if index >= len(content): 
				currentLetter = ' '
			else:
				currentLetter = content[index].lower()
			node = Square(j, i, width, height,rows, currentLetter)
			grid[i].append(node)
			index += 1
	return grid 


def drawGrid(win, rows, width):
	# gap = width//rows
	# for i in range(rows):
	# 	pygame.draw.line(win, white, (0, i*gap), (width,i*gap))
	# 	pygame.draw.line(win, white, (i*gap, 0), (i*gap,width))
	return

def draw(win, grid, rows, width):
	win.fill(white)
	for row in grid:
		for node in row:
			node.draw(win)

	drawGrid(win, rows, width)
	pygame.display.update()

def processText():
	text = ''
	infile = open("processed.txt", "r")
	while True:
		line = infile.readline()
		if not line:
			break
		if not "Chapter" in line:
			text += line.strip() + " "
	infile.close()
	return text

def changeColorByRandom(grid, rows, restore = True):
	indices = []
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			indices.append((i,j))
	random.shuffle(indices)
	count = 0
	updateRects = []
	speed = 250
	for i in indices:
		r = i[0]
		c = i[1]
		if restore:
			grid[r][c].restoreColor()
		else:
			grid[r][c].setColor()
		currentSquare = grid[r][c]
		currentSquare.draw(win)
		updateRects.append(pygame.Rect(currentSquare.x, currentSquare.y, currentSquare.width, currentSquare.height))
		count += 1
		if count == speed:
			pygame.display.update(updateRects)
			updateRects = []
			count = 0
	pygame.display.update()
	return
    	
def sparkle(grid, indices):

	blank = []
	filled = []
	for i in indices:
		r = i[0]
		c = i[1]
		if grid[r][c].getColor() != selectColor(grid[r][c].getLetter()):
			blank.append(grid[r][c])
		else:
			filled.append(grid[r][c])

	random.shuffle(blank)
	random.shuffle(filled)

	while True:
		print("going into big loop")
		speed = 70
		updateRect = []
		count = 0
		for i in range(1, len(blank)):
			if i == len(blank) or i == len(filled):
				filled = filled[len(blank):].extend(filled[:len(blank)])
				break
			blank[i].invertColor()
			blank[i].draw(win)
			filled[i].invertColor()
			filled[i].draw(win)
			blank[i], filled[i] = filled[i], blank[i]
			updateRect.append(pygame.Rect(blank[i].x, blank[i].y, blank[i].width, blank[i].height))
			updateRect.append(pygame.Rect(filled[i].x, filled[i].y, filled[i].width, filled[i].height))
			count += 1
			if count == speed:
				pygame.display.update(updateRect)
				count = 0
	return

def sparkleAlgorithm(grid, rows):
	win.fill(white)
	pygame.display.update()
	indices = []
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			indices.append((i,j))
			grid[i][j].setColor()
	random.shuffle(indices)
	count = 0
	updateRects = []
	speed = 250
	num = 0
	for i in indices:
		r = i[0]
		c = i[1]
		grid[r][c].restoreColor()
		currentSquare = grid[r][c]
		currentSquare.draw(win)
		updateRects.append(pygame.Rect(currentSquare.x, currentSquare.y, currentSquare.width, currentSquare.height))
		count += 1
		num += 1
		if count == speed:
			pygame.display.update(updateRects)
			updateRects = []
			count = 0
		if num == len(indices) // 10 * 9:
			break
	pygame.display.update()
	sparkle(grid, indices)
	return
					
    	

def squareWhiteOutAlgorithm(grid, rows, width):
	mp = {}
	while True:
		speed = 400
		win.fill(white)
		pygame.display.update()
		changeColorByRandom(grid, rows)
		pygame.time.wait(3000)
		changeColorByRandom(grid, rows, False)
		pygame.time.wait(3000)
		win.fill(black)
		pygame.display.update()
		pygame.time.wait(5000)
		pygame.time.wait(3000)
    			
    	
    	
def calculateRows(length):
	perfectRows = math.floor(math.sqrt(length))
	while w % perfectRows != 0:
		perfectRows -= 1
	print(perfectRows)
	return perfectRows

    	
def main(win, width):

	global grid

	run = True

	parseSourceText("genesis.txt")
	content = processText()
	# content = content[:len(content)//20]
	content = content
	print(len(content))
	while len(content) < 144500:
		content += " "
	rows = 485
	print(rows)
	grid = makeGrid(rows, width, content)
	draw(win,grid,rows, width)

	pygame.display.update()
	while run:

		for event in pygame.event.get(): 
			if event.type==pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					print("clicked")
					sparkleAlgorithm(grid, rows)

				if event.key == pygame.K_c:
					squareWhiteOutAlgorithm(grid, rows, width)

main(win, w)
pygame.quit()