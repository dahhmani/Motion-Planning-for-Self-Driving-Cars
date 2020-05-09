import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import random

euclidean = lambda vector1, vector2: np.linalg.norm(np.array(vector1) - np.array(vector2))
manhattan = lambda vector1, vector2: np.sum(np.absolute(np.array(vector1) - np.array(vector2)))

class RoadMap:
    def __init__(self,game,world):
        self.game = game
        # discretized space parameters
        start=(410,408)
        goal=(world.width_px-1.5*world.window.finish.get_width(), world.height_px/2)
        self.start, self.goal = Node(start), Node(goal)
        self.width = world.width_px
        self.height = world.height_px - 180 
        self.goalRadius = 30 
        self.lanes_y = [180, 270, 360, 450, 540]
        # obstacles' parameters
        self.verticalOffset = 30 # 2*game.orange_car.car_width_px
        self.horizontalOffset = 30 # 45 - game.orange_car.car_height_px/2 + 5
        # robot parameters
        self.robotRadius = game.orange_car.car_width_px//2
        self.stepSize = 50 
        ## trajectory parameters
        self.mergeDistance = 2*game.orange_car.car_width_px

    def collisionAvoidance(self, state):
        p = state[:2]
        isNotObstacle = True
        for obstacle in self.game.obst_list:
            if self.inRectangle(p, obstacle):
                isNotObstacle = False
                break

        return isNotObstacle

    def sample(self, goalProbability):
        # if random.randint(0,100) > goalProbability*100:
        if random.random() > goalProbability:
            return Node((random.uniform(self.start.state[0], self.width), random.uniform(180, self.height)))
        else:
            return self.goal

    def checkLane(self, waypoint):
        lanes = self.lanes_y
        y = waypoint[1]
        if lanes[0] <= y < lanes[1]:
            return 3 # leftmost lane
        elif lanes[1] <= y < lanes[2]:
            return 2
        elif lanes[2] <= y < lanes[3]:
            return 1
        elif lanes[3] <= y < lanes[4]:
            return 0 # rightmost lane
        else:
            return None

    def inRectangle(self, point, obstacle):
        # Robot's current position
        x, y = point[0], point[1] # (col, row)
        
        # rectangle parameters
        x_L = obstacle.spritex-self.horizontalOffset
        x_U = obstacle.spritex+obstacle.car_width_px+self.horizontalOffset
        y_L = obstacle.spritey-self.verticalOffset
        y_U = obstacle.spritey+obstacle.car_height_px+self.verticalOffset

        return x_L <= x <= x_U and y_L <= y <= y_U

    def contain(self, state):

        return self.start.state[0] <= state[0] <= self.width and 180 <= state[1] <= self.height

    def create(self):
        figure = plt.figure(figsize=(11,2))
        self.ax = plt.axes(xlim=(0,self.width), ylim=(180,self.height))
        self.ax.invert_yaxis()
        self.ax.set_aspect('equal')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Map')
        # draw obstacles
        for obstacle in self.game.obst_list:
            x_L = obstacle.spritex
            x_U = x_L+obstacle.car_width_px
            y_L = obstacle.spritey
            y_U = y_L+obstacle.car_height_px
            self.drawPolygon((x_L, x_U, y_L, y_U))
        # draw lanes
        for i in range(1, 4):
            lane_y = self.lanes_y[i]
            plt.plot((0,self.width), (lane_y,lane_y), '--', color='green', linewidth=0.5)

        return figure

    def drawPolygon(self, parameters):
        if isinstance(parameters, tuple):
            x_L, x_U, y_L, y_U = parameters
            vertices = [(x_L,y_L), (x_U,y_L), (x_U,y_U), (x_L,y_U)]
        else:
            vertices = parameters       

        polygon = Polygon(vertices, linewidth=0.5, color='blue')
        self.ax.add_artist(polygon)

    def drawArrow(self, start, end, color='black'):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        # arrow = plt.quiver(start[0], start[1], end[0], end[1], color=color, units = 'xy', scale = 5)
        arrow = plt.arrow(start[0], start[1], dx, dy, color=color, length_includes_head=True, head_width=0.1, head_length=0.15)
        self.ax.add_artist(arrow)

        return arrow

    def drawCircle(self, parameters, color='blue'):
        xc, yc, r = parameters

        circle = Circle((xc,yc), r, linewidth=0.5, color=color)
        self.ax.add_artist(circle)

        return circle    

    @staticmethod
    def drawSegment(segment):
        # p (x,y) in image coords
        X = list(map(lambda p: p[0], segment))
        Y = list(map(lambda p: p[1], segment))
        plt.plot(X, Y, '-o', color='cyan', linewidth=0.5, markersize=0.1, zorder=0)

    @staticmethod
    def scatter(X, Y):
        plt.plot(X, Y, 'o', color='cyan', markersize=0.5, zorder=0)

