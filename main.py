import pygame
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Initiliase the pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title, Icon
pygame.display.set_caption("Amogus Space Invaders")
icon = pygame.image.load(r'images/spaceship.png')
pygame.display.set_icon(icon)

class Actor:
    def __init__(self, image, coords):
        self.image = image
        self.coords = coords
    
    def draw(self):
        screen.blit(self.image, (self.coords[0], self.coords[1]))

# Player Class
class Player(Actor):
    name = ""
    change_coords = [0, 0]
    SPEED = 1
    def __init__(self, name, image, coords):
        self.name = name
        Actor.__init__(self, image, coords)
    
    def move(self, key):
        if key == pygame.K_UP:
            self.change_coords[1] -= self.SPEED
        if key == pygame.K_DOWN:
            self.change_coords[1] += self.SPEED
        if key == pygame.K_LEFT:
            self.change_coords[0] -= self.SPEED
        if key == pygame.K_RIGHT:
            self.change_coords[0] += self.SPEED
    
    def stop(self, key):
        if key == pygame.K_DOWN or key == pygame.K_UP or key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.change_coords = [0, 0]
    
    def update(self):
        self.coords = np.add(self.coords, self.change_coords)

    def check_boundary(self):
        if self.coords[0] <= 0:
            self.coords[0] = 0
        
        if self.coords[0] >= 736:
            self.coords[0] = 736
        
        if self.coords[1] <= 0:
            self.coords[1] = 0
        
        if self.coords[1] >= 540:
            self.coords[1] = 540

playerImg = pygame.image.load('images/among-us-64.png')
player_coords = [370, 480]
player = Player("Player 1", playerImg, player_coords)

# Enemy
class Impostor(Actor):
    possible_images = ['images/among-us-imposter-64-1.png', 'images/among-us-imposter-64-2.png', 'images/among-us-imposter-64-3.png']

    def __init__(self, image, coords):
        Actor.__init__(self, image, coords)

    def move():
        return 0

def initialise_imposters(NUM_IMPOSTORS, NUM_ROW):
    arr = []

    for i in range(NUM_IMPOSTORS):
        space_between = SCREEN_WIDTH / NUM_ROW
        

    return arr

impostor_array = initialise_imposters(20, 5) # 20 Impostors, 5 on each row

running = True
while running:

    # RGB
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            player.move(event.key)
        
        if event.type == pygame.KEYUP:
            player.stop(event.key)
    
    player.check_boundary()
    player.update()
    player.draw()


    pygame.display.update()