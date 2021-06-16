import pygame
import numpy as np
import random
import math

from Player import Player
from Impostor import Impostor

from pygame import mixer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

background = pygame.image.load(r"images/background_spaceship_resized.png")

# Initiliase the pygame
pygame.init()

# Font Used
font = pygame.font.Font("freesansbold.ttf", 26)

""" # Death Screen Movie
death_movie = pygame.movie.Movie("insert-name.mpg")
sur_obj=pygame.display.set_mode(death_movie.get_size())
mov_scre=pygame.Surface(death_movie.get_size()).convert() """

# Load the background music
mixer.music.load(r"sounds/background.wav")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Load the destroy sound
destroy_sound = mixer.Sound(r"sounds/destroy_impostor.wav")
death_sound = mixer.Sound(r"sounds/player_death.wav")

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title, Icon
pygame.display.set_caption("Amogus Space Invaders")
icon = pygame.image.load(r'images/spaceship.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('images/among-us-64.png')
player_coords = [370, 480]
player = Player("Player 1", playerImg, player_coords, destroy_sound)

def display_score(player):
    string_score = font.render("Score: " + str(player.score), True, [255, 255, 255])
    screen.blit(string_score, (10, 10))

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

# Want to create infinite generation of enemies to try to maximise score before getting killed by imposters
# So an infinite level space invaders among us
while True:

    # RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire_bullet()
            else:
                player.move(event.key)
        
        if event.type == pygame.KEYUP:
            player.stop(event.key)
    
    player.check_boundary()
    player.update()
    player.draw(screen)
    
    for bullet in player.bullets:
        bullet.fire()
        bullet.draw(screen)

    player.check_hit_enemy(impostor_array)

    if Impostor.FRAME_COUNT == Impostor.STEP_TIME:
        for impostor in impostor_array:
            impostor.move()
        Impostor.FRAME_COUNT = 0
    else:
        Impostor.FRAME_COUNT += 1

    for impostor in impostor_array:
        impostor.draw(screen)

    display_score(player)

    if player.check_death(impostor_array):
        death_sound.play()
        pygame.time.delay(5000)
        pygame.quit()
        quit()

    pygame.display.update()

