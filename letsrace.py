import pygame
import time
import random
from screeninfo import get_monitors
import math
import json

pygame.init()

SONG_FINISHED = pygame.USEREVENT + 1

soundtracks=['soundtrack1.wav','soundtrack2.wav']
pygame.mixer.music.set_endevent(SONG_FINISHED)
crash_sound = pygame.mixer.Sound("car_crash.wav")


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
Car=[]
Car.append(pygame.image.load("Car1.png"))
Car.append(pygame.image.load("Car2.png"))
Car.append(pygame.image.load("Car3.png"))
Car.append(pygame.image.load("Car4.png"))

def get_high_score():
    high_scores=0
    try: 
        with open('high_score.json','r') as f:
            high_scores= json.load(f)
            f.close()
    except IOError:
        print("There is no high score yet.")
    except ValueError:
        print("I'm confused. Starting with no high score.")
    return high_scores

def save_high_score(new_high_score):
    try:
        with open("high_score.json","w") as f:
            f.write(json.dumps(new_high_score))
            f.close()
    except IOError:
        print("Unable to save the high score.")

def things_dodged(count,nop,diff):
    high_score = get_high_score()
    font=pygame.font.SysFont(None,40)
    text=font.render("Score "+str(count),True,black)
    if count > high_score[str(nop)][diff]:
        high_score[str(nop)][diff]=count
        save_high_score(high_score)
    highScore=font.render("High Score "+str(high_score[str(nop)][diff]),True,black)
    gameDisplay.blit(text,(20,20))
    gameDisplay.blit(highScore,(20,50))

def car1(car,x,y):
    gameDisplay.blit(car,(x,y))
    return car.get_rect(x=x, y=y)

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
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    message_display('Player '+car+'Crashed')
    

def crash3():
	message_display('Collision')

def game_loop(): 
    pygame.mixer.music.load('main_menu.wav')
    pygame.mixer.music.play(0)
    song_idx=0
    controls=[[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d],[pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT],[pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l],[pygame.K_KP8,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6]]  
    max_nob = 10
    max_players=4
    starting_speed=0
    number_of_players=0
    gameDisplay.fill(white)
    message_display2('Enter number of players 1-4')
    while(number_of_players==0 or number_of_players>4):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    number_of_players=1
                elif event.key==pygame.K_2:
                    number_of_players=2
                elif event.key==pygame.K_3:
                    number_of_players=3
                elif event.key==pygame.K_4:
                    number_of_players=4
                elif event.key == pygame.K_5:
                    pygame.quit()
                    quit()
    gameDisplay.fill(white)
    y_change=[0]*number_of_players
    x_change=[0]*number_of_players
    car_controls=[[0]*4]*number_of_players
    if(number_of_players==1):
        car_controls[0]=controls[1]
    elif(number_of_players==2):
        car_controls[0]=controls[0]
        car_controls[1]=controls[1]
    elif(number_of_players==3):
        car_controls[0]=controls[0]
        car_controls[1]=controls[2]
        car_controls[2]=controls[1]
    elif(number_of_players==4):
        car_controls[0]=controls[0]
        car_controls[1]=controls[2]
        car_controls[2]=controls[1]
        car_controls[3]=controls[3]

    difficulty=""
    message_display2('Choose a difficulty 1.Easy 2.Medium 3.Hard')
    while(starting_speed==0):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    difficulty="easy"
                    starting_speed=4
                elif event.key==pygame.K_2:
                    difficulty="medium"
                    starting_speed=9
                elif event.key==pygame.K_3:
                    difficulty="hard"
                    starting_speed=14
                elif event.key == pygame.K_4:
                    pygame.quit()
                    quit()
    dividing_factor = 1/(2*number_of_players)
    thing_speed=[starting_speed]*max_nob

    x=[0.0]*number_of_players
    y=[(display_height*0.79)]*number_of_players
    for i in range(0,number_of_players):
        if i==0:
            x[i]=display_width*dividing_factor
        else:
            x[i]=x[i-1]+2*display_width*dividing_factor


    thing_startx = [0]*max_nob
    for i in range(0,max_nob):
        thing_startx[i]=random.randrange(0,display_width)
    thing_starty=[-600]*max_nob
    thing_width=[50]*max_nob
    thing_height=[50]*max_nob

    dodged=0

    gameExit=False
    nob=1
    keypressed=[0]*number_of_players
    pygame.mixer.music.stop()
    pygame.mixer.music.load(soundtracks[song_idx])
    pygame.mixer.music.play(0)
    while not gameExit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:  
                for i in range(0,number_of_players):
                    if event.key in car_controls[i]:
                        if event.key==car_controls[i][0]:
                            x_change[i]=0
                            y_change[i]=-8
                            keypressed[i]=event.key
                        elif event.key==car_controls[i][1]:
                            x_change[i]=-8
                            y_change[i]=0
                            keypressed[i]=event.key
                        elif event.key==car_controls[i][2]:
                            x_change[i]=0
                            y_change[i]=8
                            keypressed[i]=event.key
                        elif event.key==car_controls[i][3]:
                            x_change[i]=8
                            y_change[i]=0
                            keypressed[i]=event.key
                if event.key == pygame.K_CAPSLOCK:
                    pygame.quit()
                    quit()

            if event.type==pygame.KEYUP:
                for i in range(0,number_of_players):
                    if event.key==keypressed[i]:
                        x_change[i]=0
                        y_change[i]=0

            if event.type==SONG_FINISHED:
                song_idx+=1
                song_idx %= len(soundtracks)
                pygame.mixer.music.load(soundtracks[song_idx])
                pygame.mixer.music.play(0)


        for i in range(0,number_of_players):          
            if y[i]+y_change[i]>=display_height:
                y[i]=0
            elif y[i]+y_change[i]<=0:
                y[i]=display_height
            y[i]+=y_change[i]
            if x[i]+x_change[i]>display_width:
                x[i]=0
            elif x[i]+x_change[i]<0:
                x[i]=display_width
            x[i]+=x_change[i]
        gameDisplay.fill(white)

        

        for i in range(0,nob):
            things(thing_startx[i],thing_starty[i],thing_width[i],thing_height[i],black)
            thing_starty[i]+=thing_speed[i]
        cars=[0]*number_of_players
        for i in range(0,number_of_players):
            cars[i]=car1(Car[i],x[i],y[i])

        things_dodged(dodged,number_of_players,difficulty)

        for i in range(0,len(cars)):
            for j in range(i+1,len(cars)):
                if cars[i].colliderect(cars[j]):
                    crash3()


        
        
        for i in range(0,nob):
            if thing_starty[i]>display_height:
                thing_starty[i]=0-thing_height[i]
                thing_startx[i]=random.randrange(0,display_width)
                dodged+=1
                thing_speed[i]+=0.1
            rect  = pygame.rect.Rect(thing_startx[i],thing_starty[i],thing_width[i],thing_height[i])
            for j in range(0,number_of_players):
                if cars[j].colliderect(rect):
                    crash(str(j+1))
                    break
        nob  = min(10,max(1,int(math.ceil(dodged/10))))

        pygame.display.update()
        clock.tick(60)
        
game_loop()
pygame.quit()
quit()
