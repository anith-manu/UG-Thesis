import pygame
import pygame.gfxdraw
from pygame.locals import *
import sys
import csv
import time
import pandas as pd
import math
import random

pygame.init()


# Class used to simplify drawing rectangular targets 
class Button():
    def __init__(self, color, x, y, width=0, height=0, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    # Method called to check if cursor is over target
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
       
    def setColor(self, color):
        self.color = color


            
# Test suite class comprising of all 6 tests
class Game():

    
    # Simple discrete pointing task 
    def test1(testID):
        
        test1 = pd.DataFrame(columns = ['trialNo', 'targetX', 'targetY', 'participant', 'testTime', 'trialTime', 'mouseX', 'mouseY', 'click', 'targetLength', 'overTarget', 'misses'])
        resetCoord = [int(w/2),int(h/2)]        
        overTarget = False
        misses = 0 

        # Target coordinates
        targetCoords = [[100,50], [500,500], [w-300, h-100], [w-100, h-300], [w-100, 30], [250, 600], [350,300], [resetCoord[0]+150, resetCoord[1]+150], [resetCoord[0]+200, resetCoord[1]], [resetCoord[0], resetCoord[1]-350]]
        test_ticks=pygame.time.get_ticks()

        # Target sizes 
        if testID == 1:
            length = 75            
        elif testID == 2:
            length = 50
        elif testID == 3:
            length = 25           

        repeat = 0
        while repeat < 10: # Repeatitions
            for i in targetCoords:
                trial_ticks=pygame.time.get_ticks()
                
                win.fill((255,255,255))
                
                pygame.mouse.set_pos(resetCoord)
                pygame.draw.circle(win, (255,0,0), resetCoord, 10)

                target = Button(green, i[0], i[1], length, length, '' )
                target.draw(win, (0,0,0))
                         
                run = True
                while run:
                    click = False
                    testTime=(pygame.time.get_ticks()-test_ticks)/1000
                    trialTime=(pygame.time.get_ticks()-trial_ticks)/1000
                    
                    x, y = pygame.mouse.get_pos()
                                
                    pygame.display.update()
                    for event in pygame.event.get():
                            
                        if event.type == pygame.QUIT:
                            pygame.quit(); sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit(); sys.exit()

                        if target.isOver([x,y]):
                            overTarget = True
                        else:
                            overTarget = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click = True
                            pos = pygame.mouse.get_pos()
                            if target.isOver([x,y]):
                                run = False
                            else:
                                misses+=1
                                
                        test1.loc[len(test1)] = [repeat+1, i[0], i[1], participant, testTime, trialTime, x, y, click, length, overTarget, misses]
            repeat+=1
                
        test1.to_csv("Test1/test1-ID"+str(testID)+"-P"+str(participant)+".csv", index=False)



    # Linear layout discrete pointing task 
    def test2(testID):
        
        misses = 0       
        targetOrder = [5,2,4,1,3]
        mousePos = 0
        mouseResetCoord = [0,0]
        click = False
        overTarget = False

        test2 = pd.DataFrame(columns = ['trialNo', 'resetPosNo', 'targetX', 'targetY', 'targetNo', 'participant', 'testID', 'testTime', 'trialTime', 'mouseX', 'mouseY', 'click', 'targetHeight', 'targetWidth', 'overTarget', 'overDistractor', 'misses'])
        
        test_ticks=pygame.time.get_ticks()

        repeat = 0
        while repeat < 10: #Repeatitions
            mousePos = 0     
            while mousePos < 4:

                # Horizontal layout
                if testID == 1:                   
                    width = 200 #Target Size 
                    height = 50
                    distance = 205 #Targets left padding
                    mouseResetCoord = [int(w/2), 300+170*mousePos] # Calculate reset positions
                    pygame.mouse.set_pos(mouseResetCoord)

                # Vertical layout    
                elif testID == 2:
                    width = 150
                    height = 50
                    distance = 70 #Targets top padding
                    mouseResetCoord = [340+200*mousePos, int(h/2)]
                    pygame.mouse.set_pos(mouseResetCoord)
                                  
                for i in targetOrder:
                    trial_ticks=pygame.time.get_ticks()
                    
                    win.fill(white)
                    
                    pygame.draw.circle(win, 0, mouseResetCoord, 10)

                    # Draw green target
                    if testID == 1:
                        targetx = i*distance
                        targety = 50
                        target = Button((0,255,0), targetx, targety, width, height, '' )
                        target.draw(win, (0,0,0))
                        
                    elif testID == 2:
                        targetx = 20
                        targety = (i*distance)+220
                        target = Button((0,255,0), targetx, targety, width, height, '' )
                        target.draw(win, (0,0,0))
                    
                    x = 1

                    # Draw distractor (red) targets
                    while x <= 5:                
                        if x!=i:
                            if testID == 1:
                                distractor = Button((255,0,0), x*distance, 50, width, height, '' )
                                distractor.draw(win, (0,0,0))
                            if testID == 2:
                                distractor = Button((255,0,0), 20, (x*distance)+220, width, height, '' )
                                distractor.draw(win, (0,0,0))      
                        x+=1

                    run = True
                    while run:
                        click = False
                        
                        testTime=(pygame.time.get_ticks()-test_ticks)/1000
                        trialTime=(pygame.time.get_ticks()-trial_ticks)/1000
                        
                        x, y = pygame.mouse.get_pos()

                        pygame.display.update()
                        for event in pygame.event.get():

                            if event.type == pygame.QUIT:
                                pygame.quit(); sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    pygame.quit(); sys.exit()

                            if target.isOver([x,y]):
                                overTarget = True
                            else:
                                overTarget = False

                            if (win.get_at([x,y]) == (255, 0, 0)):
                                overDistractor = True
                            else:
                                overDistractor = False

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                click = True
                                if target.isOver([x,y]):
                                    pygame.mouse.set_pos(mouseResetCoord)
                                    run = False
                                else:
                                    misses+=1
                    
                            test2.loc[len(test2)] = [repeat+1, mousePos+1, targetx, targety, i, participant, testID, testTime, trialTime, x, y, click, height, width, overTarget, overDistractor, misses]
                mousePos+=1
            repeat+=1

        test2.to_csv("Test2/test2-ID"+str(testID)+"-P"+str(participant)+".csv", index=False)



    # One-dimensional reciprocal tapping task
    def test3(testID):
        
        hits = 0
        misses = 0
        click = False
        overTarget = False
        timeLimit = 90 # Time limit
        resetCoords = [[w-80,50],[w-300,300],[w-350,500]] 

        win.fill(white)

        test3 = pd.DataFrame(columns = ['targetCount', 'targetX', 'targetY', 'participant', 'testID', 'testTime', 'mouseX', 'mouseY', 'click', 'targetHeight', 'targetWidth', 'overTarget', 'hits', 'misses'])

        pygame.display.update()

        clock = pygame.time.Clock()

        circley = 0 #Variable used to restrict y-coordinate movement
        
        if testID == 1:
            target1x = 50 # Target 1 x-coord 
            target2x = w-80 # Target 2 x-coord 
            targety = 50 # Fixed y-coord for both targets
            height = 100 # Targets height
            width = 35 # Target widths
            circley = 100
            target1 = Button(green, target1x, targety, width, height, '' )
            target2 = Button(red, target2x, targety, width, height, '' )
            pygame.mouse.set_pos(resetCoords[0])

        elif testID == 2:
            target1x = 300
            target2x = w-300
            targety = 300
            height = 100
            width = 70
            circley = 350
            target1 = Button(green, target1x, targety, width, height, '' )
            target2 = Button(red, target2x, targety, width, height, '' )
            pygame.mouse.set_pos(resetCoords[1])

        else:
            target1x = 50
            target2x = w-50
            targety = 500
            height = 100
            width = 10
            circley = 550
            target1 = Button(green, target1x, targety, width, height, '' )
            target2 = Button(red, target2x, targety, width, height, '' )
            pygame.mouse.set_pos(resetCoords[2])

        targetx = target1x
        
        target1count = 1 # No. of times target 1 has become target (turned green)
        target2count = 0 # No. of times target 2 has become target (turned green)
        
        targetCount = target1count
        
        start_ticks=pygame.time.get_ticks()

        run = True
        while run:
            
            win.fill(white)
            
            target1.draw(win, (0,0,0))
            target2.draw(win, (0,0,0))
        
            click = False

            # timer
            seconds=(pygame.time.get_ticks()-start_ticks)/1000
            if seconds > timeLimit: 
                run = False

            x, y = pygame.mouse.get_pos()
            cursor = pygame.draw.circle(win, 0, [x,circley], 8) # circle that moves only horizontally
            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                     pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

                if target1.isOver([x,y]) or target2.isOver([x,y]):
                    overTarget = True
                else:
                    overTarget = False                    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                    if target1.isOver([x,circley]):
                        targetx = target2x
                        target1.setColor(red)
                        target1.draw(win, (0,0,0))

                        target2.setColor(green)
                        target2.draw(win, (0,0,0))
                        
                        pygame.display.update()

                        target2count+=1
                        targetCount = target2count
                        
                        hits+=1
                        
                    elif target2.isOver([x,circley]):
                        
                        targetx = target1x
                        target2.setColor(red)
                        target2.draw(win, (0,0,0))

                        target1.setColor(green)
                        target1.draw(win, (0,0,0))

                        pygame.display.update()

                        target1count+=1
                        targetCount = target1count

                        hits+=1

                    else:
                        misses+=1
                        
                test3.loc[len(test3)] = [targetCount, targetx, targety, participant, testID, seconds, x, circley, click, height, width, overTarget, hits, misses]
               
        test3.to_csv("Test3/test3-ID"+str(testID)+"-P"+str(participant)+".csv", index=False)
            


    # Reciprocal tapping test with tunnel
    def test4(testID):

        crossed = False #variable to check tunnel border collision with circle (cursor)
        overTarget = False
        crossedCount = 0 #variable to track number of collision readings
        timeLimit = 90 # Time limit
        hits = 0

        if testID == 1:
            twidth = 150 #tunnel width
            width = 100 #target width
        elif testID == 2:
            twidth = 100
            width = 100
        else:
            twidth = 50
            width = 100

        test4 = pd.DataFrame(columns = ['targetX', 'targetY', 'participant', 'tunnelWidth', 'testTime', 'mouseX', 'mouseY', 'click', 'targetHeight', 'targetWidth', 'overTarget', 'crossed', 'crossedCount', 'hits'])

        clock = pygame.time.Clock()
        resetCoord = (1300,h/2)

        target1x = 0        
        target2x = w-width
        targety = (h/2)-(twidth/2)

        target1 = Button(green, target1x, targety, width, twidth)
        target2 = Button(red, target2x, targety, width, twidth)    

        targetx = target1x

        # Tunnel borders drawn as rectangles of width 1 to make collision detection easier
        line1rect = pygame.Rect(100,(h/2)-(twidth/2), w-2*(width), 1) 
        line2rect = pygame.Rect(100, (h/2)+(twidth/2), w-2*(width), 1)
        
        pygame.display.update()

        pygame.mouse.set_pos(resetCoord)

        start_ticks=pygame.time.get_ticks()
        
        run = True
        while run:
            crossed = False
            click = False

            #timer
            seconds=(pygame.time.get_ticks()-start_ticks)/1000
            if seconds > timeLimit:
                run = False        
                
            win.fill(white)
                    
            target1.draw(win, (0,0,0))
            target2.draw(win, (0,0,0))

            # draw tunnel borders
            pygame.draw.line(win, 0, [width, (h/2)-(twidth/2)], [w-(width), (h/2)-(twidth/2)], 3)
            pygame.draw.line(win, 0, [width, (h/2)+(twidth/2)], [w-(width), (h/2)+(twidth/2)], 3)            
     
            x,y = pygame.mouse.get_pos()
            cursor = pygame.draw.circle(win, 0, [x,y], 10) #circle that follows cursor
            pygame.display.update()
            clock.tick(60)
           
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                    
                if event.type == pygame.MOUSEMOTION:
                    # check if circle collided with tunnel borders
                    if cursor.colliderect(line1rect) or cursor.colliderect(line2rect):
                        crossedCount += 1
                        crossed = True
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                    if target1.isOver([x,y]) or target2.isOver([x,y]):
                        overTarget = True
                        hits += 1
                    else:
                        overTarget = False
                        
                    if target1.isOver([x,y]):
                        targetx = target2x
                        target2.setColor(green)
                        target1.setColor(red)                    
                    elif target2.isOver([x,y]):
                        targetx = target1x
                        target1.setColor(green)
                        target2.setColor(red)
                    
                test4.loc[len(test4)] = [targetx, targety, participant, twidth, seconds, x, y, click, h, width, overTarget, crossed, crossedCount, hits]

        test4.to_csv("Test4/test4-ID"+str(testID)+"-P"+str(participant)+".csv", index=False)
      


    # Zig-zag tunnel tests
    # Parameters
    # rows - to iterate through rows of 'maze'
    # cols - to iterate through columns of 'maze'
    # maze - 1-d array representing the entire maze
    # twidth - to set width of tunnel
    def test5(rows, cols, maze, testID, twidth):

        test5 = pd.DataFrame(columns = ['targetX', 'targetY', 'participant', 'tunnelWidth', 'testTime', 'mouseX', 'mouseY', 'targetHeight', 'targetWidth', 'overTarget', 'crossed', 'crossedCount', 'click', 'hits', 'misses'])           
    
        resetCoord = (10,10)
        pygame.mouse.set_pos(resetCoord)
        borders = [] #array that stores pygame rectangle values of all black areas (used to detect collision)
        hits = 0
        misses = 0
        timeLimit = 90 # Time limit
        crossed = False
        overTarget = False
        click = False
        crossedCount = 0
        clock = pygame.time.Clock()
        
        x = 0
        y = 0

        # iterate through 'maze'
        for i in range(0,cols*rows):
            # store black rectangle details in 'borders'
            if maze[ x + (y*cols) ] == 0:
                borders.append(pygame.draw.rect(win, 0, (x * twidth, y * twidth, twidth, twidth)))
            x = x + 1
            if x > cols-1:
                x = 0 
                y = y + 1 

        start_ticks=pygame.time.get_ticks()
        
        run = True
        while run:
            click = False
            crossed = False
            seconds=(pygame.time.get_ticks()-start_ticks)/1000
            if seconds > timeLimit:
                run = False
                
            pygame.event.pump()
            win.fill(white)
            bx = 0
            by = 0
            
            targetx = 0
            targety = 0

            # iterate through 'maze'
            for i in range(0,cols*rows): 
                # draw black squares at locations in 'maze' with value 0
                if maze[ bx + (by*cols) ] == 0:
                    pygame.draw.rect(win, 0, (bx * twidth, by * twidth, twidth, twidth))
                # draw green target at location in 'maze' with value 2    
                elif maze[ bx + (by*cols) ] == 2:
                    targetx = bx * twidth
                    targety = by * twidth
                    target = Button(green, bx * twidth, by * twidth, twidth, twidth)
                    target.draw(win, 0)
                bx = bx + 1
                if bx > cols-1:
                    bx = 0 
                    by = by + 1  
 
            x,y = pygame.mouse.get_pos()
            cursor = pygame.draw.circle(win, red, [x,y], 10) # red circle that follows cursor    
            pygame.display.update()
            clock.tick(60)
                
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                        
                elif event.type == pygame.MOUSEMOTION:
                    # check if circle collided with black squares i.e borders of the tunnel
                    if cursor.collidelistall(borders):
                        crossedCount += 1
                        crossed = True

                if target.isOver([x,y]):
                    overTarget = True
                else:
                    overTarget = False       

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                    if target.isOver([x,y]):
                        pygame.mouse.set_pos(resetCoord)
                        hits+=1
                    else:
                        misses+=1
                        
                test5.loc[len(test5)] = [targetx, targety, participant, twidth, seconds, x, y, twidth, twidth, overTarget, crossed, crossedCount, click, hits, misses]
                
        test5.to_csv("Test5/test5-ID"+str(testID)+"-P"+str(participant)+".csv", index=False)



    # Multi-directional tapping task    
    def test6(testID):

        circles = 9 # number of circles 
        radius = 0  # 22, 55
        distance = 0  # 125, 250, 500
        targetOrder = [1,6,2,7,3,8,4,9,5] # set target order (alternating)
        hits = 0
        misses = 0
        click = False
        overTarget = False
        last_pos = None
        
        targetx = 0
        targety = 0

        test6 = pd.DataFrame(columns = ['targetNo', 'targetX', 'targetY', 'participant', 'testID', 'testTime', 'trialTime', 'mouseX', 'mouseY', 'click', 'targetRadius', 'distance', 'overTarget', 'hits', 'misses'])

        resetCoord = ((w/2), (h/2))
        pygame.mouse.set_pos(resetCoord)

        if testID == 1:
            radius = 20 # circle radius
            distance = 500 # distance between opposite circles 
        elif testID == 2:
            radius = 30
            distance = 350
        elif testID == 3:
            radius = 40
            distance = 200    

        test_ticks=pygame.time.get_ticks()

        repeat = 0
        while repeat < 1: # Repeatitions
        
            for j in targetOrder:

                 trial_ticks=pygame.time.get_ticks()
                
                 win.fill(white)

                 run = True
                 while run:
                    click = False

                    testTime=(pygame.time.get_ticks()-test_ticks)/1000
                    trialTime=(pygame.time.get_ticks()-trial_ticks)/1000
                    
                     # Drawing circles
                    for i in range(1, circles + 1):
                        pygame.gfxdraw.aacircle(win, int(w/2) + int(math.cos(math.pi * 2 / circles * i) * distance / 2),
                                            int(h/2) + int(math.sin(math.pi * 2 / circles * i) * distance / 2),
                                            radius, (100, 100, 100))
                     


                     # Select a circle and make it red
                    targetx = int(w/2) + int(math.cos(math.pi * 2 / circles * j) * distance / 2)
                    targety = int(h/2) + int(math.sin(math.pi * 2 / circles * j) * distance / 2)
                    pygame.gfxdraw.filled_circle(win, targetx, targety, radius, (255, 0, 0))

                    pygame.display.update()

                    x,y = pygame.mouse.get_pos()

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            pygame.quit(); sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit(); sys.exit()

                        # check if cursor is over target
                        if (win.get_at([x,y]) == (255, 0, 0)):
                            overTarget = True
                        else:
                            overTarget = False 
                            
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click = True
                            click = win.get_at([x,y]) == (255, 0, 0)
               
                            if click == 1:
                                hits += 1
                                run = False
                            else:
                                misses +=1

                        test6.loc[len(test6)] = [j, targetx, targety, participant, testID, testTime, trialTime, x, y, click, radius, distance, overTarget, hits, misses]
             
            repeat += 1
                     
        test6.to_csv("Test6/test6-ID"+str(testID)+"-P"+str(participant)+".csv", index=False)                



            

red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
            
win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#win = pygame.display.set_mode((1340,900))
w, h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Tracking Tests")

# Participant number
participant = 7



### Test-5 setup ###
rows = 15 
cols = 10
maze1 = [1,1,1,0,0,0,0,0,0,0,
         0,0,1,1,1,0,0,0,0,0,
         0,0,0,0,1,1,1,0,0,0,
         0,0,0,0,0,0,1,1,2,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,]

maze2 = [1,0,0,0,0,0,0,0,0,0,
         1,0,0,0,0,0,0,0,0,0,
         1,1,0,0,0,0,0,0,0,0,
         0,1,0,0,0,0,0,0,0,0,
         0,1,1,0,0,0,0,0,0,0,
         0,0,1,0,0,0,0,0,0,0,
         0,0,2,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,]

tunnelWidth1 = 40
tunnelWidth2 = 55
tunnelWidth3 = 70




### Run Tests ####
Game.test1(1) 
Game.test1(2)
Game.test1(3)

Game.test2(1)
Game.test2(2)

Game.test3(1)
Game.test3(2)
Game.test3(3)

Game.test4(1)
Game.test4(2)
Game.test4(3)

Game.test5(rows, cols, maze1, 1, tunnelWidth1)
Game.test5(rows, cols, maze1, 2, tunnelWidth2)
Game.test5(rows, cols, maze1, 3, tunnelWidth3)

Game.test5(rows, cols, maze2, 4, tunnelWidth1)
Game.test5(rows, cols, maze2, 5, tunnelWidth2)
Game.test5(rows, cols, maze2, 6, tunnelWidth3)

Game.test6(1)
Game.test6(2)
Game.test6(3)

pygame.quit(); sys.exit()
