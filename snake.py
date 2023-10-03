# package imports
import pygame
import random
import logging

# initialization
pygame.init()

MainWindowHeight = 800
MainWindowWidth = 800
MainWindow = pygame.display.set_mode((MainWindowWidth,MainWindowHeight))
pygame.display.set_caption("Snake")

DefaultFontSize = 36
font = pygame.font.Font(None, DefaultFontSize) # none = default font

# Global Variables
LastMovement = None
Run = True
Score = 0

## snake
SnakeXPosition = random.randint(0, MainWindowWidth * 0.75)
SnakeYPosition = random.randint(0, MainWindowHeight * 0.75)
SnakeWidth = 25
SnakeHeight = 25
SnakeVelocity = 2
CurrentSnakeRotation = 0
SnakeSegments = [(SnakeXPosition, SnakeYPosition)]  # List to store snake segments' positions
SnakeLength = 1  # Initial snake length

## colors
Red = (255,0,0)
DarkRed = (150,0,0)
Green = (0,255,0)
Black = (0,0,0)
MainColor = (75, 75, 75)

## apple
ApplePresent = False
AppleWidth = 25
AppleHeight = 25
AppleXPosition = random.randint(0, MainWindowWidth - AppleWidth)
AppleYPosition = random.randint(0, MainWindowHeight - AppleHeight)

# boosters
ActiveBoosters = []
LastSpaceBarPress = 0  # Variable to store the time of the last space bar press

# configuration 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ALIVE = True

def restart():
    import sys
    import os
    os.execv(sys.executable, ['python'] + sys.argv)

# Movement functions
def goRight():
    global SnakeXPosition
    global CurrentSnakeRotation
    CurrentSnakeRotation = 90
    if SnakeXPosition > (MainWindowWidth-(SnakeWidth/2)) :
        SnakeXPosition = 0
    else :
        SnakeXPosition += SnakeVelocity
def goLeft():
    global SnakeXPosition
    global CurrentSnakeRotation
    CurrentSnakeRotation = -90
    if SnakeXPosition < (0 -(SnakeWidth/2)) :
        SnakeXPosition = MainWindowWidth - SnakeWidth
    else:
        SnakeXPosition -= SnakeVelocity
def goUp() :
    global SnakeYPosition
    global CurrentSnakeRotation
    CurrentSnakeRotation = 0
    if SnakeYPosition < (0-(SnakeHeight/2)) :
        SnakeYPosition = MainWindowHeight
    else :
        SnakeYPosition -= SnakeVelocity
def goDown() :
    global SnakeYPosition
    global CurrentSnakeRotation
    CurrentSnakeRotation = 180
    if SnakeYPosition > (MainWindowHeight-(SnakeHeight/2)) : 
        SnakeYPosition = 0
    else :
        SnakeYPosition += SnakeVelocity

def speedBoost():
    global LastMovement, SnakeVelocity
    SnakeVelocity *= 2

def toggleBooster(booster):
    global SnakeVelocity, ActiveBoosters

    logging.debug("booster: " + booster + " active boosters: " + str(ActiveBoosters))
    if booster == "speed":
        if "speed" in ActiveBoosters:
            logging.debug("Toggling booster " + booster + " OFF")
            ActiveBoosters.remove("speed")
            SnakeVelocity = SnakeVelocity * 0.5
        else: 
            logging.debug("Toggling booster " + booster + " ON")
            ActiveBoosters.append("speed")
            speedBoost()

def drawSnake():
    global SnakeSegments, SnakeXPosition, SnakeYPosition, SnakeWidth, SnakeHeight, Green, MainWindow, CurrentSnakeRotation

    snake_surface = pygame.Surface((SnakeWidth, SnakeHeight), pygame.SRCALPHA)

    for segment in SnakeSegments:
        pygame.draw.rect(MainWindow, Green, (segment[0], segment[1], SnakeWidth, SnakeHeight))


        pygame.draw.rect(snake_surface, Green, (0, 0, SnakeWidth, SnakeHeight)) # body
        pygame.draw.rect(snake_surface, Black, (SnakeWidth * 0.14, SnakeHeight * 0.2, (SnakeWidth * 0.3), (SnakeHeight * 0.3))) # left eye
        pygame.draw.rect(snake_surface, Black, (SnakeWidth * 0.63, SnakeHeight * 0.2, (SnakeWidth * 0.3), (SnakeHeight * 0.3))) # right eyes
        pygame.draw.rect(snake_surface, Black, (SnakeWidth * 0.14, SnakeHeight * 0.2, (SnakeWidth * 0.8), (SnakeHeight * 0.15))) # sunglasses
        pygame.draw.rect(snake_surface, Black, (SnakeWidth * 0.14, SnakeHeight * 0.7, (SnakeWidth * 0.8), (SnakeHeight * 0.20))) # mouth
        
        rotated_snake = pygame.transform.rotate(snake_surface, CurrentSnakeRotation)
        rotated_rect = rotated_snake.get_rect(center=(SnakeXPosition + SnakeWidth / 2, SnakeYPosition + SnakeHeight / 2))
        MainWindow.blit(rotated_snake, rotated_rect.topleft)

