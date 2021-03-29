# by Timothy Downs, inputbox written for my map editor
# Modified by Ari Madian for python 3.x and bad word filtering

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# For bad word filtering, just modify the bad_words_file path to get
#   your text file of choice.
#
# Only near the center of the screen is blitted to

import pygame
import pygame.font
import pygame.event
import pygame.draw
from pygame.locals import *

from settings import Settings

def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    setting = Settings()
    fontobject = pygame.font.SysFont("Comic Sans MS", 18)
    pygame.draw.rect(screen, (0, 0, 0),
                     (0,
                      (setting.height - 165) - 10,
                      401, 101), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     (0,
                      (setting.height - 165) - 10,
                      402, 142), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    (0,
                     (setting.height - 165) - 10))
    pygame.display.flip()


def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + "".join(current_string))
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            return current_string
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + "".join(current_string))
    return "".join(current_string)
def say(screen,stringtosay,secs,whilenotclicked=False):
    tick = 0
    setting = Settings()
    if(whilenotclicked):
        while True:
            display_box(screen, stringtosay)
            if(not get_key() == None):
                break
        return
    while tick < secs*setting.fps:
        display_box(screen, stringtosay)
        tick+=1


def main():
    screen = pygame.display.set_mode((320, 240))


if __name__ == '__main__': main()