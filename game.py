import pygame
import sys
import random

pygame.init()

screenWidth, screenHeight = 720, 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
try:
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
except:
    print("Icon not found.")
pygame.display.set_caption('Blingo Blocko')

fontSmall = pygame.font.SysFont('aharoni', 48)
fontMedium = pygame.font.SysFont('aharoni', 56)
fontLarge = pygame.font.SysFont('aharoni', 72)

gameState = False  
gameoverState = False
score = 0

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

blockColors = {
    0: (50, 50, 95),      
    1: (250, 120, 140),   
    2: (255, 140, 105),   
    3: (255, 240, 115),   
    4: (115, 255, 180),   
    5: (150, 230, 255),   
    6: (150, 150, 255),   
    7: (230, 150, 255),  
}
blockShapes = {
    "T": ([[1, 1, 1], [0, 1, 0]], 1),
    "C": ([[1, 1, 1], [1, 0, 1]], 2),
    "O": ([[1, 1], [1, 1]], 3),
    "S": ([[0, 1, 1], [1, 1, 0]], 4),
    "I": ([[1, 1, 1, 1]], 5),
    "L": ([[1, 0], [1, 1]], 6),
    "P": ([[1, 1, 1], [1, 1, 0]], 7),
}


def block_placeable(block, gridX, gridY):
    blockShape, blockColor = block
    for rowOffset, row in enumerate(blockShape):
        for colOffset, value in enumerate(row):
            if value != 0:
                newRow = gridY + rowOffset
                newCol = gridX + colOffset
                if newRow >= 8 or newCol >= 8 or tiles[newRow][newCol] != 0:
                    return False
    return True

def place_available(block):
    for row in range(8):
        for col in range(8):
            if block_placeable(block, col, row):
                return True
    return False

def get_placeable_block():
    placeableBlocks = [block for block in blockShapes.values() if place_available(block)]
    return random.choice(placeableBlocks) if placeableBlocks else None

def rotate_block(block):
    shape, color = block
    return ([list(row) for row in zip(*shape[::-1])], color)

def flip_block(block):
    shape, color = block
    return ([row[::-1] for row in shape], color)

curBlock = get_placeable_block()
nextBlock = get_placeable_block()