def drawApple():
    global AppleXPosition, AppleYPosition, AppleWidth, AppleHeight, MainWindow, Red, Apple

    Apple = pygame.Rect(AppleXPosition, AppleYPosition, AppleWidth, AppleHeight)
    pygame.draw.rect(MainWindow, Red, Apple)

def hitSelf():
    global SnakeSegments
    head_position = SnakeSegments[0]
    # Check if the head collides with any of the body segments
    for segment in SnakeSegments[1:]:
        if head_position == segment:
            return True  # Collision detected
    return False  # No collision

def closeGame():
    import sys
    pygame.quit()
    sys.exit()
 
def gameOver():
    global Run, DarkRed, Black, Score, ALIVE
    logging.debug("Game over, score was: " + str(Score))
    MainWindow.fill(DarkRed)
    text = font.render("GAME OVER | Your score was: " + str(Score) + " | Press R to play again.", True, Black)  
    text_position = text.get_rect(center=(MainWindowWidth // 2, MainWindowHeight // 4)) 
    MainWindow.blit(text, text_position) 
    pygame.display.update()
    ALIVE = False

    while ALIVE == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                if event.key == pygame.K_ESCAPE:
                    closeGame()


def eatApple():
    global SnakeVelocity, SnakeHeight, ApplePresent, Score, SnakeLength
    SnakeVelocity += 0.2
    ApplePresent = False
    SnakeLength += 1
    Score = Score + 1

def applyEventListeners (keys):
        global LastMovement
        if keys[pygame.K_a]: LastMovement = "left"
        if keys[pygame.K_d]: LastMovement = "right"
        if keys[pygame.K_w]: LastMovement = "up"
        if keys[pygame.K_s]: LastMovement = "down"
        if keys[pygame.K_r]: restart()
        if keys[pygame.K_ESCAPE]: closeGame()
        if keys[pygame.K_F5]: gameOver() 

        if LastMovement == "left": goLeft()
        if LastMovement == "right": goRight()
        if LastMovement == "up": goUp()
        if LastMovement == "down": goDown()
        
        # Check for self-collision
        if hitSelf():
            gameOver() 

def drawScore():
    global Score, MainWindow, DefaultFontSize, Red
    font = pygame.font.Font(None, DefaultFontSize * 2)
    text = font.render(str(Score), True, Red)  
    text_position = text.get_rect(center=(MainWindowWidth // 2, MainWindowHeight // 2)) 
    font = pygame.font.Font(None, DefaultFontSize)
    MainWindow.blit(text, text_position) 

while Run: 
    pygame.time.delay(20)
    current_time = pygame.time.get_ticks()  # current time in ms

    keys = pygame.key.get_pressed()
    applyEventListeners(keys)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

    if ALIVE == False:
            gameOver()
    else: 
        pass
    
    # Check for space bar press and limit it to every 0.5 seconds (500 milliseconds)
    if keys[pygame.K_SPACE] and current_time - LastSpaceBarPress > 500:
        toggleBooster("speed")
        LastSpaceBarPress = current_time  # Update the last space bar press time

    # Add the new head position to the beginning of the SnakeSegments list
    SnakeSegments.insert(0, (SnakeXPosition, SnakeYPosition)) 

    # Check if the snake's length exceeds the desired length
    if len(SnakeSegments) > SnakeLength:
        # Remove the last segment if the snake's length is greater than the desired length
        SnakeSegments.pop()
    
    MainWindow.fill(MainColor)

    drawScore()
    drawSnake()
 
    # Check if the snake collides with the apple
    if (SnakeXPosition < AppleXPosition + AppleWidth and SnakeXPosition + SnakeWidth > AppleXPosition and
        SnakeYPosition < AppleYPosition + AppleHeight and SnakeYPosition + SnakeHeight > AppleYPosition):
        # Snake has eaten the apple, set ApplePresent to False to spawn a new one
        eatApple()

    # Draw a new apple if the previous one was eaten
    if not ApplePresent:
        AppleXPosition = random.randint(0, MainWindowWidth - AppleWidth)
        AppleYPosition = random.randint(0, MainWindowHeight - AppleHeight)
        ApplePresent = True

    drawApple()
    pygame.display.update()

pygame.quit()
