# Import all essential libraries

import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 30
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
ROCKET = 'gallery/sprites/rocket.png'
BACKGROUND = 'gallery/sprites/background.png'
ASTEROID = 'gallery/sprites/asteroid.png'

# Creating welcome screen of the game
def welcomeScreen():

    rocketx = int(SCREENWIDTH/5)
    rockety = int((SCREENHEIGHT - GAME_SPRITES['rocket'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    
    while True:
        for event in pygame.event.get():
            
            # If user clicks on cross button or presses esc key, the game closes.
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, the game starts
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['rocket'], (rocketx, rockety))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

# Creating randomised asteroids' spawner
def getRandomasteroid():

    asteroidHeight = GAME_SPRITES['asteroid'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    asteroidX = SCREENWIDTH + 10
    y1 = asteroidHeight - y2 + offset
    asteroid = [
        {'x': asteroidX, 'y': -y1}, #upper asteroid
        {'x': asteroidX, 'y': y2} #lower asteroid
    ]
    return asteroid

# Placement of elements in the game
def mainGame():
    score = 0
    rocketx = int(SCREENWIDTH/5)
    rockety = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 asteroids for blitting on the screen
    newBelt1 = getRandomasteroid()
    newBelt2 = getRandomasteroid()

    # List of upper asteroids
    upperasteroids = [
        {'x': SCREENWIDTH+200, 'y':newBelt1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newBelt2[0]['y']},
    ]
    # List of lower asteroids
    lowerasteroids = [
        {'x': SCREENWIDTH+200, 'y':newBelt1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newBelt2[1]['y']},
    ]

    # Defining velocity of the elements in the game
    asteroidVelX = -4

    rocketVelY = -9
    rocketMaxVelY = 10
    rocketMinVelY = -8
    rocketAccY = 1

    rocketthrust = -8 # velocity while thrusting
    rocketthrusted = False # It is true only when the rocket is thrusting

    # Looping the execution of program until input (SPACE, UP ARROW KEY, ESC)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if rockety > 0:
                    rocketVelY = rocketthrust
                    rocketthrusted = True
                    GAME_SOUNDS['wing'].play()

        # How game reacts whem crashed
        crashTest = isCollide(rocketx, rockety, upperasteroids, lowerasteroids) # This function will return true if the rocket is crashed
        if crashTest:
            return     

        # Check for score
        rocketMidPos = rocketx + GAME_SPRITES['rocket'].get_width()/2
        for asteroid in upperasteroids:
            asteroidMidPos = asteroid['x'] + GAME_SPRITES['asteroid'][0].get_width()/2
            if asteroidMidPos<= rocketMidPos < asteroidMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if rocketVelY <rocketMaxVelY and not rocketthrusted:
            rocketVelY += rocketAccY

        if rocketthrusted:
            rocketthrusted = False            
        rocketHeight = GAME_SPRITES['rocket'].get_height()
        rockety = rockety + min(rocketVelY, GROUNDY - rockety - rocketHeight)

        # Move asteroids to the left
        for upperasteroid , lowerasteroid in zip(upperasteroids, lowerasteroids):
            upperasteroid['x'] += asteroidVelX
            lowerasteroid['x'] += asteroidVelX

        # Add/spawn a new asteroid when the first is about to cross the leftmost part of the screen
        if 0<upperasteroids[0]['x']<5:
            newasteroid = getRandomasteroid()
            upperasteroids.append(newasteroid[0])
            lowerasteroids.append(newasteroid[1])

        # If the asteroid is out of the screen, remove it
        if upperasteroids[0]['x'] < -GAME_SPRITES['asteroid'][0].get_width():
            upperasteroids.pop(0)
            lowerasteroids.pop(0)
        
        # Blitting the sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperasteroid, lowerasteroid in zip(upperasteroids, lowerasteroids):
            SCREEN.blit(GAME_SPRITES['asteroid'][0], (upperasteroid['x'], upperasteroid['y']))
            SCREEN.blit(GAME_SPRITES['asteroid'][1], (lowerasteroid['x'], lowerasteroid['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['rocket'], (rocketx, rockety))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# How game reacts when collided
def isCollide(rocketx, rockety, upperasteroids, lowerasteroids):
    if rockety> GROUNDY - 25  or rockety<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for asteroid in upperasteroids:
        asteroidHeight = GAME_SPRITES['asteroid'][0].get_height()
        if(rockety < asteroidHeight + asteroid['y'] and abs(rocketx - asteroid['x']) < GAME_SPRITES['asteroid'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for asteroid in lowerasteroids:
        if (rockety + GAME_SPRITES['rocket'].get_height() > asteroid['y']) and abs(rocketx - asteroid['x']) < GAME_SPRITES['asteroid'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

# Allocating the resources and the global dynamics of the game
if __name__ == "__main__":

    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Rocket Rush with ICR')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['asteroid'] =(pygame.transform.rotate(pygame.image.load(ASTEROID).convert_alpha(), 180), 
    pygame.image.load(ASTEROID).convert_alpha()
    )

    # Adding game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['rocket'] = pygame.image.load(ROCKET).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he gives any input
        mainGame() # The main game function 