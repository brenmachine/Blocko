import pygame
import sys

pygame.init()

screenWidth, screenHeight = 720, 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Blingo Blocko')

tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0],
]
columnIndex = 0
rowIndex = 0

screen.fill('#3a3a4a')
#print(tiles[4][0]) matrix for drawing
for x in tiles:
    for y in x:
        pygame.draw.rect(screen, (255, 255, 255), (rowIndex, columnIndex, 90, 90), 1)
        rowIndex += 90
    columnIndex += 90
    rowIndex = 0
            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #screen.fill('#3a3a4a')

    #checkrowfill()
    #checkcolfill()
    #generate blocks here
    pygame.display.update()
