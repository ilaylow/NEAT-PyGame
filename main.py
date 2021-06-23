import pygame
import numpy as np
import random

from Player import Player
from Impostor import Impostor

from pygame import mixer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

background = pygame.image.load(r"images/background_spaceship_resized.png")

# Initiliase the pygame
pygame.init()

# Use clock
clock = pygame.time.Clock()

# Font Used
font = pygame.font.Font("freesansbold.ttf", 26)

death_font = pygame.font.Font("freesansbold.ttf", 36)

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
destroy_sound.set_volume(0.2)

death_sound = mixer.Sound(r"sounds/player_death.wav")
death_sound.set_volume(0.2)

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

    for i in range(NUM_IMPOSTORS // NUM_PER_ROW):
        space_between = SCREEN_WIDTH / NUM_PER_ROW
        for j in range(NUM_PER_ROW):

            # Get coords
            coords = [Impostor.START_X + (j * space_between), Impostor.START_Y + (i * Impostor.ROW_SPACE)]
            arr.append(Impostor(coords))

    return arr

def spawn_random_impostor(NUM_IMPOSTORS, NUM_PER_ROW, impostor_arr):
    space_between = SCREEN_WIDTH / NUM_PER_ROW

    i = random.randint(0, NUM_IMPOSTORS // NUM_PER_ROW - 1)
    j = random.randint(0, NUM_PER_ROW - 1)

    coords = [Impostor.START_X + (j * space_between), Impostor.START_Y + (i * Impostor.ROW_SPACE)]

    impostor_arr.append(Impostor(coords))

    return impostor_arr

NUM_IMPOSTORS = 20
NUM_ROWS = 5
impostor_array = initialise_imposters(NUM_IMPOSTORS, NUM_ROWS) # 20 Impostors, 5 on each row

# Each time we hit 10000, we increase the speed and rate at which the impostors move and spawn
DIFFICULTY_LEVEL = 1
DIFFICULTY_CONTROL_TIME = 10000
FRAME_COUNT = 0

def display_difficulty():
    string_difficulty = font.render("Difficulty Level: " + str(DIFFICULTY_LEVEL), True, [255, 255, 255])
    screen.blit(string_difficulty, (150, 10))

def show_death_screen():
    string_death = death_font.render("Game Over... ", True, [255, 255, 255])
    screen.blit(string_death, (100, 100))

# Want to create infinite generation of enemies to try to maximise score before getting killed by imposters
# So an infinite level space invaders among us
while True:

    # RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    if player.alive == False:
        impostor_array = []
        Impostor.bullets = []
        Impostor.SPAWN = False
        show_death_screen()

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
    
    # Imposter Fire Enemy Bullets
    if Impostor.SHOOT_FRAME == Impostor.SHOOT_TIMER:
        Impostor.SHOOT_FRAME = 0
        if len(impostor_array) != 0:
            rand_imp = impostor_array[random.randint(0, len(impostor_array) - 1)]
            rand_imp.fire_bullet()
    else:
        Impostor.SHOOT_FRAME += 1

    # Fire Bullets Across Screen
    for bullet in player.bullets:
        bullet.fire()
        bullet.draw(screen)
    
    bulletCount = len(Impostor.bullets) - 1
    while bulletCount >= 0:
        if Impostor.bullets[bulletCount].coords[1] >= 600:
            Impostor.bullets.pop(bulletCount)
        else:
            Impostor.bullets[bulletCount].fire()
            Impostor.bullets[bulletCount].draw(screen)

        bulletCount -= 1

    # Check for collision between bullets between impostors
    player.check_hit_enemy(impostor_array)

    # Difficulty Update Across Time
    if FRAME_COUNT == DIFFICULTY_CONTROL_TIME:
        DIFFICULTY_LEVEL += 1
        Impostor.SPAWN_LOWER = round(Impostor.SPAWN_LOWER * 0.9)
        Impostor.SPAWN_HIGHER = round(Impostor.SPAWN_HIGHER * 0.9)
        Impostor.STEP_TIME = round(Impostor.STEP_TIME * 0.9)
        Impostor.ROW_JUMP = round(Impostor.ROW_JUMP * 1.1)
        Impostor.SHOOT_TIMER = round(Impostor.SHOOT_TIMER * 0.9)
        Impostor.SHOOT_FRAME = 0
        Impostor.FRAME_COUNT = 0
        FRAME_COUNT = 0
    else:
        FRAME_COUNT += 1

    # Spawn Update
    if Impostor.SPAWN_COUNT == Impostor.SPAWN_TIME and Impostor.SPAWN:
        impostor_array = spawn_random_impostor(NUM_IMPOSTORS, NUM_ROWS, impostor_array)
        Impostor.SPAWN_COUNT = 0
        Impostor.SPAWN_TIME = random.randint(Impostor.SPAWN_LOWER, Impostor.SPAWN_HIGHER)
    else:
        Impostor.SPAWN_COUNT += 1

    # Impostor Movement
    if Impostor.FRAME_COUNT == Impostor.STEP_TIME:
        for impostor in impostor_array:
            impostor.move()
        Impostor.FRAME_COUNT = 0
    else:
        Impostor.FRAME_COUNT += 1

    # Draw Impostor
    for impostor in impostor_array:
        impostor.draw(screen)

    # Display Scores and Difficulty
    display_score(player)
    display_difficulty()

    if player.check_death(impostor_array, Impostor.bullets):
        mixer.music.stop()
        death_sound.play()
        pygame.time.delay(3000)
        player.alive = False

    clock.tick(500)
    pygame.display.update()

