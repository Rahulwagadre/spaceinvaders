# import pygame module
import pygame
# import os module to find the path of our utility images
import os

# initializing pygame
pygame.init()

# initializing sound effect library
pygame.mixer.init()

# initializing pygame font library to print text on game window
pygame.font.init()

# setting height and width of game window
WIDTH, HEIGTH = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGTH))

# setting caption to game window
pygame.display.set_caption("First game!")

# making white color combination in rgb formate
WHITE = (255,255,255)

# frames per second which meanes how many times the game window will get refreshed in a second
FPS = 60

# it will decide how fast our space ship and the bullets will move
VEL = 5
BULLET_VEL = 7

# border to seperate the spaceships
BLACK = (0,0,0)       # black
BORDER = pygame.Rect(WIDTH // 2 - 5,0,10,HEIGTH)

# sound effect variables
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

# bullet color
RED = (255,0,0)
YELLOW = (255,255,0)

# maximumum number of bullet any spaceship can shoot
MAX_BULLET = 3

# importing images from our asset folder it will need os module to do so
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets','spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets','spaceship_red.png'))

# resizing the image
SPACE_SHIP_WIDTH = 55
SPACE_SHIP_HEIGHT = 40

YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT))

# rotating the image so that they are opposite and facing to each other
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP,90)
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP,270)

# genereting user event to show that a bullet collide with any spaceship
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# importing space image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets','space.png')),(WIDTH,HEIGTH))

# setting font type and size of the text
HEALTH_FONT = pygame.font.SysFont('comicsans',40)

WINNER_FONT = pygame.font.SysFont('comicsans',100)

# utility fuction
def draw_window(red,yellow,yellow_bullets,red_bullets,yellow_health,red_health):
    # filling game window with white color
    #WIN.fill(WHITE)

    # deploying space image on game window
    WIN.blit(SPACE,(0,0))

    # creating border rectangle
    pygame.draw.rect(WIN,BLACK,BORDER)

    # creating health status text object
    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health),1,WHITE)
    red_health_text = HEALTH_FONT.render("Health : " + str(red_health), 1, WHITE)

    # showing health status on game window
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))

    # deploying both the images in game window
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    # creating bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    # updating game window
    pygame.display.update()

# Yellow spaceship movement controller function
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + 23 < WIDTH/2:  # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGTH:  # down
        yellow.y += VEL
# Red spaceship movement controller function
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > WIDTH/2 + 20:  # Left
        red.x -= VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:  # Up
        red.y -= VEL
    if keys_pressed[pygame.K_RIGHT]and red.x + red.width < WIDTH:  # Right
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGTH:  # down
        red.y += VEL

# bullet handler
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x + SPACE_SHIP_WIDTH < 0:
            red_bullets.remove(bullet)

def draw_winner(winner_text):
    draw_winner = WINNER_FONT.render(winner_text,1,WHITE)
    WIN.blit(draw_winner,(WIDTH//2 - draw_winner.get_width()//2, HEIGTH//2 - draw_winner.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

# game runner function
def main():
    red = pygame.Rect(700,100,SPACE_SHIP_HEIGHT,SPACE_SHIP_WIDTH)
    yellow = pygame.Rect(100, 300, SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH)

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True

    red_health = 10
    yellow_health = 10

    while run:
        # it will make our game consistant at every computer irrespactive of its speed
        # means this while loop will get executed 60 times in a second
        clock.tick(FPS)

        # event handling
        for event in pygame.event.get():

            # condition to get out of game window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # keydown dont take a key as bieng contineusly pressed it takes 1 input at a time
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + SPACE_SHIP_WIDTH - 20,yellow.y + SPACE_SHIP_HEIGHT // 2 + 6,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + SPACE_SHIP_HEIGHT // 2 + 6, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # taking all the key that are bieng pressed
        keys_pressed = pygame.key.get_pressed()

        # spaceship movement handler call
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed, red)

        # all the stuff needed to control bullets
        handle_bullets(yellow_bullets, red_bullets, yellow, red)


        draw_window(red,yellow,yellow_bullets,red_bullets,yellow_health,red_health)

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red wins...!"

        if red_health <= 0:
            winner_text = "Yellow wins...!"

        if winner_text != "":
            draw_winner(winner_text)  # someone won
            break

    # pygame.quit()          #we will not quit game as any player wins we just restart the game again after 5 seconds
    main()

if __name__ == '__main__':
    # game runner function call
    main()

