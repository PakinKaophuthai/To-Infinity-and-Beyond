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
scroll_thresh = 200 #pixels
gravity = 1
max_platform = 10
scroll = 0
bg_scroll = 0

#define color
white = (255, 255, 255)

#load image
jumpy_image = pygame.image.load('D:/kmitl/file python/Project/test/assets1/asstor.png').convert_alpha()
bg_image = pygame.image.load('D:/kmitl/file python/Project/test/assets1/bgspce.png').convert_alpha()
platform_image = pygame.image.load('D:/kmitl/file python/Project/test/assets1/platformUFO.png').convert_alpha()

#fuction for drawing bg
def drawing_bg(scroll):
    screen.blit(bg_image, (0, 0 + scroll))
    screen.blit(bg_image, (0, -600 + scroll))
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
        scroll = 0
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
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

        #check if the player has bounced to the top of the sreen
        if self.rect.top <= scroll_thresh:
            #if players is jumping
            if self.vel_y < 0:
                scroll = -dy

        
        #update position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

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

    def update(self, scroll):

        #update platfrom's v position
        self.rect.y += scroll

        #check if platform has gone off the screen
        if self.rect.top > screen_height:
            self.kill()

#player instance
jumpy = Player(screen_width // 2, screen_height - 150)

#create sprte groups
platform_group = pygame.sprite.Group()


#create starting platform
platform = Platform(screen_width // 2 - 50, screen_height - 50, 100)
platform_group.add(platform)


#game loop
run = 1
while run:

    clock.tick(FPS)

    scroll = jumpy.move()

    #draw background
    bg_scroll += scroll
    if bg_scroll >= 600:
        bg_scroll = 0
    drawing_bg(bg_scroll)
    
    
    #generate platform
    if len(platform_group) < max_platform:
        p_w = random.randint(40,60)
        p_x = random.randint(0,screen_width - p_w)
        p_y = platform.rect.y - random.randint(80, 120)
        platform = Platform(p_x, p_y, p_w)
        platform_group.add(platform)
        
    #update platfrom
    platform_group.update(scroll)
    
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