class Tree:
    def __init__(self, rootNode):
        self.nodes = [rootNode] # robot states 

    def addEdge(self, existingNode, newNode):
        newNode.parent = existingNode
        self.nodes.append(newNode)

    def nearestNeighbor(self, randomState):
        minDistance = np.inf
        for state in self.nodes:
            distance = state.cost2go(randomState)
            if distance < minDistance:
                minDistance = distance
                nearestNode = state

        return (nearestNode, minDistance)

class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state # the pose (position + orientation) of the point robot stored as (x, y, theta)
        self.action = action # the action performed on the parent to produce this state
        self.parent = parent # previous node
        self.trajectory = [] # interpolated states from parent to child

    def neighbors(self, Map):    
        adj = []
        # x, y, theta = self.state
        x, y, theta = self.state[0], self.state[1], 0      
     
        # action set = {direction of movement defined as an angle}
        no_actions=8
        d = Map.stepSize
        actions = np.linspace(np.deg2rad(-180), np.deg2rad(180), no_actions, endpoint=True) 
        for action in actions:
            angle = theta + action # in radians
            if angle <= -np.pi:
                angle += 2*np.pi
            if angle > np.pi:
                angle -= 2*np.pi
            adj.append(((x + d*np.cos(angle), y + d*np.sin(angle), angle), action))

        return [(Node(neighbor[0], neighbor[1]), Map.stepSize) for neighbor in adj if Map.contain(neighbor[0]) and Map.collisionAvoidance(neighbor[0])]

    def cost2go(self, other, heuristic=euclidean):

        return heuristic(self.state[:2], other.state[:2])

    def discretize(self, grid):
        xIndex = self.index(self.state[0], grid.positionResolution)
        yIndex = self.index(self.state[1], grid.positionResolution)
        # thetaIndex = int(self.state[2]/grid.angleResolution)
        thetaIndex = 0

        return xIndex + grid.sizeX*(yIndex + thetaIndex*grid.sizeY)

    @staticmethod
    def index(num, threshold):
        # amplification is needed because of floating point roundoff errors
        amplification = 1e6 # higher amplification allows lower thresholds
        num_int = num // 1
        num_dec = (num % 1)
        quotient = num_dec // threshold 

        num_dec *= amplification
        threshold *= amplification
        remainder = num_dec % threshold

        if quotient:
            if remainder >= threshold/2:
                i = num_int + (quotient*threshold + threshold)/amplification
            else:
                i = num_int + quotient*threshold/amplification
        else:
            if remainder >= threshold/2: 
                i = num_int + threshold/amplification
            else:
                i = num_int

        return int(i/threshold*amplification)

    def stoppingState(self, stateSpace, other, maxBranchSize, distance):
        if self == other:
            newNode = None
        elif distance <= maxBranchSize and stateSpace.collisionAvoidance(other.state):
            newNode = other
        else:
            p1, p2 = self.state, other.state
            ratio = maxBranchSize / distance
            x_pi = p1[0] + ratio*(p2[0]-p1[0])
            y_pi = p1[1] + ratio*(p2[1]-p1[1])
            newNode = Node((x_pi, y_pi))
            if not stateSpace.collisionAvoidance(newNode.state):
                newNode = None

        return newNode
                
    def __eq__(self, other):

        return self.state == other.state

    def __lt__(self, other): 
        # overloading this operator is required to make "heapq" work 
        return self.state < other.state