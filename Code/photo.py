# Import Python functions
import pygame
import pickle
from time import time
import math
import random
import sys

# Import our own functions
sys.path.append('Game/')
sys.path.append('MotionPlanning/')
from car import car
from window import Window
from world import World
from game import car_game
import statespace
import motionplanner

difficulty = "Easy" #Easy, Medium, Hard, Extreme, Random


print("Starting game")
game=car_game(difficulty) # Instantiate game

print("Generating world")
world=World(game) # Generate world

# Set window width and height to match the world
world.window.width_px=world.WorldSize_px[0]
world.window.height_px=world.WorldSize_px[1]
world.window.win = pygame.display.set_mode((world.window.width_px, world.window.height_px))

# Start the window at the top left corner
world.window.x=0
world.window.y=0

# Put the orange car in the right spot
game.orange_car.spritex=410-game.orange_car.car_width_px/2
game.orange_car.spritey=375

# Draw the window and then save it
world.window.redrawGameWindow(game,world.WorldSize_px)
path='world_files/'+game.gameMode+'.png'
pygame.image.save(world.window.win,path)
print("Image saved to '"+path+"'")

pygame.quit()
