import pygame
import os
pygame.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shooting Game!')

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)

PARTITION_BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets/hit_sound.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gun_sound.mp3'))

HEALTH_FONT = pygame.font.SysFont('Trebuchet MS',30)
WINNER_FONT = pygame.font.SysFont('Trebuchet MS', 80)
WINNER_TEXT_BLOCK = pygame.Rect(0,HEIGHT//2 - 85,WIDTH,170)

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,45
VEL = 5
BULLET_VEL = 12
MAX_BULLETS = 4

YELLOW_HIT = pygame.USEREVENT + 0
RED_HIT = pygame.USEREVENT + 1

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/space.jpg')), (WIDTH,HEIGHT))

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, PARTITION_BORDER)

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), True, YELLOW)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), True, RED)
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #yellow_left
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < PARTITION_BORDER.x : #yellow_right
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #yellow_up
            yellow.y -= VEL    
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGHT - 5: #yellow_down
            yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > PARTITION_BORDER.x + PARTITION_BORDER.width + 10: #red_left
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VEL < WIDTH + 10: #red_right
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0 : #red_up
            red.y -= VEL    
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT - 9 : #red_down
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow,red):
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
        elif bullet.x < 0:
            red_bullets.remove(bullet)   

def draw_winner(text):
    pygame.draw.rect(WIN, BLACK, WINNER_TEXT_BLOCK)
    draw_text = WINNER_FONT.render(text, True, GREEN)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(4000)


def main():
    yellow = pygame.Rect(30, HEIGHT/2 - YELLOW_SPACESHIP.get_height()/2 ,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red = pygame.Rect(WIDTH - RED_SPACESHIP.get_width() - 30,HEIGHT/2 - RED_SPACESHIP.get_height()/2,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 5
    red_health = 5

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RETURN and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break                

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
        

    main()

if __name__ == '__main__':
    main()
