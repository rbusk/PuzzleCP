import pygame
from objects import *
import random
from solution import *
import copy

def get_window_width(puzzleSize,numberOfTiles):
	tileLength = 150 + 125*numberOfTiles
	puzzleLength = 200+75*puzzleSize

	if tileLength > puzzleLength:
		return tileLength
	else:
		return puzzleLength

def get_print_start_point(windowWidth, spaceBetweenTile, numberOfTile, tileSize):
	puzzleWidth = numberOfTile*tileSize + (numberOfTile-1)*spaceBetweenTile
	start = (windowWidth-puzzleWidth)/2
	return start

def get_front_of_puzzle(tile,x,y,tile_size,short_edge):
	color = tile.get_color()
	puzzle = FrontEdge(x,y,color[0],color[3],color[2],short_edge,tile_size) 
	return puzzle

def get_middle_of_puzzle(tile,x,y,tile_size,short_edge):
	color = tile.get_color()
	puzzle = MiddleEdge(x,y,color[0],color[2],short_edge,tile_size) 
	return puzzle

def get_end_of_puzzle(tile,x,y,tile_size,short_edge):
	color = tile.get_color()
	puzzle = BackEdge(x,y,color[0],color[1],color[2],short_edge,tile_size) 
	return puzzle

def shuffle_tile(tileList,numberOfTiles):

	#for each tile, swap with another random tile
	for x in xrange(numberOfTiles):
		colors_temp = tileList[x].get_color()
		n = random.randint(0, numberOfTiles-1) #random tile number to swap with
		tileList[x].set_color(tileList[n].get_color())
		tileList[n].set_color(colors_temp)

	tileList = rotate_tile(tileList, numberOfTiles)

	return tileList #return randomly swapped and rotated tiles

def rotate_tile(tileList, numberOfTiles):

	for x in xrange(numberOfTiles):
			tileList[x].rotate_tile()
	return tileList
		

