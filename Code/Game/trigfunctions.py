import math
import numpy as np

def cosd(deg_angle):
	a=math.cos(np.deg2rad(deg_angle))
	return a

def sind(deg_angle):
	a=math.sin(np.deg2rad(deg_angle))
	return a

def tand(deg_angle):
	a=math.tan(np.deg2rad(deg_angle))
	return a


def cotd(deg_angle):
	a=math.sin(np.deg2rad(deg_angle))
	b=math.cos(np.deg2rad(deg_angle))

	cotd=b/a
	return cotd

def cot(rad_angle):
	a=math.sin(rad_angle)
	b=math.cos(rad_angle)
	cot=b/a
	return cot