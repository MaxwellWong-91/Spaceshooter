import pygame
from pygame.locals import *
import os
import sys
import math
import random
from Player import Player
from Enemy import Enemy
from Bullet import Bullet
pygame.init()

HALF = 2

# used for window size
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

window = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
pygame.display.set_caption("Space Shooter")

# loads background and adjusts size
BACKGROUND_IMAGE = pygame.image.load(os.path.join(os.path.dirname("__file__"), "Images", "Background" , "game_background_4.png")).convert()
#BACKGROUND_IMAGE = pygame.transform.scale( BACKGROUND_IMAGE, ( SCREEN_WIDTH, SCREEN_HEIGHT ) )

MAP_CHANGE_SPEED = 4

CHAR_SIZE = 64
ENEMY_SIZE = 128

BULLET_SIZE = 30

# controls time
FPS = 30
clock = pygame.time.Clock()

X_OFFSET = 100

# used for win and lose message
FONT_SIZE = 64

# used for the play again button
BUTTON_TEXT_SIZE = 36
BUTTON_WIDTH = 215
BUTTON_HEIGHT = 65
BUTTON_X = SCREEN_WIDTH/HALF - 75
BUTTON_Y = SCREEN_HEIGHT/HALF\

user = Player( X_OFFSET, SCREEN_HEIGHT / HALF, CHAR_SIZE, CHAR_SIZE )
    
enemies = Enemy( SCREEN_WIDTH, SCREEN_HEIGHT / HALF, ENEMY_SIZE, ENEMY_SIZE, user, SCREEN_WIDTH, SCREEN_HEIGHT, 10 )

def mainLoop():
    # handles background music
    pygame.mixer.music.load("Background Music.mp3")
    pygame.mixer.music.play(-1)

    # used to make sure bullets don't fire too fast
    BULLET_DELAY = 500
    previousTime = pygame.time.get_ticks()

    # Gets x positon of background
    firstImageX = 0
    secondImageX = BACKGROUND_IMAGE.get_width()
    gameRun = True
    while gameRun:
        
        pygameEvents = pygame.event.get()

        for event in pygameEvents:
            # quits game
            if event.type == pygame.QUIT:
                gameRun = False
                pygame.quit()
    

        # constantly moves background
        firstImageX -= MAP_CHANGE_SPEED
        secondImageX -= MAP_CHANGE_SPEED
        if firstImageX < BACKGROUND_IMAGE.get_width() * -1:
            firstImageX = BACKGROUND_IMAGE.get_width()
        if secondImageX < BACKGROUND_IMAGE.get_width() * -1:
            secondImageX = BACKGROUND_IMAGE.get_width() 

        key = pygame.key.get_pressed()
        
        # handles moving space ship
        if ( key[ pygame.K_RIGHT ] or key[ pygame.K_LEFT ] or key[ pygame.K_UP ] or key[ pygame.K_DOWN ] ):
            user.setFlying( True )
            user.move( key, SCREEN_WIDTH, SCREEN_HEIGHT )
        else:   
            user.setFlying( False )
        
        # handles firing bullets 
        if key[ pygame.K_SPACE ]:
            currentTime = pygame.time.get_ticks()
            # fires bullet after half a second
            if currentTime - previousTime > BULLET_DELAY:
                previousTime = currentTime
                user.setBullet( BULLET_SIZE ) 

        for userBullet in user.getBullets():
            # check if bullet hit enemy
            if enemies.isHit( userBullet ):
                enemies.hit()
                user.getBullets().pop( user.getBullets().index( userBullet ) )
            # check out of bounds
            if userBullet.getHitBox()[0] + userBullet.getHitBox()[2] > SCREEN_WIDTH:
                user.getBullets().pop( user.getBullets().index( userBullet ) )
        
        for enemyBullet in enemies.getBullets():
            #check if bullet hit user
            if user.isHit( enemyBullet ):
                user.hit()
                enemies.getBullets().pop( enemies.getBullets().index( enemyBullet ) )
            # check out of bounds
            if enemyBullet.getHitBox()[0] < 0:
                enemies.getBullets().pop( enemies.getBullets().index( enemyBullet ) )
        
        clock.tick( FPS )
        
        drawWindow( firstImageX, secondImageX, pygameEvents )
    
                          
# puts all the stuff onto screen
def drawWindow( firstImageX, secondImageX, events ):
    window.blit( BACKGROUND_IMAGE, (firstImageX, 0) )
    window.blit( BACKGROUND_IMAGE, (secondImageX, 0) )
    # draws user and enemy if not dead
    if user.currentHealth != 0:
        user.draw( window )
    if enemies.currentHealth != 0:
        enemies.draw( window )
    
    # handles player or enemy dead
    if user.currentHealth == 0:
        drawButton( events )
        placeText("You Lose :(", (255, 255, 255), SCREEN_WIDTH/HALF - 120, SCREEN_HEIGHT/HALF - 100, FONT_SIZE)
        
    if enemies.currentHealth == 0:
        drawButton( events )
        placeText("You Win :)", (255, 255, 255), SCREEN_WIDTH/HALF - 120, SCREEN_HEIGHT/HALF - 100, FONT_SIZE)

    pygame.display.update()


# p uts text on the screen
def placeText( message, color, positionX, positionY, fontSize ):
    font = pygame.font.SysFont("comicsansms", fontSize)
    text = font.render(message, True, color)
    window.blit(text, (positionX, positionY))

# puts the play again button
def drawButton( events ):
    mouse = pygame.mouse

    # black outline of button
    pygame.draw.rect( window, (0,0,0), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 1 )

    # checks if mouse is hovering over button
    if ( BUTTON_X < mouse.get_pos()[0] < BUTTON_X + BUTTON_WIDTH and 
         BUTTON_Y < mouse.get_pos()[1] < BUTTON_Y + BUTTON_HEIGHT ):
       pygame.draw.rect( window, (255,0,0), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 0)

       # if mouse is clicked restart game
       for event in events:
            if ( event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 ):
                restartGame()
    else:
       pygame.draw.rect( window, (200,0,0), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 0)

    placeText("Play Again?", (255, 255, 255), SCREEN_WIDTH/HALF - 60, SCREEN_HEIGHT/HALF, BUTTON_TEXT_SIZE)

# restarts the game
def restartGame():
    global user
    user = Player( X_OFFSET, SCREEN_HEIGHT / HALF, CHAR_SIZE, CHAR_SIZE )
    global enemies 
    enemies = Enemy( SCREEN_WIDTH, SCREEN_HEIGHT / HALF, ENEMY_SIZE, ENEMY_SIZE, user, SCREEN_WIDTH, SCREEN_HEIGHT, 10 )
    

if __name__.endswith("__main__"):
    mainLoop()