class Puzzle:

	def __init__(self, screen):

		#self.tileList is list of possible tiles, self.solutionList is list of actual tiles that solve puzzle
		#puzzleList is list of tiles that user has added to solve the puzzle
		self.tileList = []
		self.solutionList = []
		self.puzzleList = []
                self.solution_tree = None

		#height and width
		self.h = 600
		self.w = 600
		self.tile_size = 75

		self.screen = screen

		self.back_button = pygame.Rect(20, 20, 75, 50)
		self.solve_button = pygame.Rect(self.w/2 - 100 , 400, 150, 75)
		self.check_button = pygame.Rect(-200, 400, 200, 75)

		self.font = pygame.font.Font(None, 30)
		self.text = self.font.render("", True, BLACK)

	#create a blank puzzle with n tiles
	def create_blank_puzzle(self, n):
		
		self.numberOfTiles = n
		self.puzzleSize = n

		self.w = get_window_width(self.puzzleSize,self.numberOfTiles)

		#x and y coordinates of upper left of first tile
		space = 50
		x = get_print_start_point(self.w,space,self.numberOfTiles,self.tile_size)
		y = 250
		s = self.tile_size + space#space b/t tiles
		blankTile = Tile(600,600,self.tile_size,(WHITE,WHITE,WHITE,WHITE))

		#add n blank tiles to tileList

		for i in range(0,self.numberOfTiles):
			self.tileList.append(Tile(x+i*s, y,self.tile_size, "blank"))

		#puzzle draw
		xP = get_print_start_point(self.w,0,self.puzzleSize,self.tile_size)
		yP = 75
		sP = 75 #space between pieces
		shortEdge = 12.5

		self.puzzleList.append(get_front_of_puzzle(self.tileList[0],xP,yP,self.tile_size,shortEdge))
		for k in range(1,self.puzzleSize-1):
			self.puzzleList.append(get_middle_of_puzzle(self.tileList[k],xP+k*sP,yP,self.tile_size,shortEdge))
		self.puzzleList.append(get_end_of_puzzle(self.tileList[self.puzzleSize-1],xP+(self.puzzleSize-1)*sP,yP,self.tile_size,shortEdge))

	#checks all edges and tiles to see if mouse is inside
	#if so, sets that piece to the input color
	def set_piece_color(self, color, pos):

		#in case a tile color has been changed, set self.text to ""
		self.text = self.font.render("", True, BLACK)

		
		blankTile = Tile(600,600,self.tile_size,(WHITE,WHITE,WHITE,WHITE))

		currentPiece = 0
		for piece in self.puzzleList:
			currentPiece += 1
			#if currentPiece is 1 or max number, then check middle segment
			if currentPiece == 1 or currentPiece == self.numberOfTiles:
				if piece.is_inside_middle(pos):
					piece.set_middle_color(color)

			#also check top and bottom segments for every edge
			if piece.is_inside_top(pos):
				piece.set_top_color(color)
			if piece.is_inside_bottom(pos):
				piece.set_bottom_color(color)
		
		for tile in self.tileList:
			#get number of triangle if mouse is inside
			n = tile.is_inside_triangle(pos)
			if (n!= -1):
				tile.set_triangle_color(color, n)


	def get_n_tiles(self):

		self.screen = pygame.display.set_mode((self.w, self.h))

		self.screen.fill(WHITE)

		running = 1

		text1 = self.font.render("How many tiles would you like in your puzzle?", True, BLACK)
		text2 = self.font.render("Press a number 3 - 9.", True, BLACK)

		while running:

			#check events
			event = pygame.event.poll()
			if event.type == pygame.QUIT:
				running =0
				return -1

	
			#check if r,y,g,b pressed; if so, check if mouse is inside either an edge or a tile
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_3:
					return 3
				if event.key == pygame.K_4:
					return 4
				if event.key == pygame.K_5:
					return 5
				if event.key == pygame.K_6:
					return 6
				if event.key == pygame.K_7:
					return 7
				if event.key == pygame.K_8:
					return 8
				if event.key == pygame.K_9:
					return 9

			self.screen.blit(text1, (20, 100))
			self.screen.blit(text2, (20, 150))
			pygame.display.flip()


	def user_create_puzzle(self):

		nTiles = self.get_n_tiles()

		if nTiles == -1:
			return

		self.create_blank_puzzle(nTiles)
		self.screen = pygame.display.set_mode((self.w, self.h))
		
		self.solve_button.centerx = self.screen.get_rect().centerx
		
		blankTile = Tile(600,600,self.tile_size,(WHITE,WHITE,WHITE,WHITE))
                for i in range(0, nTiles):
                    self.solutionList.append(blankTile)

                running = 1

		while running:

			#check events
			event = pygame.event.poll()
			if event.type == pygame.QUIT:
				running =0
				return 0

	
			#check if r,y,g,b pressed; if so, check if mouse is inside either an edge or a tile
			if event.type == pygame.KEYUP:

				pos = pygame.mouse.get_pos()
				if event.key == pygame.K_r:
					self.set_piece_color(RED, pos)
				if event.key == pygame.K_b:
					self.set_piece_color(BLUE, pos)
				if event.key == pygame.K_y:
					self.set_piece_color(YELLOW, pos)
				if event.key == pygame.K_g:
					self.set_piece_color(GREEN, pos)

			if event.type == pygame.MOUSEBUTTONUP:

				#check buttons
				r = self.check_buttons()
				if r == -1:
					running = 0
					return 1


			self.draw_puzzle()
			self.draw_buttons()
			pygame.display.flip()

	def create_random_puzzle(self):
		
		#x and y coordinates of upper left of first tile
		space = 50
		x = get_print_start_point(self.w,space,self.numberOfTiles,self.tile_size)
		y = 250
		s = self.tile_size + space#space b/t tiles
		blankTile = Tile(600,600,self.tile_size,(WHITE,WHITE,WHITE,WHITE))

		#make tiles based on previous tile color
		self.tileList.append(Tile(x, y, self.tile_size))
		self.solutionList.append(blankTile)
		for i in range(1,self.numberOfTiles):
			self.tileList.append(Tile(x+i*s, y,self.tile_size,self.tileList[i-1].get_right_color()))
			self.solutionList.append(blankTile)

		#puzzle draw
		xP = get_print_start_point(self.w,0,self.puzzleSize,self.tile_size)
		yP = 75
		sP = 75 #space between pieces
		shortEdge = 12.5

		#generate puzzle based on tile colors
		self.puzzleList.append(get_front_of_puzzle(self.tileList[0],xP,yP,self.tile_size,shortEdge))
		for k in range(1,self.puzzleSize-1):
			self.puzzleList.append(get_middle_of_puzzle(self.tileList[k],xP+k*sP,yP,self.tile_size,shortEdge))
		self.puzzleList.append(get_end_of_puzzle(self.tileList[self.puzzleSize-1],xP+(self.puzzleSize-1)*sP,yP,self.tile_size,shortEdge))

		#random shuffle of self.tileList
		self.tileList = shuffle_tile(self.tileList,self.numberOfTiles)

	def play(self):

		self.numberOfTiles = self.get_n_tiles()
		self.puzzleSize = self.numberOfTiles

		self.w = get_window_width(self.puzzleSize,self.numberOfTiles)
		self.screen = pygame.display.set_mode((self.w, self.h))

		self.solve_button.centerx = self.screen.get_rect().centerx/2
		self.check_button.centerx = self.screen.get_rect().centerx/2*3

		#set up puzzle and tiles for user's selection
		self.create_random_puzzle()

		#current selected tile
		currentTile = 0
		
		blankTile = Tile(600,600,self.tile_size,(WHITE,WHITE,WHITE,WHITE))

		#pygame.init()
		pygame.display.set_caption("Course Project 3: Interactive Puzzle")

		running = 1
		solved = False

		while running:

			#check events
			event = pygame.event.poll()
			if event.type == pygame.QUIT:
				running =0
				return 0

			#check if user has pressed a key
			if event.type == pygame.KEYUP:

				#quit
				if event.key == pygame.K_q:
					running = 0
			
				#delete
				if event.key == pygame.K_d:
					pos = pygame.mouse.get_pos()

					#iterate through pieces in puzzleList to see if mouse is inside
					currentPiece = 0
					for piece in self.puzzleList:
						currentPiece += 1
						if piece.is_inside(pos):
							self.solutionList[currentPiece-1] = blankTile
							self.text = self.font.render("", True, BLACK)

			if event.type == pygame.MOUSEBUTTONUP:

				#check buttons
				r = self.check_buttons()
				if r == -1:
					running = 0
					return 1

				pos = pygame.mouse.get_pos()

				#get number of tile from self.tileList (lower tiles) if one was clicked
				#currentTile is number of selected tile from choices
				place = 0
				for tile in self.tileList:
					place += 1
					if tile.is_inside(pos):
						if currentTile == 0:
							currentTile += place

				#iterate through each piece in puzzleList (upper tiles)
				#check to see if mouse click was inside each piece
				currentPiece = 0
				for piece in self.puzzleList:
					currentPiece += 1
					if piece.is_inside(pos):
						#if user has selected a tile to place
						if currentTile != 0:
							self.text = self.font.render("", True, BLACK)
							rect = piece.get_rect() #rect for piece in puzzleList
							tile = Tile(rect[0],rect[1],rect[2],self.tileList[currentTile-1].get_color()) #create tile to place in puzzle
							self.solutionList[currentPiece-1] = tile #place in puzzle

						#if user has not selected a tile to place
						else:
							#if selected tile in puzzle is not blank
							if self.solutionList[currentPiece-1] != blankTile:
								self.text = self.font.render("", True, BLACK)
								rect = piece.get_rect() #rect for piece in puzzleList
								c = self.solutionList[currentPiece-1].get_color() #get color list for tiles
								newColors = ((c[3], c[0], c[1], c[2]))
								tile = Tile(rect[0], rect[1], rect[2], newColors) #create new tile to replace the old one
								self.solutionList[currentPiece-1] = tile #place in puzzle

						currentTile = 0
							
					# Display solution status
					font = pygame.font.Font(None, 30)
					text = ''

					'''if solved:
						text = font.render("Valid Solution", True, GREEN)
					else: 
						text = font.render("Valid Solution", True, WHITE)
					self.screen.blit(text, (self.w/2-75, self.h/2))'''
			#print puzzle
			self.draw_puzzle()

			#print buttons
			self.draw_buttons()

			pygame.display.flip()

	def draw_buttons(self):
		#draw back_button
		pygame.draw.rect(self.screen, BLUE, self.back_button, 0)

		#create text for back_button
		back_text = self.font.render("BACK", True, (255, 255, 255))
		back_text_pos = back_text.get_rect()
		back_text_pos.centerx = self.back_button.centerx
		back_text_pos.centery = self.back_button.centery
		self.screen.blit(back_text, back_text_pos)

		#draw solve_button
		pygame.draw.rect(self.screen, BLUE, self.solve_button, 0)

		#create text for solve_button

		solve_text = self.font.render("SOLVE", True, (255, 255, 255))
		solve_text_pos = solve_text.get_rect()
		solve_text_pos.centerx = self.solve_button.centerx
		solve_text_pos.centery = self.solve_button.centery
		self.screen.blit(solve_text, solve_text_pos)

		#draw check_button
		pygame.draw.rect(self.screen, BLUE, self.check_button, 0)

		#create text for check_button
		check_text = self.font.render("CHECK SOLUTION", True, (255, 255, 255))
		check_text_pos = check_text.get_rect()
		check_text_pos.centerx = self.check_button.centerx
		check_text_pos.centery = self.check_button.centery
		self.screen.blit(check_text, check_text_pos)

		#display text for self.text
		text_pos = self.text.get_rect()
		text_pos.centerx = self.screen.get_rect().centerx
		text_pos.centery = 550
		self.screen.blit(self.text, text_pos)

	def solution_check(self):
                # SolutionChecker class builds a 2PDA from the user's solution
                # using SolutionTree's solutions to create the transitions
                pda = SolutionChecker(self.solutionList, self.solution_tree.solutions)
                
                # Ryan's almost working code. so close... :/
                """solutions = self.solution_tree.solutions
		answer = copy.copy(self.solutionList)
		ans_len = len(answer)
		stack = ['$']
		accept = False
		reject = False
		isFirst = True
		get_matches = True
		solution = 0
		while accept == False and reject == False and len(answer) != 0:
			print stack
			tile = answer.pop(-1)

			if isFirst == True:
				isFirst = False
				if get_matches == True:
					get_matches = False
					matches = self.get_matches_of_tile(tile)
					if len(matches) > 0:
						position = matches[0]
					else:
						reject = False
						continue
					i = position[0]
					j = position[1]
					solution = i
					print i
					if position == None:
						reject = True
						print 'Not correct solution'
						continue
					print matches
				if j != ans_len-1:
					print 'First spot incorrect'
					reject = True
					continue
				string = str(i) + str(j)
				stack.append(string)
				continue
			else:
				position = self.get_position_of_tile(tile,solution)
				if position == None:
					stack.pop()
					if len(matches) > 1:
						matches.pop(0)
						position = matches[0]
						stack.append(str(position[0])+str(position[1]))
						solution = position[0]
						answer = copy.copy(self.solutionList)
						tile = answer.pop(-1)
						continue
					reject = True
					print 'Not correct solution'
					continue
				i = position[0]
				j = position[1]
				string = str(i) + str(j)
			print string

			previous = stack.pop()
			if previous != str(i)+str(j+1):
				if len(matches) > 1:
					matches.pop(0)
					print matches
					position = matches[0]
					stack.append(str(position[0])+str(position[1]))
					solution = position[0]
					print solution
					answer = copy.copy(self.solutionList)
					tile = answer.pop(-1)
					continue
				reject = True
				print 'Not correct order'
			else:
				stack.append(string)

			#read tile off string
			if len(answer) == 0:
				last = stack.pop()
				position = self.get_position_of_tile(last,j)
				if int(previous) == int(last)+1:
					if len(stack) == 1:
						dollar = stack.pop()
						if dollar == '$':
							accept = True
							print 'Valid Solution' """

	def get_position_of_tile(self,tile,solution=None):
		for i,tiles in enumerate(self.solution_tree.solutions):
			try:
				j = tiles.index(tile)
			except ValueError:
				continue
			position = [i,j]
			if solution != None:
				if i == solution:
					return position
			else:
				return position
			
			return None
	
	def get_matches_of_tile(self,tile):
		positions = []
		for i,tiles in enumerate(self.solution_tree.solutions):
			try:
				j = tiles.index(tile)
			except ValueError:
				continue
			positions.append([i,j])
			
		return positions


	def draw_puzzle(self):
		self.screen.fill(WHITE)
		for piece in self.puzzleList:
			piece.draw(self.screen)
		for tile in self.tileList:
			tile.draw(self.screen)
		for solution in self.solutionList:
			solution.draw(self.screen)

	#returns 1 if all segments and tiles are colored and 0 if otherwise
	def is_puzzle_colored(self):
		#check piece in the puzzle
		for piece in self.puzzleList:
			if not piece.is_colored():
				return 0

		#check each tile in the list of tile options
		for tile in self.tileList:
			if not tile.is_colored():
				return 0
			
		#otherwise, all tiles and segments are colored, so return 1
		return 1

	def is_solution_colored(self):
		for solution in self.solutionList:
			if not solution.is_colored():
				return 0
		return 1
	# returns 1 if all tiles are placed in puzzle and 0 otherwise
	def is_puzzle_completed(self):

		blankTile = Tile(600,600,self.tile_size,(WHITE,WHITE,WHITE,WHITE))

		for piece in self.solutionList:
			if piece==blankTile:
				return 0

		return 1


	def check_buttons(self):

		pos = pygame.mouse.get_pos()
		# Print Solution Tree
		self.solution_tree = Solution_Tree(self.tileList, self.puzzleList)

		#if solve button hit and puzzle is completely colored, then use solver to solve puzzle
		if self.solve_button.collidepoint(pos) and self.is_puzzle_colored():
			print '\n\n DFA SOLUTION TREE \n\n' + str(self.solution_tree.root) + '\n\n'
			self.solve_puzzle()
			return 1

		if self.back_button.collidepoint(pos):
			return -1

		if self.check_button.collidepoint(pos) and self.is_puzzle_completed():
			self.solution_check()
			return 1

	def solve_puzzle(self):
		if len(self.solution_tree.solutions) == 0 :
			self.text = self.font.render("There is no solution.", True, BLACK)
			blankTile = Tile(600,600,self.tile_size,(WHITE,WHITE,WHITE,WHITE))

			#fill with blank tiles
			for i in range(0, len(self.puzzleList)):
				self.solutionList[i] = blankTile


		else:
			self.text = self.font.render("Solved!", True, BLACK)
			# Fill the puzzle with a random valid solution if more than one
			randInt = random.randint(0, len(self.solution_tree.solutions)-1)
			aSolution = self.solution_tree.solutions[randInt]
			for i in range(0,len(self.puzzleList)):
				rect = self.puzzleList[i].get_rect()
				self.solutionList[i] = Tile(rect[0], rect[1], rect[2], aSolution[i].get_color())

