# Motion Planner for Self-Driving Cars    			             
This project implements RRT motion planning for a car (non-holonomic robot) with steering as the only control input.  
A\*, Dijkstra, BFS and DFS planners are also supported.

<p align="center">
  <img src="https://github.com/dahhmani/Motion-Planning-for-Self-Driving-Cars/blob/master/demo/demo.gif?raw=true">
</p>

## How to Run
Clone this entire repository. Make sure the directory you clone it to is one you have write access to, as several files are created while the program runs. Open Terminal and navigate to the Code directory. Type `python autopilot.py`. If you have additional versions of Python installed, you may need to type `python3 autopilot.py` instead. 

The program will solve a path from the start to goal. A matplotlib based visualization will appear, showing you the obstacles as blue blocks and the explored nodes in light blue. When that concludes, the Pygame visualization will launch, showing you the car driving from start to finish. 

## Dependencies
    numpy
    pickle
    pygame
    random
    matplotlib
    collections
    heapq
    time
    os
    math
    Python 3.8


## Difficulty Modes
The program has several difficulty modes, which can be selected by changing the value of `gameMode` in `game.py`. At this time, only Easy mode has been fully tested. The harder worlds were built before non-holonomic motion was incorporated, and may therefore only be solveable with a holonomic vehicle. 



### Easy
Easy mode features a length of road and a handful of obstacles. The image below was split onto two lines for easier viewing. 

![Easy Mode](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/course_split2.png)



### Medium

![Medium Mode](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/Medium1.png)



### Hard

![Hard Mode](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/Hard1.png)


### Random

The other modes have the blue cars in carefully handpicked locations, placed for the right combination of difficulty and feasibility. They were all designed to be solvable, with at least one valid path. There is also a random mode, which generates a random number of blue cars in random locations on a road of random length. There is no check for or guarantee that the produced world will be solvable, but you're welcome to try it anyway. Change `gameMode` in `car_game.py` to "Random". 

## World Builder
Want to build your own track? You can! `worldbuilder.py` is a version of the game that lets you place blue cars wherever you want. Make your own difficulty label, and then run the worldbuilder. Use the arrow keys to move the camera around, and then left click where ever you want a car. Blue cars auto snap to the nearest lane midline so they are always centered on their lane. There isn't an easy way to remove erronous cars, so be careful where you click. When you're done, hit 'Q' to save and exit. The next time you load the game with that difficulty mode, all of your cars will be where you placed them. You can also change the road length at the top of this file. 


## View Modes

### Chaser View
This mode fixes the camera frame to the orange car, and moves with it. The planner has access to the entire course, but the pygame visualizer only shows a portion of it at a time. This allows you to see the action up close and with more detail. This mode is the default. 

### Sky View (PENDING)
This mode fixes the camera frame to the entire track, and it does not move. This allows you to see the entire track at once, but it may be more difficult to see the finer details, especially on the longer courses. 

### Photo Mode
The program has an optional Photo Mode (accessible by running `photo.py`) that takes a photo of the entire track at the start. This mode was used to create the track images for each of the difficulty modes above. Set the difficulty in `photo.py` to whichever course you want to take a photo off. The game will load, take a photo (saved to `world_files/difficulty.png`) and then quit. 


## Sources and Additional Reading
http://ckw.phys.ncku.edu.tw/public/pub/Notes/GeneralPhysics/Powerpoint/Extra/05/11_0_0_Steering_Theroy.pdf

## Graphic Sources

Car graphics from: http://clipart-library.com/overhead-car-cliparts.html

Grass from https://www.moddb.com/groups/indie-devs/tutorials/how-to-make-a-simple-grass-texture-in-gimp