import pygame
import time
import random

pygame.init()

display_width=800
display_height=600

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
brown=(165,42,42)

car_width=60

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Lets Race")
clock=pygame.time.Clock()

CarImg=pygame.image.load("Racecar.png")

def things_dodged(count):
    font=pygame.font.SysFont(None,40)
    text=font.render("Score "+str(count),True,black)
    gameDisplay.blit(text,(20,20))

def car1(x,y):
    gameDisplay.blit(CarImg,(x,y))

def car2(x,y):
    gameDisplay.blit(CarImg,(x,y))


def things(thingx,thingy,thingw,thingh,color):
    color=brown

    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def text_objects(text,font):
    textSurface=font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect=text_objects(text, largeText)
    TextRect.center=((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash():
    message_display('You Crashed')

def game_loop():
    y_change=0
    y2_change=0

    x=(display_width*0.48/2)
    y=(display_height*0.79)

    x2=(display_width*0.48*1.5)
    y2=(display_height*0.79)

    x_change=0
    x2_change=0

    thing_startx=random.randrange(0,display_width)
    thing_starty=-600
    thing_speed=9
    thing_width=100
    thing_height=100

    dodged=0

    gameExit=False

    while not gameExit:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a:
                    x_change=-8
                    y_change=0
                elif event.key==pygame.K_d:
                    x_change=8
                    y_change=0
                elif event.key==pygame.K_w:
                    x_change=0
                    y_change=-8
                elif event.key==pygame.K_s:
                    x_change=-0
                    y_change=8
                if event.key==pygame.K_LEFT:
                    x2_change=-8
                    y2_change=0
                elif event.key==pygame.K_RIGHT:
                    x2_change=8
                    y2_change=0
                elif event.key==pygame.K_UP:
                    x2_change=0
                    y2_change=-8
                elif event.key==pygame.K_DOWN:
                    x2_change=-0
                    y2_change=8

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_d or event.key==pygame.K_a or event.key==pygame.K_s or event.key==pygame.K_w or event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    x_change=0
                    y_change=0
                    x2_change=0
                    y2_change=0

        x+=x_change
        if y+y_change>=display_height*0.79:
            y_change=0
        elif y+y_change<=0:
        	y_change=0
        y+=y_change

        x2+=x2_change
        if y2+y2_change>=display_height*0.79:
            y2_change=0
        elif y2+y2_change<=0:
        	y2_change=0
        y2+=y2_change

        gameDisplay.fill(white)

        #things(thingx,thingy,thingw,thingh,color)
        things(thing_startx,thing_starty,thing_width,thing_height,black)
        thing_starty+=thing_speed
        car1(x,y)
        car2(x2,y2)
        things_dodged(dodged)

        if x>display_width-car_width or x<0:
            crash()
        if x2>display_width-car_width or x2<0:
            crash()

        if thing_starty>display_height:
            thing_starty=0-thing_height
            thing_startx=random.randrange(0,display_width)
            dodged+=1
            if thing_speed<15:
                thing_speed+=0.25

        if y<thing_starty+thing_height:
            print('y crossover')

            if ((x>thing_startx and x<thing_startx+thing_width) and (y>thing_starty and y<thing_starty+thing_height)) or ((x+car_width>thing_startx and x+car_width<thing_startx+thing_width) and (y>thing_starty and y<thing_starty+thing_height)):
                print('x crossover')
                crash()
            elif ((x2>thing_startx and x2<thing_startx+thing_width) and (y2>thing_starty and y2<thing_starty+thing_height)) or ((x2+car_width>thing_startx and x2+car_width<thing_startx+thing_width) and (y2>thing_starty and y2<thing_starty+thing_height)):
                print('x crossover')
                crash()

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
