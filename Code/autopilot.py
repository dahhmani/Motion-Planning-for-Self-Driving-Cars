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

def main():
    difficulty="Easy" #Easy, Medium, Hard, Extreme, Random

    # Launch Game
    print("Starting game")
    game=car_game(difficulty) # Instantiate game
    print("Generating world")
    world=World(game) # Generate world

    # Generate Motion Plan
    print("Generating roadmap for solver")
    Map = statespace.RoadMap(game, world)
    print("Attempting to solve")
    planner = motionplanner.SamplingPlanner(Map)
    t0 = time()
    solved, plan, exploredNodes, _ = planner.RRT()
    t1 = time() 
    if solved: 
        print(f'Path found in {t1-t0} s\n')
    else:
        print('Path not found')
    planner.simulation(plan, exploredNodes)
    actions = motionplanner.actionPlanner_SDC(Map, plan)

    # Run Game in Autopilot Mode
    runGame(game, world, actions)
    
    pygame.quit()

def runGame(game, world, actions):
    busy = False
    ready_for_next_action = True
    angle = 0
    turn_increment = 15
    count, start_count =0, 0

    while game.run:
        game.clock.tick(100)
        count+=1

        # Update green cars
        for active_car in game.active_list:
            active_car.spritex+=active_car.vel
            active_car.updateCarOrigin()

        # Get new events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False

        keys = pygame.key.get_pressed()

        # t = pygame.time.get_ticks()

        if ready_for_next_action:
            if actions:
                action,position = actions.pop(0)
                ready_for_next_action = False

                if action == 'L':
                    angle = turn_increment
                    lane_change_count = 33
                elif action == 'R':
                    angle = -turn_increment
                    lane_change_count = 33

        if game.orange_car.x + 3*game.orange_car.car_width_px < position:
            game.orange_car.turnCar(0,game)
            start_count = count
        else:
            if count-start_count<=lane_change_count:
                game.orange_car.turnCar(angle,game)  
            elif game.orange_car.theta*(angle/abs(angle)) > 0:
                game.orange_car.turnCar(-angle,game)
            else:
                game.orange_car.theta = 0
                ready_for_next_action = True

        world.updateWinPos(game)
        world.window.redrawGameWindow(game,world.WorldSize_px)
            
        if keys[pygame.K_q]:
            pygame.quit()
            game.run=False

if __name__ == '__main__':
    main()