#libraries
import pygame
import random

#initailise pygame
pygame.init()

#game window dimensions
screen_width = 400
screen_height = 600

#create game window
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Jumpy but upgrade')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game veriables
gravity = 1
max_platform = 10


#define color
white = (255, 255, 255)


#load image
jumpy_image = pygame.image.load('D:/kmitl/file python/Project/test/assets/jumpy.png').convert_alpha()
bg_image = pygame.image.load('D:/kmitl/file python/Project/test/assets/bg-01.png').convert_alpha()
platform_image = pygame.image.load('D:/kmitl/file python/Project/test/assets/plate.png').convert_alpha()


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
        #reset variables
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -5
            self.flip = True
        if key[pygame.K_d]:
            dx = 5
            self.flip = False

        #gravity
        self.vel_y += gravity
        dy += self.vel_y


        #encure player doesnt go off the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right


        #check collision with platform
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -21
                    

        #chack collision with ground
        if self.rect.bottom + dy > screen_height:
            dy = 0
            self.vel_y = -21

        #update position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 7, self.rect.y - 5))
        pygame. draw.rect(screen, white, self.rect, 2)

#Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



#player instance
jumpy = Player(screen_width // 2, screen_height - 150)

#create sprte groups
platform_group = pygame.sprite.Group()

#create temporary plateform
for p in range(max_platform):
    p_w = random.randint(60, 60)
    p_x = random.randint(0, screen_width - p_w)
    p_y = p * random.randint(80, 120)
    platform = Platform(p_x, p_y, p_w)
    platform_group.add(platform)


#game loop
run = 1
while run:

    clock.tick(FPS)

    jumpy.move()

    #draw background
    screen.blit(bg_image, (0, 0))
    
    #draw spirtes
    platform_group.draw(screen)
    jumpy.draw()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0

    #update display window
    pygame.display.update()

pygame.quit()
