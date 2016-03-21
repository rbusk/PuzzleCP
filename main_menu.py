import pygame
import sys
from puzzle import puzzle

if __name__ == '__main__':
		w = 600
		h = 400

		pygame.init()
		screen = pygame.display.set_mode((w, h))
		screen.fill((255, 255, 255))

		running = 1
		rect1 = pygame.Rect(0, 0, 600, 200)
		rect2 = pygame.Rect(0, 200, 600, 200)

		font = pygame.font.Font(None, 30)

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = 0

				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if rect1.collidepoint(pos):
						#pygame.display.quit()
						puzzle = puzzle()
						puzzle.play()
						#pygame.display.quit()
						#pygame.quit()
						#break
					elif rect2.collidepoint(pos):
						print 'run script 2'

			#draw rectangles
			pygame.draw.rect(screen, (0, 0, 0), rect1, 1)
			pygame.draw.rect(screen, (0, 0, 0), rect2, 1)
			
			#render text
			text1 = font.render("Solve a puzzle", True, (0, 0, 0))
			text2 = font.render("Create your own puzzle", True, (0, 0, 0))
			screen.blit(text1, (w/2-75, h/4))
			screen.blit(text2, (w/2-125, 3*h/4))

			pygame.display.flip()
