
# Import Python functions
import math
import numpy as np
import pygame
import random
import cv2
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import pickle
import os


# Import our own functions
from trigfunctions import*
from car import car
from window import Window


class World():
    def __init__(self,game):

        if game.gameMode!='Random':
            filepath='world_files/road_length'+game.gameMode+'.data'
            if os.path.exists(filepath):
                with open('world_files/road_length'+game.gameMode+'.data','rb') as filehandle:
                        width=pickle.load(filehandle)
            else:
                width=300
        else:
            width=random.randint(150,1500)

        self.width_m=width # meters
        self.height_m=24 # meters

        self.width_px=self.width_m*game.pixpermeter
        self.height_px=self.height_m*game.pixpermeter

        self.WorldSize_px=(self.width_px,self.height_px)

        self.window=Window(game, self.WorldSize_px)


        if game.gameMode == 'Random':
            for i in range (5,random.randint(20,45)):
                self.generateRandomObstacle(game)
        
        else:
            self.generateBlueCars(game)

        # self.generateGreenCars(game)
            # self.showWorldMap(game)


        # Create our car
        print("Spawning our car")
        game.orange_car=car(410,408,"protagonist",game)
        
        game.all_sprites.add(game.orange_car)

        print("All cars spawned.")




    def generateBlueCars(self,game):
    # Create stationary cars
        print("Populating Blue cars")

        start_pos_list=[]
        filepath='world_files/car_positions_'+game.gameMode+'.data'
        if os.path.exists(filepath):
            with open('world_files/car_positions_'+game.gameMode+'.data','rb') as filehandle:
                start_pos_list=pickle.load(filehandle)
                # print(start_pos_list)

        for start_pos in start_pos_list:
            x,y=start_pos
            new_obst=car(x,y,"obstacle",game)
            game.obst_list.add(new_obst)
            game.all_sprites.add(new_obst)





    def generateRandomObstacle(self,game):
        print("Randomly poulating blue cars")
        randx=random.randint(250,self.width_px-400)
        lanes=[225,320,405,500]
        randy=random.choice(lanes)
        new_obst=car(randx,randy,"obstacle",game)
        if new_obst.spritex>self.width_px-400:
            new_obst.kill()
        else:
            game.obst_list.add(new_obst)
            game.all_sprites.add(new_obst)

        # return self.obst_list



    def generateGreenCars(self,game):
        # Create dynamic cars
        print("Populating Green cars")
        for i in range (0,random.randint(1,3)):
            # tempcar=car(0,0,"dynamic")
            randx=random.randint(100,900)
            randy=random.randint(50,350)
            # # Eliminate cars on the lane lines
            # if (100-tempcar.car_height<=randy<=100+tempcar.car_height) or (200-tempcar.car_height<=randy<=200+tempcar.car_height) or (300-tempcar.car_height<=randy<=300+tempcar.car_height):
            #     randy=random.randint(50,350)
            greencar=car(randx,randy,"dynamic",game)
            game.active_list.add(greencar)
            game.all_sprites.add(greencar)
        print("Done adding green cars")
        # tempcar.kill()
        # obst_list=[]


    # def moveWindow(self,keys,game):

    #     if keys[pygame.K_LEFT] and self.window.x > self.window.vel: 
    #         self.window.x -= self.window.vel

    #     elif keys[pygame.K_RIGHT] and self.window.x < (self.width_px - self.window.vel - self.window.width_px):
    #         self.window.x += self.window.vel

    #     if keys[pygame.K_DOWN] and self.window.y <(self.height_px-self.window.vel-self.window.height_px):
    #         self.window.y+=self.window.vel

    #     elif keys[pygame.K_UP] and self.window.y > self.window.vel:
    #         self.window.y-=self.window.vel

    #     if keys[pygame.K_a]:
    #         game.orange_car.turnCar(15)

    #     # print(self.window.x,self.window.y)
    #     if not self.window.photoMode:
    #         game.orange_car.x=self.window.x+self.window.width_px//2
    #         game.orange_car.y=self.window.y+self.window.height_px//2
    #         game.orange_car.updateSpriteOrigin()


    def updateWinPos(self,game):
            self.window.x=-self.window.width_px//2+game.orange_car.x
            self.window.y=-self.window.height_px//2+game.orange_car.y


    # def showWorldMap(self,game):
    #     # plt.figure(1)
    #     # plt.subplot(111)
    #     # plt.axis([0, self.width_m, 0, self.height_m])
    #     # matplotlib.axes.Axes.invert_yaxis()
    #     # plt.title("World Map")
    #     # plt.grid()
    #     # # ax.set_aspect('equal')
    #     worldMap=np.full((self.width_px,self.height_px,3),(255,255,255),np.uint8)
    #     # Draw all cars as rectangles
    #     for sprite in game.all_sprites:
    #         worldMap=cv2.rectangle(worldMap,(sprite.spritex,sprite.spritey),(sprite.spritex+sprite.car_width,sprite.spritey+sprite.car_height),sprite.body_color,-1)


    #         # a=Rectangle((sprite.spritex,sprite.spritey),sprite.car_width,sprite.car_height, fc=sprite.body_color, angle=sprite.theta,alpha=.5)
    #         # ax.add_patch(a)
    #     worldMap=cv2.rectangle(worldMap,(self.window.x,self.window.y),(self.window.x+self.window.width_px,self.window.y+self.window.height_px),(0,0,0),3)
    #     # win_box=Rectangle(,self.window.width_m,self.window.height_m,fill=None, ec='black', lw=3, angle=0)
    #     # ax.add_patch(win_box)

    #     worldMap=cv2.resize(worldMap,(1000,400))
    #     cv2.imshow("World Map",worldMap)
    #     cv2.waitKey(0)

    #     # fullWorld.show()

    #     # viewWindow=plt.figure(2)
    #     # plt.title("Window View")
    #     # fig2, ax2 = plt.subplots(1)
    #     # ax2.set_xlim(0,self.window.width_m)
    #     # ax2.set_ylim(0,self.window.height_m)
    #     # ax2.invert_yaxis()
    #     # ax2.grid()
    #     # ax2.set_xlabel('meters')
    #     # ax2.set_ylabel('meters')

    #     # # ax2.set_aspect('equal')
    #     # viewWindow.show()


    #     # plt.show()





    


