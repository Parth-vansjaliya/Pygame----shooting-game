import pygame
from pygame.locals import *
import time, random
import math

pygame.init()

WIDTH = 800
HEIGHT = 500

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
win_color = (100, 200, 100)
lose_color = (200, 100, 100)

FPS = 60
clock = pygame.time.Clock()

gamewindow = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Shooting Game")

icon = pygame.image.load('./img/icon.png')

pygame.display.set_icon(icon)

def terminate():
    pygame.quit()
    quit()    

def collision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow((x1-18) - x2, 2) + math.pow(y1 - (y2-10), 2)))
    if distance < 20:
        return True

    else:
        return False

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    gamewindow.blit(bullet, [x+20, y])

def text_blit(text, color, x, y, size):
    font1 = pygame.font.SysFont('arial', size, bold=True)
    font = font1.render(text, True, color)
    frect = font.get_rect()
    frect.center = (x, y)
    gamewindow.blit(font, frect)

def block(text, color, x, y):
    b = pygame.draw.rect(gamewindow, color, [x, y, block_size, block_size], border_radius=4)
    text_blit(str(No), black, b.center[0], b.center[1], 22)

def winner():
    if player == 'winner':
        a = False
        while not a:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()

                    if event.key == K_RETURN:
                        gameloop()

            gamewindow.fill(win_color)
            text_blit("You Won, Congrats", blue, 400, 200, 20)
            text_blit("Would you like to play again, Press Enter", blue, 400, 235, 20)
            pygame.display.update()
            clock.tick(FPS)

def lose():
    if player == 'lose':
        b = False
        while not b:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                    if event.key == K_RETURN:
                        gameloop()

            gamewindow.fill(lose_color)
            text_blit("You Lose", red, 400, 200, 20)
            text_blit("Would you like to play again, Press Enter", red, 400, 235, 20)
            pygame.display.update()
            clock.tick(FPS)


def gameloop():
    global block_size, No, bullet, bullet_state, player
    exit_game = False

    block_size = 35
    block_x = 100
    block_y = 50
    blockchange_x = 2
    blockchange_y = 40
    blockVelocity = 2
    
    No = random.randint(5, 26)
    player = ''
    no_of_bullet = No + 2

    bg1 = pygame.image.load('./img/bg.jpg').convert_alpha()
    bg = pygame.transform.scale(bg1, (WIDTH, HEIGHT))

    space_ship1 = pygame.image.load('./img/spaceship.png').convert_alpha()
    space_ship = pygame.transform.scale(space_ship1, (70, 70))
    ship_x = 380
    ship_y = 400
    velocity_x = 0
    velocity_y = 0
    velocity = 4

    bullet_img = pygame.image.load("./img/bullet.png").convert_alpha()
    bullet = pygame.transform.scale(bullet_img, (30, 30))
    bullet_rect = bullet.get_rect()
    bullet_x = 400
    bullet_y = 400
    bulletchangeY = 0
    bulletVelocity = 10
    bullet_state = 'Ready'

    while not exit_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    velocity_x = velocity; velocity_y = 0

                if event.key == K_LEFT:
                    velocity_x = - velocity; velocity_y = 0

                if event.key == K_b:
                    if bullet_state == 'Ready':
                        bullet_state = 'fire'
                        bullet_x = ship_x
                        no_of_bullet -= 1
                        bulletchangeY = - bulletVelocity
                
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    velocity_x = 0; velocity_y = 0

                if event.key == K_LEFT:
                    velocity_x = 0; velocity_y = 0

        ship_x = ship_x + velocity_x
        
        if ship_x <= 0:
            ship_x = 0

        elif ship_x >= 730:
            ship_x = 730

        block_x = block_x + blockchange_x

        if block_x <= 10:
            blockchange_x = blockVelocity
            block_y = block_y + blockchange_y
        
        elif block_x >= 750:
            blockchange_x = - blockVelocity
            block_y = block_y + blockchange_y

        if bullet_y <= 10:
            bullet_y = 400
            bullet_state = 'Ready'

        iscoll = collision(block_x, block_y, bullet_x, bullet_y)
        if iscoll:
            bullet_y = 400
            bullet_state = 'Ready'
            No -= 1
            block(str(No), green, block_x, block_y)
            if No == 0:
                if no_of_bullet >= 1:
                    player = 'winner'
                    winner()
                else:
                    player = "lose"
                    lose()

        if no_of_bullet == 0 and bullet_state == 'Ready':
            player = "lose"
            lose()

        if block_y > 380:
            player = "lose"
            lose()

        # gamewidow.blit(bg, (0, 0))
        gamewindow.fill(white)
        block('1', green, block_x, block_y)
        gamewindow.blit(space_ship, (ship_x, ship_y))

        if bullet_state == 'fire':
            bullet_y = bullet_y + bulletchangeY
            fire_bullet(bullet_x, bullet_y)

        text_blit("Welcom to our Shooting Game", green, 380, 30, 20)
        text_blit("Bullets Left = " + str(no_of_bullet), green, 80, 30, 20)
        pygame.display.update()
        clock.tick(FPS)

gameloop()
