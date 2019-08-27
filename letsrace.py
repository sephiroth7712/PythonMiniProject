import pygame
import time
import random
from screeninfo import get_monitors
import math

pygame.init()

display_width=get_monitors()[0].width
display_height=get_monitors()[0].height

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
brown=(165,42,42)

car_width=60



gameDisplay=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("Lets Race")
clock=pygame.time.Clock()

CarA=pygame.image.load("car1.jpeg")
CarB=pygame.image.load("car2.jpeg")

def get_high_score():
    high_score = 0
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
    except IOError:
        print("There is no high score yet.")
    except ValueError:
        print("I'm confused. Starting with no high score.")
    return high_score

def save_high_score(new_high_score):
    try:
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        print("Unable to save the high score.")

def things_dodged(count):
    high_score = get_high_score()
    font=pygame.font.SysFont(None,40)
    text=font.render("Score "+str(count),True,black)
    if count > high_score:
        save_high_score(count)
    highScore=font.render("High Score "+str(high_score),True,black)
    gameDisplay.blit(text,(20,20))
    gameDisplay.blit(highScore,(20,50))

def car1(x,y):
    gameDisplay.blit(CarA,(x,y))
    return CarA.get_rect(x=x, y=y)

def car2(x,y):
    gameDisplay.blit(CarB,(x,y))
    return CarB.get_rect(x=x, y=y)


def things(thingx,thingy,thingw,thingh,color):
    color=brown
    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def text_objects(text,font):
    textSurface=font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect=text_objects(text, largeText)
    TextRect.center=((display_width/2),(display_height/3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def message_display2(text):
    largeText=pygame.font.Font('freesansbold.ttf',75)
    TextSurf, TextRect=text_objects(text, largeText)
    TextRect.center=((display_width/2),(display_height/3))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

def crash(car):
    message_display('Player '+car+'Crashed')
    

def crash3():
	message_display('Collision')

def game_loop():   
    max_nob = 5
    starting_speed=0
    gameDisplay.fill(white)
    message_display2('Choose a difficulty 1.Easy 2.Medium 3.Hard')
    while(starting_speed==0):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    starting_speed=4
                elif event.key==pygame.K_2:
                    starting_speed=9
                elif event.key==pygame.K_3:
                    starting_speed=14
                elif event.key == pygame.K_4:
                    pygame.quit()
                    quit()
    thing_speed=[starting_speed]*max_nob
    y_change=0
    y2_change=0

    x=(display_width*0.48/2)
    y=(display_height*0.79)

    x2=(display_width*0.48*1.5)
    y2=(display_height*0.79)

    x_change=0
    x2_change=0

    thing_startx = [0]*max_nob
    for i in range(0,max_nob):
        thing_startx[i]=random.randrange(0,display_width)
    thing_starty=[-600]*max_nob
    thing_width=[50]*max_nob
    thing_height=[50]*max_nob

    dodged=0

    gameExit=False
    nob=1
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
                elif event.key == pygame.K_CAPSLOCK:
                    pygame.quit()
                    quit()

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    x2_change=0
                    y2_change=0
                if event.key==pygame.K_d or event.key==pygame.K_a or event.key==pygame.K_s or event.key==pygame.K_w:
                    x_change=0
                    y_change=0

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
        
        for i in range(0,nob):
            things(thing_startx[i],thing_starty[i],thing_width[i],thing_height[i],black)
            thing_starty[i]+=thing_speed[i]

        car_1 = car1(x,y)
        car_2 = car2(x2,y2)
        things_dodged(dodged)

        if car_1.colliderect(car_2):
            crash3()

        if x>display_width-car_width or x<0:
            crash('1')
        if x2>display_width-car_width or x2<0:
            crash('2')
        
        for i in range(0,nob):
            if thing_starty[i]>display_height:
                thing_starty[i]=0-thing_height[i]
                thing_startx[i]=random.randrange(0,display_width)
                dodged+=1
                thing_speed[i]+=0.3
            rect  = pygame.rect.Rect(thing_startx[i],thing_starty[i],thing_width[i],thing_height[i])
            if car_1.colliderect(rect):
                crash('1')
                break
            if car_2.colliderect(rect):
                crash('2')
                break
        nob  = min(5,max(1,int(math.ceil(dodged/10))))

        pygame.display.update()
        clock.tick(60)
        
game_loop()
pygame.quit()
quit()
