import pygame
import math
from queue import PriorityQueue

w = 800
win = pygame.display.set_mode((w,w))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")

red = (255,0,0)
green = (0,255,0)
blue = (51,153,255)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
purple = (153,51,255)
orange = (255,165,0)
grey = (192,192,192)
turquoise = (0,153,153)


class Node:
	def __init__(self, row, col, width, totalRows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width 
		self.color = white
		self.neighbors = []
		self.width = width
		self.totalRows = totalRows

	def pos(self):
		return self.x, self.y  

	def isClosed(self):
		return self.color == orange

	def isOpen(self):
		return self.color == yellow

	def isBarrier(self):
		return self.color == black

	def isStart(self):
		return self.color == turquoise

	def isEnd(self):
		return self.color == red

	def reset(self):
		self.color = white

	def makeClosed(self):
		self.color = orange

	def makeOpen(self):
		self.color = yellow

	def makeBarrier(self):
		self.color = black

	def makeStart(self):
		self.color = turquoise

	def makeEnd(self):
		self.color = red

	def makePath(self):
		self.color = purple

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def updateNeighbors(self, grid):
		if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isBarrier(): #down
			self.neighbors.append(grid[self.row + 1][self.col])
			if self.col > 0 and self.row< self.totalRows -1 and not grid[self.row+1][self.col-1].isBarrier(): #downleft
				self.neighbors.append(grid[self.row+1][self.col-1])
			if self.row < self.totalRows -1 and self.col <self.totalRows - 1 and not grid[self.row + 1][self.col +1 ].isBarrier(): #downright
				self.neighbors.append(grid[self.row + 1][self.col+1])

		if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): #up
			self.neighbors.append(grid[self.row - 1][self.col])
			if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col-1].isBarrier(): #upleft
				self.neighbors.append(grid[self.row - 1][self.col-1])
			if self.col < self.totalRows - 1 and self.row >0 and not grid[self.row-1][self.col+1].isBarrier(): #upright
				self.neighbors.append(grid[self.row-1][self.col+1])	


		if self.col < self.totalRows - 1 and not grid[self.row][self.col+1].isBarrier(): #right
			self.neighbors.append(grid[self.row][self.col+1])
			if self.row < self.totalRows -1 and self.col <self.totalRows - 1 and not grid[self.row + 1][self.col +1 ].isBarrier(): #downright
				self.neighbors.append(grid[self.row + 1][self.col+1])
			if self.col < self.totalRows - 1 and self.row >0 and not grid[self.row-1][self.col+1].isBarrier(): #upright
				self.neighbors.append(grid[self.row-1][self.col+1])


		if self.col > 0 and not grid[self.row][self.col-1].isBarrier(): #left
			self.neighbors.append(grid[self.row][self.col-1])
			if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col-1].isBarrier(): #upleft
				self.neighbors.append(grid[self.row - 1][self.col-1])
			if self.col > 0 and self.row< self.totalRows -1 and not grid[self.row+1][self.col-1].isBarrier(): #downleft
				self.neighbors.append(grid[self.row+1][self.col-1])

		

	def __lt__(self, other):
		return False



def algorithm(draw, grid, start, end):
	count = 0
	openSet = PriorityQueue()
	openSet.put((0, count, start))
	cameFrom = {}
	gScore = {node: float("inf") for row in grid for node in row}
	gScore[start] = 0
	fScore = {node: float("inf") for row in grid for node in row}
	fScore[start] = h(start.pos(), end.pos())

	openSetHash = {start}

	while not openSet.empty():

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = openSet.get()[2]
		openSetHash.remove(current)

		if current is end:
			reconstructPath(cameFrom, end, draw)
			end.makeEnd()
			return True

		for neighbor in current.neighbors:
			tempG = gScore[current] + h(current.pos(), neighbor.pos())

			if tempG < gScore[neighbor]:
				cameFrom[neighbor] = current
				gScore[neighbor] = tempG
				fScore[neighbor] = tempG + h(neighbor.pos(), end.pos())

				if neighbor not in openSetHash:
					count += 1
					openSet.put((fScore[neighbor],count,neighbor))
					openSetHash.add(neighbor)
					if neighbor!= start and neighbor != end:
						neighbor.makeOpen()
		draw()

		if current!=start and current!= end:
			current.makeClosed()

	return None


def algorithm2(draw, grid, start, end):
	count = 0
	openSet = PriorityQueue()
	openSet.put((0, count, start))
	cameFrom = {}
	gScore = {node: float("inf") for row in grid for node in row}
	gScore[start] = 0
	fScore = {node: float("inf") for row in grid for node in row}
	fScore[start] = h(start.pos(), end.pos())

	openSetHash = {start}

	while not openSet.empty():

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = openSet.get()[2]
		openSetHash.remove(current)

		if current is end:
			reconstructPath(cameFrom, end, draw)
			end.makeEnd()
			return True

		for neighbor in current.neighbors:
			tempG = gScore[current] + h(current.pos(), neighbor.pos())

			if tempG < gScore[neighbor]:
				cameFrom[neighbor] = current
				gScore[neighbor] = tempG
				fScore[neighbor] = tempG 

				if neighbor not in openSetHash:
					count += 1
					openSet.put((fScore[neighbor],count,neighbor))
					openSetHash.add(neighbor)
					if neighbor!= start and neighbor != end:
						neighbor.makeOpen()
		draw()

		if current!=start and current!= end:
			current.makeClosed()

	return None



def h(p1,p2):
	x1, y1 = p1 
	x2, y2 = p2
	return math.sqrt((float(x1-x2))**2 + (float(y1-y2))**2)



def reconstructPath(cameFrom, current, draw):
	for i in grid:
		for j in i:
			if j.color == yellow or j.color == orange:
				j.reset()

	while current in cameFrom:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = cameFrom[current]
		if current.color != turquoise and current.color != red:
			current.makePath()
		draw()
		

def makeGrid(rows, width):
	grid = []
	gap = width//rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid 


def drawGrid(win, rows, width):
	gap = width//rows
	for i in range(rows):
		pygame.draw.line(win, grey, (0, i*gap), (width,i*gap))
		pygame.draw.line(win, grey, (i*gap, 0), (i*gap,width))



def draw(win, grid, rows, width):
	win.fill(white)

	for row in grid:
		for node in row:
			node.draw(win)

	drawGrid(win, rows, width)
	pygame.display.update()



def getClicked(pos, rows, width):
	gap = width//rows
	y, x = pos

	row = y//gap
	col = x//gap

	return row, col


def main(win, width):
	rows = 40
	global grid
	grid = makeGrid(rows, width)

	start = None
	end = None

	run = True

	while run:
		draw(win,grid,rows, width)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = getClicked(pos, rows, width)
				node = grid[row][col]


				if node != end and node != start:
					node.makeBarrier()
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = getClicked(pos, rows, width)
				node = grid[row][col]
				node.reset()

				if node!=end and node!=start:
					if not start and not end:
						start = node
						node.makeStart()
					elif not start:
						start = node
						node.makeStart()

					elif not end:
						end = node
						node.makeEnd()

				elif node is start:
					start = None
					node.reset()

				elif node is end:
					end = None
					node.reset()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.updateNeighbors(grid)

					algorithm(lambda: draw(win,grid,rows, width), grid, start, end)

				if event.key == pygame.K_RETURN and start and end:
					for row in grid:
						for node in row:
							node.updateNeighbors(grid)

					algorithm2(lambda: draw(win,grid,rows, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = makeGrid(rows,width)



main(win, w)
pygame.quit()
