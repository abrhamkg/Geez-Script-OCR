import pygame
from pygame.locals import *
import sys
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

MODEL_DIR = config['DEFAULT']['MODEL_DIR']
DATA_DIR = config['DEFAULT']['DATA_DIR']

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREEN = (0, 155,   0)
DARKGRAY = (40, 40, 40)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

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
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{}, {}".format(x,y)

    FPSCLOCK = pygame.time.Clock()
    DISPSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # Get the content to convert to image
    with open(os.path.join(DATA_DIR, 'text/training.txt'), 'r', encoding='utf8') as trainingfile:
        txt = trainingfile.readlines()

    # Clear the screen
    clear()

    img_train_fldr = os.path.join(DATA_DIR, "img/train")
    os.chdir(img_train_fldr)
    count = 1
    lines_per_image = 16
    while True:
        start = (count - 1) * lines_per_image
        end = min(start + lines_per_image, len(txt))
        lines = txt[start:end]

        clear()
        xc = 15
        yc = 15
        x0, y0 = xc,yc

        wMax = 0
        lab = open('label_{}.txt'.format(count), 'w', encoding='utf8')

        for line in lines:
            line = line.rstrip("\n")#.decode('UTF-8')

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
