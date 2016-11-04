#!/usr/bin/python
# Import libraries 
import pygame
from time import strftime
import csv
from pprint import pprint

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

#Text
    label = myfont.render("Current Grade: ", 1, (255,255,0))
    screen.blit(label, (100, 10))

    label = myfont.render("MPH: ", 1, (255,255,0))
    screen.blit(label, (320, 10))

    label = myfont.render("Top Speed: ", 1, (255,255,0))
    screen.blit(label, (500, 10))

    label = myfont.render("Activity Log: ", 1, (255,255,0))
    screen.blit(label, (100,300)) 

    with open('Data.txt', 'rU') as fp:
      number = 360
      for line in fp:
         line = line.rstrip('\n')
      	 label = myfont.render(line,1,(255,255,0))         
       	 screen.blit(label, (75,number))
         number+=10 


    with open('speed.txt', 'rU') as fp:
      for line in fp:
         line = line.rstrip('\n')
         label = myfont.render(line,1,(255,255,0))
         screen.blit(label, (500,70))

    with open('mph.txt', 'rU') as fp:
      for line in fp:
         line = line.rstrip('\n')
         label = myfont.render(line,1,(255,255,0))
         screen.blit(label, (320,70))


    with open('grade.txt', 'rU') as fp:
      for line in fp:
         line = line.rstrip('\n')
         label = myfont.render(line,1,(255,255,0))
         screen.blit(label, (100,70))

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Courier",10)
  
 
   # Define some fonts to draw text with
    myfont = pygame.font.SysFont(None, 100)
    myfontsmall = pygame.font.SysFont(None, 50)

    # Create the strings to display
    mytime = strftime("%H:%M")
    mysecs = strftime("%S")
   
    # Render the strings
    clocklabel = myfont.render(mytime, 1, (255,255,255))
    secondlabel = myfontsmall.render(mysecs, 1, (255,255,255))
   
    # Screen
    textpos = clocklabel.get_rect() # Gets the rectangle of the hours and minutes...
    textpos.centerx = clockScreen.get_rect().centerx # ...and center horizontally...
    textpos.centery = clockScreen.get_rect().centery # ...and vertically
    secpos =  (textpos[0] + textpos[2] + 10, textpos[1] + textpos[3] - 55) # A bit of trial and error to position the seconds
   
    # Draw the text onto our screen
    clockScreen.blit(secondlabel, secpos)
    clockScreen.blit(clocklabel, textpos)
   
    # Update the display (i.e. show the output of the above!)
    pygame.display.flip()


# Set up a boolean for a clean loop
quitloop=False

# Set up a variable to check when to refresh display
refresh = 0

# Run our main loop
while not quitloop:
    for event in pygame.event.get():
       
        # Handle quit message received
        if event.type == pygame.QUIT:
            quitloop = True
       
        # 'Q' to quit   
        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_q):
                quitloop = True
   
    # If pygame's clock is greater than our variable then we need to update display
    if pygame.time.get_ticks() > refresh:
       
        # Run the function to update display     
        showClock(screen)
       
        # Update refresh time to 500ms in the future
        refresh = pygame.time.get_ticks() + 500

def disp(phrase,loc,screen):   # function to display phrase at loc on surface.
    s = font.render(phrase, True, (255,255,255))
    screen.blit(s, loc) 
