import pygame
import os

class Asteroid( object ):
    def __init__( self, positionX, positionY, width, height ):
        self.setPositionX( positionX )
        self.setPositionY( positionY )
        self.setWidth( width )
        self.setHeight( height )

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