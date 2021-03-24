import random

from termcolor import colored


class Block():
    def __init__(self, type):
        self.type = type
        self.color = 'white'
        self.chardmg = 'X'
        self.char = ''
        self.health = 2
        self.x = 0
        self.y = 0
        self.id = random.randint(0,999999)
        self.getChar()
    def getInfo(self):
        return {'id':self.id,'x':self.x,'y':self.y,'color':self.color,'char':self.char,'type':self.type,'health':self.health}
    def getChar(self):
        if(self.health == 2):
            char = colored(self.chardmg, self.color, 'on_' + self.color)
        else:
            char = colored(self.chardmg, 'grey', 'on_' + self.color)
        self.char = char
class Bullet():
    def __init__(self):
        self.range = 10
        self.x = 0
        self.y = 0
        self.id = random.randint(0,9999999)
        self.xadd = 0
        self.yadd = 0
    def getInfo(self):
        return {'id':self.id,'x':self.x,'y':self.y,'range':self.range,'xadd':self.xadd,'yadd':self.yadd}