import pygame
from settings import Settings


class Character:
    def __init__(self, screen, x_pos, y_pos):
        self.settings = Settings()
        self.screen = screen
        self.image = pygame.image.load('images/character.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.centery
        self.x = x_pos
        self.speed = 10
        self.y = y_pos
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.id = 0
        self.move = False
        self.setblockvar = False
        self.remblockvar = False
        self.setblockpos = (0,0)
        self.remblockpos = (0,0)
    def sendMoveData(self):
        self.move = False
        return str({'event':'move','x_pos':self.x,'y_pos':self.y,'id':self.id})
    def setBlock(self):
        self.setblockvar = False
        return str({'blockplace': True, 'x_pos': self.setblockpos[0], 'y_pos': self.setblockpos[1]})
    def remBlock(self):
        self.remblockvar = False
        return str({'blockremove': True, 'x_pos': self.remblockpos[0], 'y_pos': self.remblockpos[1]})
    def sendMyData(self):
        return str({'x_pos': self.x, 'y_pos': self.y})
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        self.rect.x = self.rect.x+((self.x-self.rect.x)/self.speed)
        if ((self.x - self.rect.x) / self.speed < 1 and(self.x - self.rect.x) / self.speed > 0):
            self.rect.x = self.x
        if ((self.x - self.rect.x) / self.speed > -1 and(self.x - self.rect.x) / self.speed < 0):
            self.rect.x = self.x
        self.rect.y = self.rect.y+((self.y-self.rect.y)/self.speed)
        if ((self.y - self.rect.y) / self.speed > -1 and(self.y - self.rect.y) / self.speed < 0):
            self.rect.y = self.y
        if ((self.y - self.rect.y) / self.speed < 1 and(self.y - self.rect.y) / self.speed > 0):
            self.rect.y = self.y
