import pygame

class Button( object ):
    def Button(self, positionX, positionY, width, height, buttonColor, textColor, text, textSize):
        self.setPositionX( positionX )
        self.setPositionY( positionY )
        self.setWidth( width )
        self.setHeight( height )
        self.buttonColor = buttonColor
        self.textColor = textColor
        self.text = text
        self.textSize = textSize

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

    def getText( self ):
        return self.text
    
    def getTextColor( self ):
        return self.textColor

    def getButtonColor( self ):
        return self.buttonColor

    def getTextSize( self ):
        return self.textSize

    # draws the button onto the screen
    def drawButton( self, window ):
        pygame.draw.rect( window, self.getButtonColor(), (self.getPositionX(), self.getPositionY(), self.getWidth(), self.getHeight()), 0 )

        self.placeText( window )


    def placeText( self, window ):
        font = pygame.font.SysFont("comicsansms", self.getTextSize())
        text = font.render(self.getText(), True, self.getTextColor())
        window.blit(text, (SCREEN_WIDTH/HALF - 100, SCREEN_HEIGHT/HALF - 50))