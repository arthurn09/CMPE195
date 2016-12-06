#!/usr/bin/python
# Import libraries
#Uptime Resources
#http://thesmithfam.org/blog/2005/11/19/python-uptime-script/
#written by Goonjan Parkhe

import pygame
from time import strftime
import csv
from pprint import pprint
import fcntl
import os
import datetime

#Size of display on touchscreen
size = (800,480)

#Pygame initialization
pygame.init()
screen = pygame.display.set_mode(size)

#Title on display window
pygame.display.set_caption("Driver Safety Report System")

def uptime():
    
    try:
        f = open( "/proc/uptime" )
        contents = f.read().split()
        f.close()
    except:
        return "Cannot open uptime file: /proc/uptime"

    total_seconds = float(contents[0])

# Helper vars:
MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY     = HOUR * 24
    
    # Get the days, hours, etc:
    days    = int( total_seconds / DAY )
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )
    
    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    string = ""
    if days > 0:
        string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
    if len(string) > 0 or hours > 0:
        string += str(hours) + " " + (hours == 1 and "hr" or "hrs" ) + ", "
if len(string) > 0 or minutes > 0:
    string += str(minutes) + " " + (minutes == 1 and "min" or "mins" ) + ", "
        string += str(seconds) + " " + (seconds == 1 and "s" or "s" )
    
    return string;

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
    
    label = myfont.render("Driving Trip: ", 1, (255,255,0))
    screen.blit(label, (80,250))
    label = myfont.render(uptime(), 1, (255,255,0))
    screen.blit(label, (80, 270))
    
    label = myfont.render("Activity Log: ", 1, (255,255,0))
    screen.blit(label, (80,320))
    
    gradeCount = 0
    with open('data.txt', 'rU') as fp:
        fcntl.flock(fp, fcntl.LOCK_EX)
        number = 350
        fp.seek(0)
        for line in fp:
            gradeCount = gradeCount + 1
            if(len(line)>0):
                try:
                    line = line.rstrip('\n')
                    label = myfont.render(line,1,(255,255,0))
                    screen.blit(label, (75,number))
                    number+=10
                except ValueError:
                    pass
        fcntl.flock(fp, fcntl.LOCK_UN)
    
    
    with open('topspeed.txt','r') as fp:
        fcntl.flock(fp, fcntl.LOCK_EX)
        fp.seek(0)
        line = fp.read()
        if(len(line)>0):
            try:
                line = line.rstrip('\n')
                label = speedfont.render(line,1,(255,255,0))
                screen.blit(label, (500,70))
            except ValueError:
                pass
        fcntl.flock(fp, fcntl.LOCK_UN)
    
    with open('speed.txt', 'r') as fp:
        fcntl.flock(fp, fcntl.LOCK_EX)
        fp.seek(0)
        line = fp.read()
        if(len(line)>0):
            try:
                line = line.rstrip('\n')
                label = mphfont.render(line,1,(255,255,0))
                screen.blit(label, (300,70))
            except ValueError:
                pass
        fcntl.flock(fp, fcntl.LOCK_UN)
    
    gradeletter = 'A'
    if gradeCount < 3:
        gradeLetter = 'A'
    elif gradeCount >= 3 and gradeCount< 6:
        gradeLetter = 'B'
    elif gradeCount >= 6 and gradeCount< 9:
        gradeLetter = 'C'
    elif gradeCount >= 9 and gradeCount< 12:
        gradeLetter = 'D'
    else:
        gradeLetter = 'F';
    
    with open('grade.txt', 'rU') as fp:
        fcntl.flock(fp, fcntl.LOCK_EX)
        fp.seek(0)
        line = fp.read()
        if(len(line)>0):
            try:
                #line = line.rstrip('\n')
                line = gradeLetter
                label = gradefont.render(line,1,(255,255,0))
                screen.blit(label, (130,70))
            except ValueError:
                pass
        fcntl.flock(fp, fcntl.LOCK_UN)
    
    pygame.init()
    pygame.font.init()
    
    # Define some fonts to draw text with
    myfont = pygame.font.SysFont(None, 100)
    myfontsmall = pygame.font.SysFont(None, 50)
    
    # Create the strings to display
    mytime = strftime("%H:%M")
    mysecs = strftime("%S")
    
    # Render the strings
    clocklabel = myfont.render(mytime, 1, (255,255,255))
    secondlabel = myfontsmall.render(mysecs, 1, (255,255,255))
    
    # And position them on the screen
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
    
    if pygame.time.get_ticks() > refresh:
        
        # Run the function to update display
        showClock(screen)
