import pygame, sys
from pygame.locals import *
import random
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()

point = 0
font1 = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 40)
FPS = 10
fpsClock = pygame.time.Clock()
width = 600
height = 800
mainSurface = pygame.display.set_mode((width, height), 0, 32)
mainWindow = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('Космический шериф')
cell = 50
TEXTCOLOR = (255, 255, 255)
buttoncol1 = (0, 255, 0)
buttoncol2 = (0, 0, 255)
buttoncol3 = (255, 0, 0)

background = pygame.image.load('Image/backGround.png')
background2 = pygame.image.load('Image/background.jpg')
background3 = pygame.image.load('Image/background2.jpg')
background4 = pygame.image.load('Image/background3.jpg')
spriteb = pygame.image.load('Image/evil.png')
sprite = pygame.image.load('Image/character.png')

gameOverSound = pygame.mixer.Sound('Sound/zvuki-quotkonets-igryiquot-game-over-sounds-30249.ogg')

speed = 5
con = False
direction = False
window = True
lvl = None
first = True
back = False


def move_villain(spritebx, min, max):
    global back
    if spritebx <= max and not back:
        spritebx += speed
        if spritebx >= max:
            back = True
    elif spritebx >= min:
        spritebx -= speed
        if spritebx <= min:
            back = False
    return spritebx


def new_pos(lvl, point):
    spritebx = random.randint(0, width - cell)
    spriteby = random.randint(100, height - cell)
    if lvl == 3:
        min = random.randint(0, width - 300)
        max = min + 300
    point += 1
    return spritebx, spriteby, point, min, max


def re(FPS, speed):
    spritey = 0
    if FPS < 120:
        FPS += 5
    if speed < 20:
        speed += 1
    con = False
    return spritey, con, FPS


def over():
    b = pygame.image.load('Image/MainBackground.png')
    mainSurface.blit(b, (0, 0))
    if point <= 1:
        drawText('Уволен', font2, mainSurface, 220, 350)
    elif point <= 3:
        drawText('Ты старпался', font2, mainSurface, 210, 350)
    elif point <= 5:
        drawText('А ты хорош,', font2, mainSurface, 200, 350)
        drawText('на меня похож', font2, mainSurface, 190, 400)
    elif point <= 10:
        drawText('Премия?', font2, mainSurface, 230, 350)
    elif point <= 20:
        drawText('Работник года', font2, mainSurface, 200, 350)
    elif point <= 30:
        drawText('Работник столетия', font2, mainSurface, 180, 350)
    elif point <= 40:
        drawText('БОГОПОДОБИЕ', font2, mainSurface, 200, 360)
    elif point <= 50:
        drawText('ТЫ УЖЕ ПРЕВОСХОДИШЬ БОГОВ!!!', font2, mainSurface, 100, 350)
        drawText('КОГДА ЭТО УЖЕ ЗАКОНЧИТСЯ?!?!', font2, mainSurface, 100, 400)
    gameOverSound.play()


def get_click(q):
    pos = q
    x = pos[0]
    y = pos[1]
    x1, y1 = x // cell, y // cell
    if x1 < 0 or width < x1:
        print('None')
    else:
        coord = x, y
        print(coord)
        return coord


def move(direction, spritex, spritey):
    spritey += 10
    if direction:
        if direction == K_LEFT and spritex != 0:
            spritex -= 10
        elif direction == K_RIGHT and spritex != width - 50:
            spritex += 10
    return spritex, spritey


def main_window(FPS, point):
    global window
    while window:
        mainWindow.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if get_click(event.pos):
                    window = False
            if not window:
                level(FPS, point)
        pygame.display.update()


def level(FPS, point):
    while True:
        drawText('1 - лёгкий уровень', font1, mainSurface, 10, 10)
        drawText('2 - средний уровень', font1, mainSurface, 10, 35)
        drawText('3 - сложный уровень', font1, mainSurface, 10, 60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_1:
                game(FPS, 1, point)
            elif event.type == KEYDOWN and event.key == K_2:
                game(FPS, 2, point)
            elif event.type == KEYDOWN and event.key == K_3:
                game(FPS, 3, point)
        pygame.display.update()


def game(FPS, lvl, point):
    global direction
    spritex = width / 2
    spritey = 0
    spritebx = random.randint(0, width - cell)
    spriteby = random.randint(100, height - cell)
    min = random.randint(0, width - 300)
    max = min + 300
    while True:
        fpsClock.tick(FPS)
        if point <= 10:
            mainSurface.blit(background4, (0, 0))
        elif point <= 30:
            mainSurface.blit(background3, (0, 0))
        elif point <= 50:
            mainSurface.blit(background2, (0, 0))
        elif point <= 60:
            mainSurface.blit(background, (0, 0))
        mainSurface.blit(sprite, (spritex, spritey))
        mainSurface.blit(spriteb, (spritebx, spriteby))
        if lvl == 3:
            spritebx= move_villain(spritebx, min, max)
        drawText(str(point), font2, mainSurface, 10, 10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                direction = event.key
            if event.type == KEYUP:
                direction = False

        if spritey <= height:
            spritex, spritey = move(direction, spritex, spritey)
        else:
            if con:
                spritey, con, FPS = re(FPS, speed)
            else:
                over()

        if -cell <= spritebx - spritex <= cell and -cell <= spriteby - spritey <= cell:
            con = True
            spritebx, spriteby, point, min, max = new_pos(lvl, point)
        pygame.display.update()


if __name__ == '__main__':
    main_window(FPS, point)