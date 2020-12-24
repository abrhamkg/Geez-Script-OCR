import pygame
from pygame.locals import *
import sys
import os
#import pyscreenshot as ImageGrab
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
unassigned = [0x1249, 0x124E, 0x124F, 0x1257, 0x1259, 0x125E, 0x125f, 0x1289, 0x128E, 0x128F, 0x12B1, 0x12B6, 0x12B7, 0x12BF, 0x12C1, 0x12C6, 0x12C7, 0x12D7, 0x1311, 0x1316, 0x1317, 0x135B, 0x135C]
sys.getfilesystemencoding = lambda: 'UTF-8'
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
    fil = open('training.txt','r',encoding='utf8')
    txt = fil.readlines()
    #print lines
    clear()
    os.chdir("training")
    count = 1
    while True:
        start = (count - 1)*16
        lines = txt[start:min(start+16,len(txt))]
        clear()
        xc = 15
        yc = 15
        x0,y0 = xc,yc
        wMax = 0
        lab = open('label_%d.txt'%count,'w',encoding='utf8')
        for line in lines:
            #print line
            #print "s",line
            line = line.rstrip("\n")#.decode('UTF-8')
            #print line
            fLine = line
            for char in line:
                #print ord(char), char,
                if ord(char) > 4950:
                    fLine = fLine.replace(char,"")
                    #print "here",
                #print
            #print line
            flist = list(fLine)
            fLine = "".join(flist)
            textArea = displayAmharicText(fLine,font, size, (xc,yc),BLACK)
            #print(type(fLine))
            lab.write(fLine+"\n")
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
        lab.close()
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
    fonts = ["nyala"]
    sizes = range(16,17)
    maxx = []
    maxy = []
    for font in fonts:
        for size in sizes:
            mx, my = main(font, size)
    print(max(maxx), max(maxy))
    terminate()
