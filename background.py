import sys 
import pygame 
import time
import signal


def handler(signum, frame):
	pass

signal.signal(signal.SIGHUP, handler)

pygame.init()
# create fullscreen display 640x480
screen = pygame.display.set_mode((740,580),0)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,0))

while True:
	screen.fill((0,0,0))
	pygame.display.update()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				pygame.quit()
