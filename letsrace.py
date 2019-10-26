import pygame
import random
import time
import json
from screeninfo import get_monitors
from math import ceil
from colour import Color

pygame.init()

gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SONG_FINISHED = pygame.USEREVENT + 1

soundtracks = ['./media/soundtrack_rock.wav', './media/soundtrack_edm.wav']
pygame.mixer.music.set_endevent(SONG_FINISHED)
crash_sound = pygame.mixer.Sound("./media/car_crash.wav")

display_width, display_height = get_monitors()[0].width, get_monitors()[0].height

black = tuple([c * 255 for c in Color("black").rgb])
white = tuple([c * 255 for c in Color("white").rgb])
red = tuple([c * 255 for c in Color("red").rgb])
brown = tuple([c * 255 for c in Color("brown").rgb])

car_width = 60

background = pygame.image.load('./models/roadtrack.jpg').convert()
background = pygame.transform.scale(background, (display_width, display_height))

pygame.display.set_caption("Lets Race")
clock = pygame.time.Clock()

Car = []
Car.append(pygame.image.load("./models/car_red.png").convert_alpha())
Car.append(pygame.image.load("./models/car_orange.png").convert_alpha())
Car.append(pygame.image.load("./models/car_black_stripes.png").convert_alpha())
Car.append(pygame.image.load("./models/car_black.png").convert_alpha())

def get_high_score():
    high_scores = 0
    try:
        with open('./cfg/high_score.json', 'r') as f:
            high_scores = json.load(f)
            f.close()
    except IOError:
        print("There is no high score yet.")
    except ValueError:
        print("I'm confused. Starting with no high score.")
    return high_scores

def save_high_score(new_high_score):
    try:
        with open("./cfg/high_score.json", "w") as f:
            f.write(json.dumps(new_high_score, indent=4, sort_keys=True))
            f.close()
    except IOError:
        print("Unable to save the high score.")

def blocks_dodged(current_score, number_of_players, difficulty):
    high_score = get_high_score()
    font = pygame.font.SysFont(None, 40)
    score = font.render("Score: " + str(current_score), True, black)
    if current_score > high_score[str(number_of_players)][difficulty]:
        high_score[str(number_of_players)][difficulty] = current_score
        save_high_score(high_score)
    high_score = font.render("High Score: " + str(high_score[str(number_of_players)][difficulty]), True, black)
    gameDisplay.blit(score, (20, 20))
    gameDisplay.blit(high_score, (20, 50))

def car1(car,x,y):
    gameDisplay.blit(car,(x,y))
    return car.get_rect(x=x, y=y)

