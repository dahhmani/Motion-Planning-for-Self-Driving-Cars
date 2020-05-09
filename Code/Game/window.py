
# Import Python functions
import math
import numpy as np
import pygame
import random
import pickle


# Import our own functions
from trigfunctions import*
from car import car

class Window():
    def __init__(self,game,WorldSize_px):
        pygame.init()
        # Fixed width and height which do not ever change
        self.width_m=30 # meters
        self.height_m=13 # meters


        self.width_px=self.width_m*game.pixpermeter
        self.height_px=self.height_m*game.pixpermeter
        self.win = pygame.display.set_mode((self.width_px, self.height_px))


        # Position of the upper left corner of the viewing window, in world coordinates (pix); Moves with the orange car        
        self.x=0
        self.y=120
        self.vel=10

        self.lane_width=90 # px


        # Import assets
        self.lane_line = pygame.image.load('../assets/lane_line_long.png')
        self.solid_line = pygame.image.load('../assets/solid_line.png')
        self.grass = pygame.image.load('../assets/grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (self.lane_width,self.lane_width))
 
        self.finish = pygame.image.load('../assets/finish_line2.png')
        self.finish_line=WorldSize_px[0]-1.5*self.finish.get_width() # x pos of the center of the finish line
        self.start_line=pygame.image.load('../assets/start_line.png')


    


    def redrawGameWindow(self,game,WorldSize_px):
        # Redraw background
        self.win.fill((56,56,59))

        self.lane_count=4
        
        # Redraw shoulder lines
        shoulder_count=WorldSize_px[0]//self.solid_line.get_width()+1

        self.top_shoulder_pos_y=2*self.lane_width-self.y
        top_shoulder_pos_x=0
        self.bot_shoulder_pos_y=WorldSize_px[1]-2*self.lane_width-self.y
        bot_shoulder_pos_x=0
        
            # Top shoulder
        if self.top_shoulder_pos_y<=self.y+self.height_px:
            self.win.blit(self.solid_line,(top_shoulder_pos_x,self.top_shoulder_pos_y))
            for i in range(shoulder_count):
                # Top shoulder
                top_shoulder_pos_x=i*self.solid_line.get_width()-self.x
                if top_shoulder_pos_x<self.x+self.width_px:
                    self.win.blit(self.solid_line,(top_shoulder_pos_x,self.top_shoulder_pos_y))

            # Bottom shoulder
        
        if self.bot_shoulder_pos_y<=self.y+self.height_px:
            self.win.blit(self.solid_line,(bot_shoulder_pos_x,self.bot_shoulder_pos_y))
            for i in range(shoulder_count):
                bot_shoulder_pos_x=i*self.solid_line.get_width()-self.x
                if bot_shoulder_pos_x<self.x+self.width_px:
                    self.win.blit(self.solid_line,(bot_shoulder_pos_x,self.bot_shoulder_pos_y))
                
            
        # Redraw lane lines
        lane_art_count=WorldSize_px[0]//self.lane_line.get_width()+1
        self.lane_pos_y=[]
        for i in range(self.lane_count-1):
            self.lane_pos_y.append(i*self.lane_width-self.y+3*self.lane_width)
            # only draw the lines that would be visible (for speed)
            if self.lane_pos_y[i]<=self.y+self.height_px:
                self.win.blit(self.lane_line,(0-self.x,self.lane_pos_y[i]))

                for j in range(lane_art_count):
                    lane_pos_x=j*self.lane_line.get_width()-self.x
                    # if lane_pos_x<self.x+self.width_px:
                    self.win.blit(self.lane_line,(lane_pos_x,self.lane_pos_y[i]))
                


        # Draw grass past shoulder (top)
        grass_count=WorldSize_px[0]//self.grass.get_width()

        if self.y<self.grass.get_height():
            # self.win.blit(self.grass,(0,0-self.y))
            
            for i in range(grass_count):
                grass_pos=i*self.grass.get_width()
                if grass_pos<self.x+self.width_px:
                    self.win.blit(self.grass,(grass_pos-self.x,0-self.y))


        # Draw grass past shoulder (bottom)
        if self.y+self.height_px>WorldSize_px[1]-self.grass.get_height():
            # self.win.blit(self.grass,(0,WorldSize_px[1]-self.grass.get_height()-self.y))

            for i in range(grass_count):
                grass_pos=i*self.grass.get_width()
                if grass_pos<self.x+self.width_px:
                    self.win.blit(self.grass,(grass_pos-self.x,WorldSize_px[1]-self.grass.get_height()-self.y))


        # Draw finish line
        if self.x+self.width_px>self.finish_line-.5*self.finish.get_width():
            # print("finish")
            self.win.blit(self.finish,(self.finish_line-.5*self.finish.get_width()-self.x,-self.y))

        # Draw start line
        # if self.x+self.width_px>self.finish_line-.5*self.finish.get_width():
            # print("finish")
        self.win.blit(self.start_line,(410+game.orange_car.car_width_px/2-self.x,-self.y))



        # Redraw all cars
        for sprite in game.all_sprites:
            # only blit items on screen
                # car is to the left of the window                car is to the right of the window         car is above window             car is below window
            if (sprite.spritex+sprite.car_width_px<self.x) or (sprite.spritex>self.x+self.width_px) or (sprite.spritey+sprite.car_height_px<self.y) or (sprite.spritey>self.y+self.height_px):
                pass
            else:
                self.win.blit(sprite.car_image_new,(int(sprite.spritex-self.x),int(sprite.spritey-self.y)))


        pygame.display.update()






    


