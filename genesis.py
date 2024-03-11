import pygame
import random
from analyze import parseSourceText
import math
from colors import letterToColorMap
w = 1000
h = 618
win = pygame.display.set_mode((w, h))

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
	
	def setColor(self, color = black):
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

def makeGrid(rows, cols, screen_width, content):
	grid = []
	width = 2
	height = 2
	print(width)
	index = 0
	for i in range(cols):
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
    	
# def sparkle(grid, indices):

# 	blank = []
# 	filled = []
# 	for i in indices:
# 		r = i[0]
# 		c = i[1]
# 		if grid[r][c].getColor() != selectColor(grid[r][c].getLetter()):
# 			blank.append(grid[r][c])
# 		else:
# 			filled.append(grid[r][c])

# 	random.shuffle(blank)
# 	random.shuffle(filled)

# 	while len(blank):
# 		print(len(blank))
# 		speed = 100
# 		diff = 8000
# 		updateRect = []
# 		count = 0
# 		for i in range(1, len(blank)):
# 			if i == len(blank) or i == len(filled):
# 				filled = filled[len(blank):].extend(filled[:len(blank)])
# 				break
# 			blank[i].invertColor()
# 			blank[i].draw(win)
# 			filled[i].invertColor()
# 			filled[i].draw(win)
# 			blank[i], filled[i] = filled[i], blank[i]
# 			updateRect.append(pygame.Rect(blank[i].x, blank[i].y, blank[i].width, blank[i].height))
# 			updateRect.append(pygame.Rect(filled[i].x, filled[i].y, filled[i].width, filled[i].height))
# 			count += 1
# 			if count == speed:
# 				pygame.display.update(updateRect)
# 				count = 0
# 		cutIdx = min(diff, len(blank))
# 		newFill = blank[:cutIdx]
# 		blank = blank[cutIdx:]
# 		updateRect = []
# 		for i in newFill:
# 			i.invertColor()
# 			i.draw(win)
# 			updateRect.append(pygame.Rect(i.x, i.y, i.width, i.height))
# 		pygame.display.update(updateRect)
# 		if not len(blank):
# 				break
# 	return

# def sparkleAlgorithm(grid, rows):
# 	while True:
# 		win.fill(white)
# 		pygame.display.update()
# 		indices = []
# 		for i in range(len(grid)):
# 			for j in range(len(grid[i])):
# 				indices.append((i,j))
# 				grid[i][j].setColor()
# 		random.shuffle(indices)
# 		count = 0
# 		updateRects = []
# 		speed = 400
# 		num = 0
# 		for i in indices:
# 			r = i[0]
# 			c = i[1]
# 			grid[r][c].restoreColor()
# 			currentSquare = grid[r][c]
# 			currentSquare.draw(win)
# 			updateRects.append(pygame.Rect(currentSquare.x, currentSquare.y, currentSquare.width, currentSquare.height))
# 			count += 1
# 			num += 1
# 			if count == speed:
# 				pygame.display.update(updateRects)
# 				updateRects = []
# 				count = 0
# 		pygame.display.update()
# 		pygame.time.wait(3000)
# 		changeColorByRandom(grid, rows, False)
# 		pygame.time.wait(3000)
# 		win.fill(black)
# 		pygame.display.update()
# 		pygame.time.wait(5000)
# 		pygame.time.wait(3000)
# 	return
					
    	
def changeColorByRandom(grid, rows, restore = True):
	indices = []
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			indices.append((i,j))
	# indices.sort(key = lambda x: grid[x[0]][x[1]].getLetter())
	random.shuffle(indices)
	count = 0
	updateRects = []
	speed = 50
	currentSpeed = speed
	for index, i in enumerate(indices):
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
		if count == currentSpeed or index > len(indices) - 30:
			pygame.display.update(updateRects)
			updateRects = []
			count = 0
	# if not restore:
   	# 	win.fill(white)
	pygame.display.update()
	return

def squareWhiteOutAlgorithm(grid, rows, width):
	mp = {}
	while True:
		win.fill(black)
		pygame.display.update()
		changeColorByRandom(grid, rows)
		pygame.time.wait(7000)
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
	rows = w // 2
	cols = h // 2

	print(rows)
	grid = makeGrid(rows, cols, width, content)
	draw(win,grid,rows, width)
	# win.fill(black)
	pygame.display.update()
	while run:

		for event in pygame.event.get(): 
			if event.type==pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				# if event.key == pygame.K_RETURN:
				# 	print("clicked")
				# 	sparkleAlgorithm(grid, rows)

				if event.key == pygame.K_c:
					squareWhiteOutAlgorithm(grid, rows, width)

main(win, w)
pygame.quit()