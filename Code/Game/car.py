# Import Python functions
import math
import numpy as np
import pygame
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

# Import our own functions
from trigfunctions import*

class car(pygame.sprite.Sprite):
    def __init__(self,x,y,car_type,game):
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()

        # Start position of car origin
        self.x=x # start position
        self.y=y # start position
        self.theta=0


        # Physical car dimensions (meters)
        self.car_width = 4
        self.car_height = 1.8
        self.wheel_radius = .46
        


        # Car sprite dimensions
        self.car_width_px=int(self.car_width*game.pixpermeter) # total width of car (for bounding box)
        self.car_height_px=int(.6*self.car_width_px) # total height of car (for b


        self.dt=.1 # seconds

        # Start position of the sprite origin
        self.updateSpriteOrigin()


        if car_type == "protagonist":
            self.car_image = pygame.image.load('../assets/orange_car.png')
            self.body_color=(0,153,255,1)
            self.stationary=False
            self.vel=2 #m/s
            self.wheel_speed = self.vel/self.wheel_radius # rad/s


        if car_type == "obstacle":
            # car does not move
            self.car_image = pygame.image.load('../assets/blue_car.png')
            self.body_color=(255,0,0,1)
            self.stationary=True

        if car_type == "dynamic":
            # car moves by itself
            self.car_image = pygame.image.load('../assets/green_car.png')
            self.body_color=(0,255,0,1)
            self.stationary=False
            self.vel=random.randint(1,6)

        self.car_image = pygame.transform.scale(self.car_image, (self.car_width_px, self.car_height_px))
        self.car_image_new=self.car_image
        self.rect = self.car_image.get_rect()
        # self.rect.x = x
        # self.rect.y = y

        if not self.stationary:
            # Front wheel drive car utlizing Ackermann Steering
            # http://ckw.phys.ncku.edu.tw/public/pub/Notes/GeneralPhysics/Powerpoint/Extra/05/11_0_0_Steering_Theroy.pdf
            self.l=self.car_width # length between front and rear wheel axes (wheelbase)
            self.a2=self.l/2 # distance from the back axel to the center of mass of the car
            self.W=self.car_height # distance between the left and right wheels


    def updateSpriteOrigin(self):
        self.spritex=self.x-self.car_width_px//2
        self.spritey=self.y-self.car_height_px//2

    def updateCarOrigin(self):
        self.x=self.spritex+self.car_width_px//2
        self.y=self.spritey+self.car_height_px//2


        #things to know about a node
        # Constants we know: l, a2, wheel speed, wheel radius
        # starting x, y, theta, vx, vy, wheel angle
        # after a dt, want to know new x,y,theta, vx,vy
        # need to find initial position of center of rotation (COR)
            # Find R
            # Use R, theta, x, y to find COR in world frame
            # Use R, a2 to find R1
        # Use R1, wheel speed, wheel radius to compute angular velocity around COR (Av)


    def turnCar(self,wheel_angle,game):
        # print("Turning")
        if wheel_angle != 0:
            R=math.sqrt(self.a2**2+self.l**2*cotd(wheel_angle)**2)

            alpha=math.asin(self.a2/R)

            R1=R*math.cos(alpha)

            ang_vel=self.wheel_radius*self.wheel_speed/(R1+self.W/2)
            if wheel_angle<0:
                ang_vel*=-1

            dtheta=np.rad2deg(ang_vel*self.dt)


            B=(180-abs(dtheta))/2-np.rad2deg(alpha)

            L=abs(2*R*sind(abs(dtheta)/2))

            # Change in position of car in car frame (x,y)
            d_c=(L*sind(B)*self.dt, L*cosd(B)*self.dt)

            deltax_m=d_c[0]*cosd(self.theta)+self.vel*cosd(self.theta)*self.dt+d_c[1]*cosd(self.theta)#+(COR_f[0]-COR_i[0])
            deltay_m=d_c[1]*sind(self.theta)+self.vel*sind(self.theta)*self.dt+d_c[0]*sind(self.theta)#+(COR_f[1]-COR_i[1])

            self.theta+=dtheta

        else:
            deltax_m=self.vel*cosd(self.theta)*self.dt
            deltay_m=self.vel*sind(self.theta)*self.dt
            # print(deltax_m)
        
        self.x+=deltax_m*game.pixpermeter
        self.y-=deltay_m*game.pixpermeter

        theta = self.theta % 360

        self.updateSpriteOrigin()
        self.car_image_new = pygame.transform.rotate(self.car_image, theta)






    def moveCar(self,world,game):

        self.spritex+=self.vel*cosd(self.theta)
        self.spritey-=self.vel*sind(self.theta)
        self.updateCarOrigin()
        world.updateWinPos(game)
    
    
    # def laneChange(self,direction):
    #     self.turnCar(15)
        



if __name__ == '__main__':
    test_car=car(50,0,"protagonist")
    right_car=car(50,0,"protagonist")
    a=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,alpha=.5)
    # b=Rectangle((right_car.x,right_car.y),right_car.car_width,right_car.car_height, angle=right_car.theta,alpha=.5,color='purple')

    fig, ax = plt.subplots(1)
    ax.add_patch(a)
    # ax.add_patch(b)


    for i in range(10):
        test_car.turnCar(15)
        b=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,color="red",alpha=1)
        ax.add_patch(b)

    for i in range(20):
        test_car.turnCar(-15)
        b=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,color="green",alpha=1)
        ax.add_patch(b)

    for i in range(10):
        test_car.turnCar(15)
        b=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,color="red",alpha=1)
        ax.add_patch(b)

    # ax.set_aspect('equal', 'box')
    ax.set_xlim(0,1250)
    ax.set_ylim(-20,180)
    ax.grid()
    plt.show()



