import pygame
import os
from Bullet import Bullet

class Enemy( object ):
    flyingImage = []

    # images to display for enemy space ship
    for i in range(1, 6):
        flyingImage.append( pygame.image.load( os.path.join( os.path.dirname("__file__"), "Images", "Red", "small_ship_animation", "R{}.png".format(i) )))
    
    SCREEN_OFFSET = 200
    
    FOLLOWING_DISTANCE = 150
    HALF = 2
    BULLET_Y_OFFSET = -30

    #bullets = []

    BULLET_SIZE = 50

    # how often to fire bullets
    FIRE_RATE = 15

    # used for vertex coordinates
    VERTEX_X_OFFSET = 35
    VERTEX_Y_OFFSET = 13

    # used for health bar
    HEALTH_BAR_WIDTH = 100
    HEALTH_BAR_HEIGHT = 8
    HEALTH = 10

    isAlive = True

    def __init__( self, positionX, positionY, width, height, player, screenWidth, screenHeight, speed ):
        self.setPositionX( positionX )
        self.setPositionY( positionY )
        self.setWidth( width )
        self.setHeight( height )
        self.flyingImageIndex = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.speed = speed
        self.setIsUp( True )
        self.player = player
        self.fireCount = 0
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
        return self.speed

    # used to determine current direction traveling of ship
    def getIsUp( self ):
        return self.isUp

    def setIsUp( self, isUp ):
        self.isUp = isUp

    # used to get the health bar of the space ship
    # red bar
    def getHealthBar1( self ):
        return ( self.getPositionX(), 
                 self.getPositionY(), 
                 self.HEALTH_BAR_WIDTH, self.HEALTH_BAR_HEIGHT )
    
    # green bar
    def getHealthBar2( self ):
        return ( self.getPositionX(), 
                 self.getPositionY(), 
                 self.HEALTH_BAR_WIDTH  - ( (self.HEALTH_BAR_WIDTH / self.HEALTH ) *  
                                            ( self.HEALTH - self.currentHealth ) ), 
                 self.HEALTH_BAR_HEIGHT )

    # used to determine vertex used for hit box
    # left point
    def getVertex1( self ):
        return ( self.getPositionX(), self.getPositionY() + self.getHeight() // self.HALF )
    
    # top right point
    def getVertex2( self ):
        return ( self.getPositionX() + self.getWidth() - self.VERTEX_X_OFFSET, 
                 self.getPositionY() + self.VERTEX_Y_OFFSET )

    # bottom left point
    def getVertex3( self ):
        return ( self.getPositionX() + self.getWidth() - self.VERTEX_X_OFFSET, 
                 self.getPositionY() + self.getHeight() - self.VERTEX_Y_OFFSET )

    # coordinates used for hitbox
    def getHitBox( self ):
        return ( self.getVertex1(), self.getVertex2(), self.getVertex3() )

    def getBullets( self ):
        return self.bullets

    def setBullet( self, bulletSize ):
        self.getBullets().append( Bullet( self.getPositionX() + ( self.getWidth() // self.HALF ), self.getPositionY() + ( self.getHeight() // self.HALF + self.BULLET_Y_OFFSET ), bulletSize, bulletSize, False ) )

    # draws all the objects onto the screen
    def draw( self, window ):
        self.move()
        
        # draws the image of the spaceship onto the screen
        window.blit( pygame.transform.scale( self.flyingImage[ self.flyingImageIndex ], ( self.getWidth(), self.getHeight() ) ), ( self.getPositionX(), self.getPositionY() ) ) 

        # draws the bullets 
        for bullet in self.getBullets():
            bullet.draw( window )

        #pygame.draw.polygon( window, (255, 0, 0), self.getHitBox(), 5)
        # draws the healthbar
        pygame.draw.rect( window, (255, 0, 0), self.getHealthBar1() )
        if self.currentHealth > 0 :
            pygame.draw.rect( window, (0, 255, 0), self.getHealthBar2() )
        pygame.draw.rect( window, (64, 64, 64), self.getHealthBar1(), 2 )
        
        

    # handles all the movements and actions in the spaceship
    def move( self ):
        
        # moves x direction
        if self.getPositionX() > self.screenWidth - self.SCREEN_OFFSET:
            self.setPositionX( self.getPositionX() - self.getSpeed() )
        
        # moves y direction
        if self.getIsUp():
            #self.setPositionY(self.getPositionY())
            self.setPositionY( self.getPositionY() - self.getSpeed() )
        else:
            #self.setPositionY(self.getPositionY())
            self.setPositionY( self.getPositionY() + self.getSpeed() )
        # changes direction when reaches end
        if self.getPositionY() < 0 or self.getPositionY() < self.player.getPositionY() - self.FOLLOWING_DISTANCE:
            self.setIsUp( False )
        if ( ( self.getPositionY() > self.screenHeight - self.getHeight() ) or 
           ( self.getPositionY() > self.player.getPositionY() + self.FOLLOWING_DISTANCE ) ) :
            self.setIsUp( True )
        
        self.flyingImageIndex += 1

        # current image index to display
        self.flyingImageIndex = self.flyingImageIndex % ( len( self.flyingImage ) - 1 )

        # makes bullets shoot out after timed delay
        self.fireCount += 1

        if self.fireCount % self.FIRE_RATE == 0:
            self.setBullet( self.BULLET_SIZE )
        
    def isHit( self, projectile ):
        # area of hitbox
        hitboxArea = self.triangleArea( self.getVertex1()[0], self.getVertex1()[1], 
                                        self.getVertex2()[0], self.getVertex2()[1],
                                        self.getVertex3()[0], self.getVertex3()[1] ) 
        
        # get sum of area of triangle formed from top left corner 
        topLeftTriangleSum = self.sumTriangleArea( projectile.getHitBox()[0], 
                                                   projectile.getHitBox()[1] )
        
        # get sum of area of triangle formed from top right corner
        topRightTriangleSum = self.sumTriangleArea( projectile.getHitBox()[0] + projectile.getHitBox()[2], 
                                                    projectile.getHitBox()[1] )
        
        # get sum of area of triangle formed from bottom left corner
        botLeftTriangleSum = self.sumTriangleArea( projectile.getHitBox()[0], 
                                                    projectile.getHitBox()[1] +projectile.getHitBox()[3])

        # get sum of area of triangle formed from bottom right corner
        botRightTriangleSum = self.sumTriangleArea( projectile.getHitBox()[0] + projectile.getHitBox()[2], 
                                                    projectile.getHitBox()[1] + projectile.getHitBox()[3])
        
        return ( self.isAlive and ( hitboxArea == topLeftTriangleSum or hitboxArea == topRightTriangleSum or 
                                    hitboxArea == botLeftTriangleSum or hitboxArea == botRightTriangleSum ) )


    # calculates area of triangle
    def triangleArea( self, x1, y1, x2, y2, x3, y3 ):
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

    # gets sum of area of triangles made from point and hitbox
    def sumTriangleArea( self, x, y ):
        area1 = self.triangleArea( x, y, 
                                   self.getVertex2()[0], self.getVertex2()[1],
                                   self.getVertex3()[0], self.getVertex3()[1] )

        area2 = self.triangleArea( self.getVertex1()[0], self.getVertex1()[1],
                                   x, y, 
                                   self.getVertex3()[0], self.getVertex3()[1] )

        area3 = self.triangleArea( self.getVertex1()[0], self.getVertex1()[1],
                                   self.getVertex2()[0], self.getVertex2()[1],
                                   x, y )

        return (area1 + area2 + area3)

    # handles spaceship getting hit
    def hit( self ):
        if self.currentHealth > 0:
            self.currentHealth -= 1

        if self.currentHealth == 0:
            self.isAlive = False
        
