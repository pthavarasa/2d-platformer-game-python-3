import pygame

class Button():
    def __init__(self,x,y,width,height,text_color,background_color,text, font, DS):
        self.rect=pygame.Rect(x,y,width,height)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
        self.text_font = font
        self.text_color=text_color
        self.background_color=background_color
        self.DS = DS
        self.angle=0
        self.button_text_color=background_color

    def collide_color(self):
        self.button_text_color= self.background_color
        self.button_background_color= self.text_color

    def default_color(self):
        self.button_text_color = self.text_color
        self.button_background_color= self.background_color

    def check(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def drawTextcenter(self):
        textobj = self.text_font.render(self.text, True, self.button_text_color)
        textrect = textobj.get_rect(center=(self.x+self.width/2 , self.y+self.height/2))
        self.DS.blit(textobj, textrect)

    def draw(self):
        #pygame.draw.rect(self.DS, self.button_background_color,(self.rect),0)
        self.drawTextcenter()