def things(thingx,thingy,thingw,thingh,color):
    color = brown
    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def text_objects(text,font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def message_display2(text,myFont = 75, xpos = 20, ypos = 20):
    largeText=pygame.font.SysFont('Arial', myFont)
    pos=(xpos,ypos)
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = largeText.size(' ')[0]  # The width of a space.
    max_width, max_height = gameDisplay.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = largeText.render(word, 0, red)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            gameDisplay.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
    pygame.display.update()
    time.sleep(2)

def crash():
    message_display2('F\nGame Over', 72, display_width / 2, display_height / 2)

def crash3():
	message_display('Collision')

def game_loop(controls, difficulty):
    pygame.mixer.music.load('./media/main_menu.wav')
    pygame.mixer.music.play(-1)
    song_idx = 0

    max_nob = 10
    max_players = 4
    starting_speed = 0
    number_of_players = 0
    gameDisplay.fill(white)

    message_display2('Enter number of players: (1 - 4)')
    message_display2('Press Esc to Exit', 50, 20, 120)

    while(number_of_players == 0 or number_of_players > 4):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                number_of_players = event.key - (pygame.K_1 - 1)

    gameDisplay.fill(white)
    y_change = [0] * number_of_players
    x_change = [0] * number_of_players
    car_controls = [[0] * 4] * number_of_players

    if number_of_players == 1:
        car_controls[0] = controls[1]
    elif number_of_players == 2:
        car_controls[0] = controls[0]
        car_controls[1] = controls[1]
    elif number_of_players == 3:
        car_controls[0] = controls[0]
        car_controls[1] = controls[2]
        car_controls[2] = controls[1]
    elif number_of_players == 4:
        car_controls[0] = controls[0]
        car_controls[1] = controls[2]
        car_controls[2] = controls[1]
        car_controls[3] = controls[3]

    message_display2('Choose a difficulty: \n1. Easy \n2. Medium \n3. Hard')

    while starting_speed == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                starting_speed = (event.key - (pygame.K_1 - 1)) * 5 - 1
                for difficulty_level, value in difficulty.items():
                    if value == starting_speed:
                        difficulty = difficulty_level
                        break

    dividing_factor = 1 / (2 * number_of_players)
    thing_speed = [starting_speed] * max_nob

    x = [0.0] * number_of_players
    y = [(display_height * 0.79)] * number_of_players

    for i in range(0, number_of_players):
        if i == 0:
            x[i] = display_width * dividing_factor
        else:
            x[i] = x[i - 1] + 2 * display_width * dividing_factor

    thing_startx = [0] * max_nob
    for i in range(0, max_nob):
        thing_startx[i] = random.randrange(0, display_width)

    thing_starty = [-600] * max_nob
    thing_width = [50] * max_nob
    thing_height = [50] * max_nob

    dodged = 0

    gameExit = False
    nob = 1
    keypressed = [0] * number_of_players
    pygame.mixer.music.stop()

    background_size = background.get_size()
    background_rect = background.get_rect()

    w, h = background_size
    back_x = 0
    back_y = 0

    back_x1 = 0
    back_y1 = -h
    pygame.mixer.music.load(soundtracks[song_idx])
    pygame.mixer.music.play(0)
    alive = [True] * number_of_players

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                for i in range(0, number_of_players):
                    if(alive[i] == False):
                        continue
                    if event.key in car_controls[i]:
                        if event.key == car_controls[i][0]:
                            x_change[i] = 0
                            y_change[i] = -8
                            keypressed[i] = event.key
                        elif event.key == car_controls[i][1]:
                            x_change[i] = -8
                            y_change[i] = 0
                            keypressed[i] = event.key
                        elif event.key == car_controls[i][2]:
                            x_change[i] = 0
                            y_change[i] = 8
                            keypressed[i] = event.key
                        elif event.key == car_controls[i][3]:
                            x_change[i] = 8
                            y_change[i] = 0
                            keypressed[i] = event.key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYUP:
                for i in range(0, number_of_players):
                    if(alive[i] == False):
                        continue
                    if event.key == keypressed[i]:
                        x_change[i] = 0
                        y_change[i] = 0

            if event.type == SONG_FINISHED:
                song_idx += 1
                song_idx %= len(soundtracks)
                pygame.mixer.music.load(soundtracks[song_idx])
                pygame.mixer.music.play(0)

        for i in range(0, number_of_players):
            if alive[i] == False:
                continue
            if y[i] + y_change[i] >= display_height:
                y[i] = 0
            elif y[i] + y_change[i] <= 0:
                y[i] = display_height
            y[i] += y_change[i]
            if x[i] + x_change[i] > display_width:
                x[i] = 0
            elif x[i] + x_change[i] < 0:
                x[i] = display_width
            x[i] += x_change[i]
        back_y1 += thing_speed[0]
        back_y += thing_speed[0]
        gameDisplay.blit(background,(back_x, back_y))
        gameDisplay.blit(background,(back_x1, back_y1))
        if back_y > h:
            back_y = -h
        if back_y1 > h:
            back_y1 = -h

        for i in range(0, nob):
            things(thing_startx[i], thing_starty[i], thing_width[i], thing_height[i], black)
            thing_starty[i] += thing_speed[i]
        cars = [0] * number_of_players

        for i in range(0, number_of_players):
            if alive[i] == False:
                continue
            cars[i] = car1(Car[i], x[i], y[i])

        blocks_dodged(dodged, number_of_players, difficulty)

        for i in range(0, len(cars)):
            if alive[i] == False:
                continue
            for j in range(i + 1, len(cars)):
                if(alive[j] == False):
                    continue
                if cars[i].colliderect(cars[j]):
                    pygame.mixer.Sound.play(crash_sound)
                    alive[i] = False
                    alive[j] = False

        for i in range(0, nob):
            if thing_starty[i] > display_height:
                thing_starty[i] = 0 - thing_height[i]
                thing_startx[i] = random.randrange(0, display_width)
                dodged += 1
                thing_speed[i] += 0.1
            rect = pygame.rect.Rect(thing_startx[i], thing_starty[i], thing_width[i], thing_height[i])
            for j in range(0, number_of_players):
                if(alive[j] == False):
                    continue
                if cars[j].colliderect(rect):
                    alive[j] = False
                    pygame.mixer.Sound.play(crash_sound)
                    break

        nob  = min(10, max(1, int(ceil(dodged / 10))))
        if alive.count(True) == 0:
            pygame.mixer.music.stop()
            crash()
        pygame.display.update()
        clock.tick(75)

if __name__ == '__main__':
    controls = [[pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d],
    [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT],
    [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l],
    [pygame.K_KP8, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6]]

    difficulty = {
        "easy": 4,
        "medium": 9,
        "hard": 14
    }

    game_loop(controls, difficulty)
    pygame.quit()
    quit()
