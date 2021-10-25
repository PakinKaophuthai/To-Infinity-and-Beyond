import pygame
import random

#initailise pygame
pygame.init()

#game window
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game variablaes
GRAVITY = 1
MAX_PLATFORM = 10
SCROLL_THRESH = 200
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (255, 153, 51)

#define font
font_small = pygame.font.SysFont('Lucida Sans',20)
font_big = pygame.font.SysFont('Lucida Sans',24)

#load image
jumpy_image = pygame.image.load('D:/kmitl/file python/Project/test/assets1/jumpy.png').convert_alpha()
bg_image = pygame.image.load('D:/kmitl/file python/Project/test/assets1/bg-01.png').convert_alpha()
platform_image = pygame.image.load('D:/kmitl/file python/Project/test/assets1/plate.png').convert_alpha()

#function text on screen
def draw_text(text, font, text_col, x, y):
    img  = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_HEIGHT, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDHT, 30), 2)
    
    draw_text("SCORE: " + str(score), font_small, WHITE, 0, 0)

#function for draw bg
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))

#player class
class Player():

    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):

        #reset variable
        scroll = 0
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx -= 10
            self.flip = True
        if key[pygame.K_d]:
            dx += 10
            self.flip = False

        #geavity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensure player doesnt go out screen
        if self.rect.left + dx < 0:
            dx =  - self.rect.left
        if self.rect.right + dx > SCREEN_WIDHT:
            dx = SCREEN_WIDHT - self.rect.right

        #check platform
        for platform in platform_group:
            #collistom in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        #check player bounced to top screen
        if self.rect.top < SCROLL_THRESH:
            #if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        screen.blit(  pygame.transform.flip(self.image, self.flip, False), (self.rect.x-12, self.rect.y-5))
        pygame.draw.rect(screen, WHITE, self.rect, 2) 

#platfrom class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width + 10, 30))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #moving platform side to side if it's a moving platform
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction

        #change platform direction if it has moved fully or hit a wall
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDHT:
            self.direction *= -1
            self.move_counter = 0


        #update platform vertical
        self.rect.y += scroll

        #check if platform gone of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#player instance
jumpy = Player(SCREEN_WIDHT // 2, SCREEN_HEIGHT - 150)

#create sprite group
platform_group = pygame.sprite.Group()

#create starting platform
platform = Platform(SCREEN_WIDHT // 2 - 50, SCREEN_HEIGHT - 30, 100, False)
platform_group.add(platform)

#game loop
run = True
while run:

    clock.tick(FPS)

    if game_over == False:
        scroll = jumpy.move()

        #draw baclground
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        #generate platforms
        if len(platform_group) < MAX_PLATFORM:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDHT - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            if p_type == 1 and score >= 500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)

        #update platform
        platform_group.update(scroll)

        #update score
        if scroll > 0:
            score += scroll

        #draw sprites
        platform_group.draw(screen)
        jumpy.draw()

        #draw panel
        draw_panel()

        #check game over
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True

    else:
        if fade_counter < SCREEN_WIDHT:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDHT - fade_counter, (y + 1) * 100, SCREEN_WIDHT, 100))
        draw_text('GAME OVER', font_big, WHITE, 130, 200)
        draw_text('SCORE:' + str(score), font_small, WHITE, 120, 250)
        draw_text('PRESS SPACE TO PLAY AGAIN',font_small, WHITE, 40, 400)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:

            #reset variable
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0

            #repositon jumpy
            jumpy.rect.center = (SCREEN_WIDHT // 2, SCREEN_HEIGHT - 150)

            #reset platforms
            platform_group.empty()
            platform = Platform(SCREEN_WIDHT // 2 - 50, SCREEN_HEIGHT - 30, 100, False)
            platform_group.add(platform)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display window
    pygame.display.update()

pygame.quit()