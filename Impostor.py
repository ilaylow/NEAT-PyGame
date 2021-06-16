from Actor import Actor
import pygame
import random

# Enemy Class
class Impostor(Actor):
    ROW_JUMP = 50
    SIDE_JUMP = 5
    direction = 1
    possible_images = ['images/among-us-imposter-64-1.png', 'images/among-us-imposter-64-2.png', 'images/among-us-imposter-64-3.png']
    STEP_TIME = 10
    FRAME_COUNT = 0
    TURN = 0

    def __init__(self, coords):
        value = random.randint(0, 2)
        image = pygame.image.load(self.possible_images[value])
        Actor.__init__(self, image, coords)

    def move(self):

        # Want to add random behaviour to the imposters behaviour

            if self.TURN == 1:
                self.coords[0] += self.direction * self.SIDE_JUMP  
                self.TURN = 0

            elif self.coords[0] >= 736 or self.coords[0] <= 0:
                self.coords[1] += self.ROW_JUMP
                self.direction *= -1
                self.TURN = 1

            else:
                self.coords[0] += self.direction * self.SIDE_JUMP    
            