while True:
    def block_placeable(block, gridX, gridY):
        blockShape, blockColor = block
        for rowOffset, row in enumerate(blockShape):
            for colOffset, value in enumerate(row):
                if value != 0:
                    newRow = gridY + rowOffset
                    newCol = gridX + colOffset
                    if newRow >= 8 or newCol >= 8 or tiles[newRow][newCol] != 0:
                        return False
        return True

    def place_available(block):
        for row in range(8):
            for col in range(8):
                if block_placeable(block, col, row):
                    return True
        return False

    def draw_preview(block, gridX, gridY):
        blockShape, blockColor = block
        canPlace = block_placeable(block, gridX, gridY)
        previewColor = (255, 255, 255, 140) if canPlace else (225, 0, 0, 140)
        
        for rowOffset, row in enumerate(blockShape):
            for colOffset, value in enumerate(row):
                if value != 0:
                    newRow = gridY + rowOffset
                    newCol = gridX + colOffset
                    if 0 <= newRow < 8 and 0 <= newCol < 8:
                        rect = pygame.Surface((90, 90), pygame.SRCALPHA)
                        rect.fill(previewColor)
                        screen.blit(rect, (newCol * 90, newRow * 90))

    def draw_current_preview():
        if curBlock:
            blockShape, blockColor = curBlock
            previewScreen = pygame.Surface((180, 180), pygame.SRCALPHA)
            previewScreen.fill((0, 0, 0, 60))  
            
            blockWidth = len(blockShape[0]) * 40
            blockHeight = len(blockShape) * 40
            startX = (180 - blockWidth) // 2
            startY = (180 - blockHeight) // 2
            
            for rowOffset, row in enumerate(blockShape):
                for colOffset, value in enumerate(row):
                    if value != 0:
                        pygame.draw.rect(
                            previewScreen,
                            blockColors[blockColor],
                            (startX + colOffset*40, startY + rowOffset*40, 40, 40)
                        )
            screen.blit(previewScreen, (520, 240))

    def draw_next_preview():
        if nextBlock:
            blockShape, blockColor = nextBlock
            previewScreen = pygame.Surface((180, 180), pygame.SRCALPHA)
            previewScreen.fill((0, 0, 0, 60)) 
            
            blockWidth = len(blockShape[0]) * 40
            blockHeight = len(blockShape) * 40
            startX = (180 - blockWidth) // 2
            startY = (180 - blockHeight) // 2
            
            for rowOffset, row in enumerate(blockShape):
                for colOffset, value in enumerate(row):
                    if value != 0:
                        pygame.draw.rect(
                            previewScreen,
                            blockColors[blockColor],
                            (startX + colOffset*40, startY + rowOffset*40, 40, 40)
                        )
            screen.blit(previewScreen, (520, 520))

    def place_block(block, gridX, gridY):
        global score
        blockShape, blockValue = block
        for rowOffset, row in enumerate(blockShape):
            for colOffset, value in enumerate(row):
                if value != 0:
                    tiles[gridY + rowOffset][gridX + colOffset] = blockValue
        score += sum(row.count(1) for row in blockShape)

    def check():
        global score
        for row in range(8):
            if all(tile != 0 for tile in tiles[row]):
                tiles[row] = [0]*8
                score += 100
        for col in range(8):
            if all(tiles[row][col] != 0 for row in range(8)):
                for row in range(8):
                    tiles[row][col] = 0
                score += 100

    def draw_tiles():
        screen.fill((50, 50, 95))
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(screen, blockColors[tiles[row][col]], (col*90, row*90, 90, 90))
                pygame.draw.rect(screen, (70, 65, 110), (col*90, row*90, 90, 90), 1)

    def draw_score():
        text = str(score)
        shadow = fontLarge.render(text, True, (0, 0, 0))
        screen.blit(shadow, (361 - shadow.get_width()//2, 11))
        scoreText = fontLarge.render(text, True, (255, 255, 255))
        screen.blit(scoreText, (360 - scoreText.get_width()//2, 10))

    def check_gameoverState():
        return not place_available(curBlock)

    def reset_game():
        global tiles, score, curBlock, nextBlock, gameoverState
        tiles = [[0 for _ in range(8)] for _ in range(8)]
        score = 0
        curBlock = get_placeable_block()
        nextBlock = get_placeable_block()
        gameoverState = False

    def draw_main_menu():
        screen.fill((50, 50, 95))
        menuTitle = fontLarge.render("Blingo Blocko", True, (255, 240, 115))
        menuSubtitle = fontMedium.render("Press [ENTER] to play!", True, (255, 255, 255))
        
        screen.blit(menuTitle, (360 - menuTitle.get_width()//2, 250))
        screen.blit(menuSubtitle, (360 - menuSubtitle.get_width()//2, 350))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not gameState:
                    gameState = True
                    reset_game()
                elif gameoverState:
                    gameState = False

        if gameState and not gameoverState:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                gridX, gridY = mouseX // 90, mouseY // 90
                if 0 <= gridX < 8 and 0 <= gridY < 8:
                    if block_placeable(curBlock, gridX, gridY):
                        place_block(curBlock, gridX, gridY)
                        check()
                        curBlock = nextBlock
                        nextBlock = get_placeable_block()
                        if check_gameoverState() or nextBlock is None:
                            gameoverState = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    curBlock = rotate_block(curBlock)
                if event.key == pygame.K_f:
                    curBlock = flip_block(curBlock)

    if gameState:
        draw_tiles()
        if not gameoverState:
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX, gridY = mouseX // 90, mouseY // 90
            draw_preview(curBlock, gridX, gridY)
            draw_current_preview()
            draw_next_preview()
            
            currentlabel = fontSmall.render("Current:", True, (255, 255, 255))
            currentShadow = fontSmall.render("Current:", True, (0, 0, 0))
            nextLabel = fontSmall.render("Next:", True, (255, 255, 255))
            nextShadow = fontSmall.render("Next:", True, (0, 0, 0))

            controlsBG = pygame.Surface((200, 140), pygame.SRCALPHA)
            controlsBG.fill((0, 0, 0, 60)) 
            screen.blit(controlsBG, (515, 40))  

            scoreBG = pygame.Surface((220, 80), pygame.SRCALPHA)
            scoreBG.fill((0, 0, 0, 60))
            screen.blit(scoreBG, (360 - 110, 5))  

            controlsText = [
                ("LMB = Place", 520, 140),
                ("R = Rotate", 520, 90),
                ("F = Flip", 520, 50)
            ]

            for text, x, y in controlsText:
                shadow = fontSmall.render(text, True, (0, 0, 0))
                screen.blit(shadow, (x + 2, y + 2))
                screen.blit(shadow, (x - 1, y - 1))
                main_text = fontSmall.render(text, True, (255, 255, 255))
                screen.blit(main_text, (x, y))

            
            screen.blit(currentShadow, (522, 222 - currentlabel.get_height()))
            screen.blit(currentlabel, (520, 220 - currentlabel.get_height()))
            screen.blit(nextShadow, (522, 502 - nextLabel.get_height()))
            screen.blit(nextLabel, (520, 500 - nextLabel.get_height()))
            
            draw_score()
        else:
            overlay = pygame.Surface((720, 720), pygame.SRCALPHA)
            overlay.fill((255, 80, 80, 128))
            screen.blit(overlay, (0, 0))

            gameoverText = fontLarge.render("Game Over: " + str(score), True, (255, 255, 255))
            continuteText = fontSmall.render("Press [ENTER] to Continue", True, (255, 255, 255))
            
            screen.blit(gameoverText, (360 - gameoverText.get_width()//2, 300))
            screen.blit(continuteText, (360 - continuteText.get_width()//2, 380))
    else:
        draw_main_menu()

    pygame.display.update()

