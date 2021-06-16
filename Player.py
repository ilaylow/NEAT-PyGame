from Actor import Actor
from Bullet import Bullet
import pygame
import numpy as np
import math

# Player Class
class Player(Actor):
    bullets = []
    name = ""
    change_coords = [0, 0]
    score = 0
    SPEED = 1

    def __init__(self, name, image, coords, sound):
        self.name = name
        self.destroy_sound = sound
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
    
    def fire_bullet(self):
        bullet = Bullet(self.coords)
        self.bullets.append(bullet)
    
    def check_hit_enemy(self, impostors):
        bullets_len = len(self.bullets) - 1
        while bullets_len >= 0:
            if self.bullets[bullets_len].hasCollide(impostors):
                self.destroy_sound.play()
                self.bullets.pop(bullets_len)
                self.score += 1
            
            elif self.bullets[bullets_len].coords[1] <= 0:
                self.bullets.pop(bullets_len)

            bullets_len -= 1
    
    def check_death(self, impostors):
        for impostor in impostors:
            if math.dist(self.coords, impostor.coords) < 20:
                return True