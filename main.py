import pygame
import numpy as np
import random

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
        if key == pygame.K_LEFT:
            self.change_coords[0] -= self.SPEED
        if key == pygame.K_RIGHT:
            self.change_coords[0] += self.SPEED
    
    def stop(self, key):
        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.change_coords = [0, 0]
    
    def update(self):
        self.coords = np.add(self.coords, self.change_coords)

    def check_boundary(self):
        if self.coords[0] <= 0:
            self.coords[0] = 0
        
        if self.coords[0] >= 736:
            self.coords[0] = 736

playerImg = pygame.image.load('images/among-us-64.png')
player_coords = [370, 480]
player = Player("Player 1", playerImg, player_coords)

# Enemy
class Impostor(Actor):
    ROW_JUMP = 50
    SIDE_JUMP = 5
    direction = 1
    possible_images = ['images/among-us-imposter-64-1.png', 'images/among-us-imposter-64-2.png', 'images/among-us-imposter-64-3.png']
    STEP_TIME = 60
    FRAME_COUNT = 0
    TURN = 0

    def __init__(self, coords):
        value = random.randint(0, 2)
        image = pygame.image.load(self.possible_images[value])
        Actor.__init__(self, image, coords)

    def move(self):

            if self.TURN == 1:
                self.coords[0] += self.direction * self.SIDE_JUMP  
                self.TURN = 0

            elif self.coords[0] >= 736 or self.coords[0] <= 0:
                self.coords[1] += self.ROW_JUMP
                self.direction *= -1
                self.TURN = 1

            else:
                self.coords[0] += self.direction * self.SIDE_JUMP    
            

def initialise_imposters(NUM_IMPOSTORS, NUM_PER_ROW):
    arr = []
    ROW_SPACE = 70
    START_X = 50
    START_Y = 30

    for i in range(NUM_IMPOSTORS // NUM_PER_ROW):
        space_between = SCREEN_WIDTH / NUM_PER_ROW
        for j in range(NUM_PER_ROW):

            # Get coords
            coords = [START_X + (j * space_between), START_Y + (i * ROW_SPACE)]
            arr.append(Impostor(coords))

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

    if Impostor.FRAME_COUNT == Impostor.STEP_TIME:
        for impostor in impostor_array:
            impostor.move()
        Impostor.FRAME_COUNT = 0
    else:
        Impostor.FRAME_COUNT += 1

    for impostor in impostor_array:
        impostor.draw()

    pygame.display.update()