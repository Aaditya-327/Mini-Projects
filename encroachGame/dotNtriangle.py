import pygame, sys, time
from pygame.locals import *
from math import atan, degrees, pi, tan, tan, sin, cos
from random import random
%matplotlib inline

pygame.init()

def display(ends):
    c = ['r', 'g', 'b', 'm']
    for i in range(1, 5):
        plt.plot(ends[i][0], ends[i][1], c[i-1]+'o')

def arctan(x, y):
    if x != 0:
        if x>0:
            if y>0: return atan(y/x)
            else:
                return 2*pi + atan(y/x)
        else:
            return pi+ atan(y/x)
    else:
        return None

def getPoint(x1, y1, length, angle):
    return (x1+ length* cos(angle),
            y1+ length* sin(angle))

def getBetween(p1, p2):
    x1, y1, x2, y2 = *p1, *p2
    seed1 = random()
    return (x1*seed1+ x2*(1-seed1), y1*seed1+ y2*(1-seed1))

def circForm(dictArr):
    p1, p2, p3, p4 = [dictArr[i] for i in range(1, 5)]
    p5, p6 = getBetween(p1, p2), getBetween(p3, p4)
    p7 = getBetween(p5, p6)
    return int(p7[0]), int(p7[1])

root = pygame.display.set_mode((800, 400))
pygame.display.set_caption('what')
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

root.fill(WHITE)
ends, damp = None, (0, 0)
   
center = (150, 250)
angle_width = pi/10
teamPath = [center, ]
redTeam = {"center" : (150, 250), "path" : {center}}
blueTeam = {"center" : (150, 250), "path" : {center}}

count = 0
while True:
    now_pos = pygame.mouse.get_pos() 
    
    (x1, y1), (x2, y2) = center, now_pos
    x, y = x2-x1, y2-y1  
    
    length = (x**2+ y**2)**0.5
    if length > 170: width = 170
    elif length < 70: width = 70
    else: width = length

    angle = arctan(x, y)
    half_wid = width/2
    
   
    if center[0] - now_pos[0] != 0 and angle != None:
        root.fill(WHITE)
        
        # center to width half:       center[0]-width/2        
        radius1 = width*2
        c2w5x, c2w5y = x1 -radius1/2, y1 - radius1/2        
        radius2 = width*1.4
        c2w52x, c2w52y = x1 -radius2/2, y1 - radius2/2  
        
                    
        pygame.draw.circle(root, BLACK, center, 4)
            
        pygame.draw.arc(root, RED, (c2w5x, c2w5y, radius1, radius1), -angle-angle_width, -angle+angle_width, 1)
        pygame.draw.arc(root, RED, (c2w52x, c2w52y, radius2, radius2), -angle-angle_width, -angle+angle_width, 1)

        pygame.draw.line(root, RED, center, getPoint(x1, y1, width, angle-angle_width))
        pygame.draw.line(root, RED, center, getPoint(x1, y1, width, angle+angle_width))
        
        pygame.draw.line(root, GREEN, center, now_pos)
        if ends != None:
            
#             pygame.draw.line(root, RED, (0, 0), getPoint(x1, y1, width, angle-angle_width))
#             pygame.draw.line(root, RED, (0, 0), getPoint(x1, y1, width, angle+angle_width))            
#             pygame.draw.line(root, RED, (0, 0), getPoint(x1, y1, 0.5* radius1, angle+angle_width))
#             pygame.draw.line(root, RED, (0, 0), getPoint(x1, y1, 0.5* radius1, angle-angle_width))
#             pygame.draw.line(root, RED, (0, 0), getPoint(x1, y1, 0.5* radius2, angle-angle_width))
#             pygame.draw.line(root, RED, (0, 0), getPoint(x1, y1, 0.5* radius2, angle+angle_width))
            
#             ends[1] = getPoint(x1, y1, radius1, -angle+angle_width)
#             ends[2] = getPoint(x1, y1, radius1, -angle-angle_width)
#             ends[3] = getPoint(x1, y1, radius2, -angle-angle_width)
#             ends[4] = getPoint(x1, y1, radius2, -angle+angle_width)
            
            if damp not in teamPath: teamPath.append(damp)
            center = damp
            for _ in range(len(teamPath[:-1])):
                pygame.draw.line(root, BLACK, teamPath[_], teamPath[_+1])    
    
#         pygame.draw.line(root, RED, center, getPoint(center, 100, 45 *pi/180))
#         pygame.draw.line(root, GREEN, center, getPoint(center, 100, 135 *pi/180))
#         pygame.draw.line(root, BLUE, center, getPoint(center, 100, 225 *pi/180))
#         pygame.draw.line(root, BLACK, center, getPoint(center, 100, 315 *pi/180))
    
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0] == 1 and angle != None:
            count += 1
            ends = {}
            ends[1] = getPoint(x1, y1, 0.5* radius1, angle+angle_width)
            ends[2] = getPoint(x1, y1, 0.5* radius1, angle-angle_width)
            ends[3] = getPoint(x1, y1, 0.5* radius2, angle-angle_width)
            ends[4] = getPoint(x1, y1, 0.5* radius2, angle+angle_width)
            damp = circForm(ends)
            
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
