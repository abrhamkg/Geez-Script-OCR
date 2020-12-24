# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 16:16:03 2019

@author: abrih
"""
from itertools import chain, combinations
import pygame
from pygame.locals import *
import sys
import os

GREEN     = (  0, 255,   0)
BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BLUE      = (  0,   0, 255)
RED       = (255,   0,   0)

BGCOLOR = WHITE
WINDOWHEIGHT = 900
WINDOWWIDTH = 1400
FPS = 30
def getCharList():
    """
        Returns the list of unicode values of all Ethiopic characters without the unassigned values
    """
    unassigned = [0x1249, 0x124E, 0x124F, 0x1257, 0x1259, 0x125E, 0x125f, 0x1289, 0x128E, 0x128F, 0x12B1, 0x12B6, 0x12B7, 0x12BF, 0x12C1, 0x12C6, 0x12C7, 0x12D7, 0x1311, 0x1316, 0x1317, 0x135B, 0x135C]
    start = 0x1200
    end = 0x1356
    l = []
    for char in range(start, end):
        if char in unassigned:
            continue
        l.append(char)
    return l
def powerset(iterable,n):
    """ 
        Returns all subsets of length 1, ..., n of the iterable
    """
    xs = list(iterable)
    return chain.from_iterable(combinations(xs,n) for n in range(1, n+1)) #len(xs+1)

def main(font, size):
    global FPSCLOCK, DISPSURF
    pygame.init()
    # Position the pygame window at exactly the following coordinates
    x = 100
    y = 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

    FPSCLOCK = pygame.time.Clock()
    DISPSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    #print DISPSURF.get_rect()
    #fil = open('training.txt','r',encoding='utf8')
    #txt = fil.readlines()
    #print lines
    clear()
    os.chdir("training_chars")
    count = 1
    all_chars = getCharList()
    all_combinations = powerset(all_chars, 2)
    while True:
        start = (count - 1)*16
        #lines = txt[start:min(start+16,len(txt))]
        clear()
        xc = 15
        yc = 15
        x0,y0 = xc,yc
        wMax = 0
        char_combn = None
        try:
            char_combn = next(all_combinations)
        except StopIteration:
            break
        chars = [chr(c).encode("utf-8").decode("utf-8") for c in char_combn]
        print(chars)
        fLine = "".join(chars)
        print(fLine)
        textArea = displayAmharicText(fLine,font, size, (xc,yc),BLACK)
        #print(type(fLine))
        if textArea.width > wMax:
            wMax = textArea.width
        yc += textArea.height + size
        #break
        for event in pygame.event.get():
            if event.type == QUIT:
                fil.close()
                terminate()
        pygame.display.update()
        margin = 10
        letter = DISPSURF.subsurface(x0 -margin, y0 -margin,wMax + 2*margin,yc - y0)
        name = 'image_%d.png'%count
        pygame.image.save(letter, name)
        pygame.time.wait(1)
        #terminate()
        count += 1
        FPSCLOCK.tick()
def terminate():
    pygame.quit()
    sys.exit(1)

def displayAmharicText(text, font, size, posTuple, color = BLUE):
    myfont = pygame.font.SysFont(font, size)
    # render text
    label = myfont.render(text, 1, color)
    return DISPSURF.blit(label, posTuple)
def clear():
    DISPSURF.fill(BGCOLOR)

if __name__ == '__main__':
    print("here")
    a = [1,2,3]
    #print(powerset(a))
    fonts = ["nyala"]
    sizes = range(16,17)
    maxx = []
    maxy = []
    for font in fonts:
        for size in sizes:
            mx, my = main(font, size)
    terminate()