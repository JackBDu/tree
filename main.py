##########################################################
###                   PYGAME – Trees                  ###
###   2st Project for Data Structure at NYU Shanghai   ###
##########################################################

__author__ = "Jack B. Du (Jiadong Du)"
__copyright__ = "Copyright 2014, the 2st DS Project @NYUSH"
__version__ = "0.0.1"
__email__ = "JackBDu@nyu.edu"
__status__ = "Developing"

import pygame
from pygame.locals import *
import sys
import math
import random

# absolute varibles
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
GRAY_COLOR = (50, 50, 50)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
BRANCH_COLOR = (190, 230, 150)

# manual initialization
pygame.init()
INIT_SCREEN_W = 1024
INIT_SCREEN_H = 768
FPS = 50
bg_color = (30, 30, 30)
fullscreen = False
caption = "Jack's Trees"
FONT_SIZE = 10
FONT = "arial"
shadowUrl = "shadow.png"

# get device info
infoObject = pygame.display.Info()
FULLSCREEN_W = infoObject.current_w
FULLSCREEN_H = infoObject.current_h

# automatic initialization
if fullscreen:
    current_screen_w = FULLSCREEN_W
    current_screen_h = FULLSCREEN_H
else:
    current_screen_w = INIT_SCREEN_W
    current_screen_h = INIT_SCREEN_H

screen = pygame.display.set_mode((current_screen_w, current_screen_h), 0, 32)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_color)
font = pygame.font.SysFont("arial", FONT_SIZE)

# some values about the treesglitter
treeSize = 12
treeLength = 70
angle = 0.3
rootX = current_screen_w/2
rootY = current_screen_h - 100
wind = 0
crazy = False
glitter = False

pygame.display.set_caption(caption)

def main():
    global screen, fullscreen, background, current_screen_w, current_screen_h, angle, treeSize, rootX, rootY, wind, crazy, bg_color, glitter
    
    mainloop = True

    a = 0.0015
    treeSizeNow = 0
    windAdjust = 0
    
    while mainloop:

        # handling FPS
        pygame.time.Clock().tick(FPS)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                mainloop = False

            # handling fullscreen
            if event.type == KEYDOWN:
                if event.key == K_f:
                    refresh = True
                    fullscreen = not fullscreen
                    if fullscreen:
                        current_screen_w = FULLSCREEN_W
                        current_screen_h = FULLSCREEN_H
                        screen = pygame.display.set_mode((current_screen_w, current_screen_h), FULLSCREEN, 32)
                        rootX = current_screen_w/2
                        rootY = current_screen_h - 150
                    else:
                        current_screen_w = INIT_SCREEN_W
                        current_screen_h = INIT_SCREEN_H
                        screen = pygame.display.set_mode((current_screen_w, current_screen_h), 0, 32)
                        rootX = current_screen_w/2
                        rootY = current_screen_h - 100
                    background = pygame.Surface(screen.get_size())
                    background = background.convert()
                    background.fill(bg_color)
                elif event.key == K_EQUALS:
                    treeSize += 1
                    treeSizeNow += 1
                elif event.key == K_MINUS:
                    treeSize -= 1
                    treeSizeNow -= 1
                elif event.key == K_w:
                    rootY -= 10
                elif event.key == K_s:
                    rootY += 10
                elif event.key == K_a:
                    rootX -= 10
                elif event.key == K_d:
                    rootX += 10
                elif event.key == K_LEFT:
                    windAdjust -= 0.003
                elif event.key == K_RIGHT:
                    windAdjust += 0.003
                elif event.key == K_c:
                    crazy = not crazy
                elif event.key == K_g:
                    glitter = not glitter
                elif event.key == K_r:
                    treeSizeNow = 0

        if pygame.mouse.get_pressed()[0]==1:
             
            try:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
            except Exception as err:
                return err

        wind += windAdjust

        angle += a
        
        if angle > 0.32 or angle < 0.28:
            a *= -1
        if treeSize > treeSizeNow:
            treeSizeNow += 0.1    

        background.fill(bg_color)
        screen.blit(background,(0,0))
        
        # call the tree function to draw the tree
        tree((rootX, rootY), int(treeSizeNow), -treeLength, angle, GRAY_COLOR)
        tree((rootX, rootY), int(treeSizeNow), treeLength, angle, BRANCH_COLOR)
        
        pygame.display.update()
        
    pygame.quit()
    
# start is the start point for each branch
# n is the size of the tree, the biggest number of branches the tree has from root to leaf
# length is the length of the branch
# angle is the angle step
# currentAngle is the current angle for the branch
# x is the class of branch
def tree(start, n, length, angle, COLOR, currentAngle = 0, x = 0):
    
    if x < n:

        # end is the end point for each branch
        end = (start[0] + length * math.sin(currentAngle), start[1] - length * math.cos(currentAngle))

        # draw a branch
        pygame.draw.line(screen, COLOR, start, end, n-x)
        
        # call itself to draw the other two branches

        if crazy:
            tree(end, n, random.randint(abs(length)-5,abs(length))*length/abs(length), angle, COLOR, currentAngle + angle + wind, x + 1)
            tree(end, n, random.randint(abs(length)-5,abs(length))*length/abs(length), angle, COLOR, currentAngle - angle + wind, x + 1)
        else:
            tree(end, n, length - length/20, angle, COLOR, currentAngle + angle + wind*length/abs(length), x + 1)
            tree(end, n, length - length/20, angle, COLOR, currentAngle - angle + wind*length/abs(length), x + 1)            

        # draw the glitter
        if n - x <= 1 and glitter:
            pygame.draw.circle(screen, GREEN_COLOR, (int(end[0]), int(end[1])), 1, 0)
        
main()
