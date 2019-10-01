import pygame
import os 

class Bullet( object ):
    allyBullet = pygame.image.load( os.path.join( os.path.dirname("__file__"), "Images", "Blue", "bullet_copy.png" ) ) 
    enemyBullet = pygame.image.load( os.path.join( os.path.dirname("__file__"), "Images", "Red", "bullet_red.png" ) ) 
    PLAYER_BULLET_X_OFFSET = 10
    PLAYER_BULLET_Y_OFFSET = 10
    PLAYER_BULLET_WIDTH_OFFSET = 15
    PLAYER_BULLET_HEIGHT_OFFSET = 20
    ENEMY_BULLET_X_OFFSET = 15
    ENEMY_BULLET_Y_OFFSET = 17
    ENEMY_BULLET_WIDTH_OFFSET = 25
    ENEMY_BULLET_HEIGHT_OFFSET = 35
    def __init__( self, positionX, positionY, width, height, isPlayer ):
        self.setPositionX( positionX )
        self.setPositionY( positionY )
        self.setWidth( width )
        self.setHeight( height )
        self.isPlayer = isPlayer
        self.setSpeed()

    def getPositionX( self ):
        return self.positionX
    
    def setPositionX( self, positionX ):
        self.positionX = positionX
    
    def getPositionY( self ):
        return self.positionY
    
    def setPositionY( self, positionY ):
        self.positionY = positionY

    def getWidth( self ):
        return self.width 

    def setWidth( self, width ):
        self.width = width 

    def getHeight( self ):
        return self.height 

    def setHeight( self, height ):
        self.height = height 

    def getSpeed( self ):
        return self.speed

    def setSpeed( self ):
        # change here for player bullet speed
        if self.isPlayer:
            self.speed = 15 
        # change here for enemy bullet speed
        else:
            self.speed = 15

    # the coordinates of the hitbox
    # returns x, y, width and height of hitbx
    def getHitBox( self ):
        if self.isPlayer:
            
            return ( self.getPositionX() + self.PLAYER_BULLET_X_OFFSET, 
                     self.getPositionY() + self.PLAYER_BULLET_Y_OFFSET, 
                     self.getWidth() - self.PLAYER_BULLET_WIDTH_OFFSET, 
                     self.getHeight() - self.PLAYER_BULLET_HEIGHT_OFFSET )
        else:
            return ( self.getPositionX() + self.ENEMY_BULLET_X_OFFSET, 
                     self.getPositionY() + self.ENEMY_BULLET_Y_OFFSET, 
                     self.getWidth() - self.ENEMY_BULLET_WIDTH_OFFSET, 
                     self.getHeight() - self.ENEMY_BULLET_HEIGHT_OFFSET )

    # puts bullet on screen
    def draw( self, window ):
        self.move()
        if self.isPlayer:
            window.blit( pygame.transform.scale( self.allyBullet, ( self.getWidth(), self.getHeight() ) ), ( self.getPositionX(), self.getPositionY() ))
        else:
            window.blit( pygame.transform.scale( self.enemyBullet, ( self.getWidth(), self.getHeight() ) ), ( self.getPositionX(), self.getPositionY() ))
        # draws hit box (used for testing)
        #pygame.draw.rect( window, (255,0,0), self.getHitBox(), 2)
        
    def move( self ):
        if self.isPlayer:
            self.setPositionX( self.getPositionX() + self.getSpeed() )
        else: 
            self.setPositionX( self.getPositionX() - self.getSpeed() )   

    