from enum import Enum

from termcolor2 import colored
class Blocks(Enum):
    GRASS = colored('x', 'green','on_green')
class screen():
    def __init__(self, xsize, ysize,bgpix=Blocks.GRASS.value):
        self.screenstr = ""
        self.screenlist = []
        for i in range(ysize):
            list02 = []
            for x in range(xsize):
                list02.append(bgpix)
            self.screenlist.append(list02)
            self.screenstr += "\n"
        self.size = [xsize, ysize]
        self.bgpix = bgpix
    def changePx(self,color,x,y):
        self.screenlist[y][x] = color
        self.screenstr = ""
        for i in self.screenlist:
            for j in i:
                self.screenstr+=j
            self.screenstr += "\n"
