#!/usr/bin/python
# Import libraries 
import pygame
from time import strftime
import csv
from pprint import pprint
import fcntl

#Size of display on touchscreen
size = (750,500)

#Pygame initialization 
pygame.init()
screen = pygame.display.set_mode(size)

#Title on display window
pygame.display.set_caption("Driver Safety Report System")

#Show Clock
def showClock(clockScreen):

#Create main dashboard display
    clockScreen.fill((0,0,0))
    pygame.draw.rect(screen, (255,255,255), [75, 50, 150, 120], 2)
    pygame.draw.rect(screen, (0,255,0), [270, 50, 150, 120],2)   
    pygame.draw.rect(screen, (0,0,255), [470, 50, 150, 120],2)
    pygame.draw.rect(screen, (255,0,0), [75, 350, 520, 120],2)

    myfont = pygame.font.SysFont("Courier", 15)
    gradefont = pygame.font.SysFont("Courier",60)
    speedfont = pygame.font.SysFont("Courier",70)
    mphfont = pygame.font.SysFont("Courier",50)
#Text
    label = myfont.render("Current Grade: ", 1, (255,255,0))
    screen.blit(label, (100, 10))

    label = myfont.render("MPH: ", 1, (255,255,0))
    screen.blit(label, (320, 10))

    label = myfont.render("Top Speed: ", 1, (255,255,0))
    screen.blit(label, (500, 10))

    label = myfont.render("Activity Log: ", 1, (255,255,0))
    screen.blit(label, (100,300)) 

    with open('data.txt', 'rU', os.O_NONBLOCK) as fp:
      number = 360
      for line in fp:
         line = line.rstrip('\n')
      	 label = myfont.render(line,1,(255,255,0))         
       	 screen.blit(label, (75,number))
         number+=10 


    with open('"speed.txt",'r') as fp:
    fcntl.flock(fd, fcntl.LOCK_EX)
      for line in fp:
         line = line.rstrip('\n')
         label = speedfont.render(line,1,(255,255,0))
         screen.blit(label, (500,70))
    fcntl.flock(fd, fcntl.LOCK_UN)

    with open('mph.txt', 'r') as fp:
    fcntl.flock(fd, fcntl.LOCK_EX)
      for line in fp:
         line = line.rstrip('\n')
         label = mphfont.render(line,1,(255,255,0))
         screen.blit(label, (300,70))
    fcntl.flock(fd, fcntl.LOCK_UN)

    with open('grade.txt', 'rU') as fp:
    fcntl.flock(fd, fcntl.LOCK_EX)
      for line in fp:
         line = line.rstrip('\n')
         label = gradefont.render(line,1,(255,255,0))
         screen.blit(label, (130,70))
    fcntl.flock(fd, fcntl.LOCK_UN)

    pygame.init()
    pygame.font.init()
 
   #Chose fonts
    myfont = pygame.font.SysFont(None, 100)
    myfontsmall = pygame.font.SysFont(None, 50)

    # Create the strings to display
    mytime = strftime("%H:%M")
    mysecs = strftime("%S")
   
    # Final clock labels 
    clocklabel = myfont.render(mytime, 1, (255,255,255))
    secondlabel = myfontsmall.render(mysecs, 1, (255,255,255))


   #A clock API for pygame was used and referred to in order to bring it up on our display screen the link from where the code was obtained from is as follows: https://www.raspberrypi.org/forums/viewtopic.php?f=41&t=51807&hilit=%2bclock#p415267 


    # And position them on the screen
    textpos = clocklabel.get_rect() # Gets the rectangle of the hours and minutes...
    textpos.centerx = clockScreen.get_rect().centerx # ...and center horizontally...
    textpos.centery = clockScreen.get_rect().centery # ...and vertically
    secpos =  (textpos[0] + textpos[2] + 10, textpos[1] + textpos[3] - 55) # A bit of trial and error to position the seconds
   
    # Draw the text
    clockScreen.blit(secondlabel, secpos)
    clockScreen.blit(clocklabel, textpos)
   
    # Update display
    pygame.display.flip()


# Clear
quitloop=False

# Refresh
refresh = 0

# Loop for sconstant update
while not quitloop:
    for event in pygame.event.get():
       
        # Handle quit message received
        if event.type == pygame.QUIT:
            quitloop = True
       
    if pygame.time.get_ticks() > refresh:
       
        # Function call    
        	showClock(screen) 

