import pygame
import os
from Bullet import Bullet

class Player( object ):
    flyingImage = []
    for i in range(1, 9):
        flyingImage.append( pygame.image.load( os.path.join( os.path.dirname("__file__"), "Images", "Blue", "Animation", "B{}.png".format(i) )))
    idle = flyingImage[6]
    SPEED = 5
    HALF = 2

    BULLET_Y_OFFSET = -15

    HITBOX1_X_OFFSET = 10
    HITBOX1_Y_OFFSET = 2
    HITBOX1_WIDTH_OFFSET = 46
    HITBOX1_HEIGHT_OFFSET = 7

    HITBOX2_X_OFFSET = 8
    HITBOX2_Y_OFFSET = 6
    HITBOX2_WIDTH_OFFSET = 43
    HITBOX2_HEIGHT_OFFSET = 55

    # used for health bar
    HEALTH_BAR_WIDTH = 100
    HEALTH_BAR_HEIGHT = 8
    HP_Y_OFFSET = 10
    HEALTH = 3

    isAlive = True

    def __init__( self, positionX, positionY, width, height ):
        self.setPositionX( positionX )
        self.setPositionY( positionY )
        self.setWidth( width )
        self.setHeight( height )
        self.isFlying = False
        self.flyingImageIndex = 0
        self.bullets = []
        self.currentHealth = self.HEALTH

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

    def setFlying( self, toFly ):
        self.isFlying = toFly

    def getSpeed( self ):
        return self.SPEED

    def getBullets( self ):
        return self.bullets

    def setBullet( self, bulletSize ):
        self.getBullets().append( Bullet( self.getPositionX() + ( self.getWidth() // self.HALF ), self.getPositionY() + ( self.getHeight() // self.HALF + self.BULLET_Y_OFFSET ), bulletSize, bulletSize, True ) )
    
    # puts space ship onto screen
    def draw( self, window ):
        if self.isFlying:
            window.blit( pygame.transform.scale( self.flyingImage[ self.flyingImageIndex ], ( self.getWidth(), self.getHeight() ) ), ( self.getPositionX(), self.getPositionY() ) ) 
        else:
            window.blit( pygame.transform.scale( self.idle, ( self.getWidth(), self.getHeight() ) ), ( self.getPositionX(), self.getPositionY() ))

        #for bullet in self.bullets:
        #    bullet.draw( window )

        for bullet in self.getBullets():
            bullet.draw( window )

        # draws hit box (used for testing)
        #pygame.draw.rect( window, (255,0,0), self.getHitBox1(), 2)
        #pygame.draw.rect( window, (255,0,0), self.getHitBox2(), 2)

        # draws the healthbar
        pygame.draw.rect( window, (255, 0, 0), self.getHealthBar1() )
        if self.currentHealth > 0 :
            pygame.draw.rect( window, (0, 255, 0), self.getHealthBar2() )
        pygame.draw.rect( window, (64, 64, 64), self.getHealthBar1(), 2 )

    # coordinates used for hitbox
    # hitbox for body
    # returns x, y, width, height of hitbox
    def getHitBox1( self ):
        return ( self.getPositionX() - self.HITBOX1_X_OFFSET + self.getWidth() // self.HALF, 
                 self.getPositionY() + self.HITBOX1_Y_OFFSET, 
                 self.getWidth() - self.HITBOX1_WIDTH_OFFSET, 
                 self.getHeight() - self.HITBOX1_HEIGHT_OFFSET )

    # hitbox for head
    # returns x, y, width, height of hitbox
    def getHitBox2( self ):
        return ( self.getPositionX() + self.HITBOX2_X_OFFSET + self.getWidth() // self.HALF, 
                 self.getPositionY() - self.HITBOX2_Y_OFFSET + self.getHeight() // self.HALF, 
                 self.getWidth() - self.HITBOX2_WIDTH_OFFSET, 
                 self.getHeight() - self.HITBOX2_HEIGHT_OFFSET )

    # handles plane movements
    def move( self, key, screenWidth, screenHeight ):
        #print ("alive")
        if key[ pygame.K_RIGHT ] and self.getPositionX() < screenWidth - self.getWidth() :
            self.setPositionX( self.getPositionX() + self.getSpeed() )
            self.flyingImageIndex += 1
        elif key[ pygame.K_LEFT ] and self.getPositionX() > self.getSpeed():
            self.setPositionX( self.getPositionX() - self.getSpeed() )
            self.flyingImageIndex += 1
        if key[ pygame.K_UP ] and self.getPositionY() > 0:
            self.setPositionY( self.getPositionY() - self.getSpeed() )
            self.flyingImageIndex += 1
        elif key[ pygame.K_DOWN ] and self.getPositionY() < screenHeight - self.getHeight():
            self.setPositionY( self.getPositionY() + self.getSpeed() )
            self.flyingImageIndex += 1

        # current image index to display
        self.flyingImageIndex = self.flyingImageIndex % ( len( self.flyingImage ) - 1 )

    # checks if something is hitting 
    def isHit( self, projectile ):

        return ( self.isAlive and
               ( self.isPointInHitBox( (projectile.getHitBox()[0], projectile.getHitBox()[1]), 
                 self.getHitBox1() ) or 
                 self.isPointInHitBox( (projectile.getHitBox()[0] , projectile.getHitBox()[1] + projectile.getHitBox()[3]), 
                 self.getHitBox1() ) or 
                 self.isPointInHitBox( (projectile.getHitBox()[0] + projectile.getHitBox()[2], projectile.getHitBox()[1]), 
                 self.getHitBox1() ) or 
                 self.isPointInHitBox( (projectile.getHitBox()[0] + projectile.getHitBox()[2], projectile.getHitBox()[1] + projectile.getHitBox()[3]), 
                 self.getHitBox1() ) or
                 self.isPointInHitBox( (projectile.getHitBox()[0], projectile.getHitBox()[1]), 
                 self.getHitBox2() ) or 
                 self.isPointInHitBox( (projectile.getHitBox()[0] , projectile.getHitBox()[1] + projectile.getHitBox()[3]), 
                 self.getHitBox2() ) or 
                 self.isPointInHitBox( (projectile.getHitBox()[0] + projectile.getHitBox()[2], projectile.getHitBox()[1]), 
                 self.getHitBox2() ) or 
                 self.isPointInHitBox( (projectile.getHitBox()[0] + projectile.getHitBox()[2], projectile.getHitBox()[1] + projectile.getHitBox()[3]), 
                 self.getHitBox2() ) ) )

    def isPointInHitBox( self, point, hitBox ):
        # point[0] should be x-coordinate and point[1] should be y coordinate
        return ( hitBox[0] < point[0] < hitBox[0] + hitBox[2] and 
                 hitBox[1] < point[1] < hitBox[1] + hitBox[3] )

    
    # handles spaceship getting hit
    def hit( self ):
        if self.currentHealth > 0:
            self.currentHealth -= 1

        if self.currentHealth == 0:
            self.isAlive = False

    # used to get the health bar of the space ship
    # red bar
    def getHealthBar1( self ):
        return ( self.getPositionX(), 
                 self.getPositionY() - self.HP_Y_OFFSET, 
                 self.HEALTH_BAR_WIDTH, self.HEALTH_BAR_HEIGHT )
    
    # green bar
    def getHealthBar2( self ):
        return ( self.getPositionX(), 
                 self.getPositionY() - self.HP_Y_OFFSET, 
                 self.HEALTH_BAR_WIDTH  - ( (self.HEALTH_BAR_WIDTH / self.HEALTH ) *  
                                            ( self.HEALTH - self.currentHealth ) ), 
                 self.HEALTH_BAR_HEIGHT )