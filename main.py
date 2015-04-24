from __future__ import division

#Brooke Bullek & Daniel Vasquez
#Physics 212E Final Project

from visual import *
#import graphing features
from visual.graph import *
import math
from random import uniform
from random import choice

#turn on/off autoscaling
scene.autoscale = True
#give spheres shiny texture by default
scene.material = materials.plastic
#change background color
scene.background = (1, 1, 0.9)
#set window title
scene.title = "Drag Force!"
#set window center
scene.center = (10, 0, 0)
#set window dimensions


#initialize any constants
grav = -9.81
airDensity = 1.2 #changing this will influence the drag force

#create a floor
floor = box(pos = (10, -30, 0), length = 30, height = 1, width = 20,
            color = color.blue)

#create a class that generates spherical objects
class Ball:
    def __init__(self, mass, radius, color):
        '''Constructor method for class Ball. Instance variables include
        mass, radius, and color. From the first two, surface area and
        density can be calculated as attributes of a spherical object.
        '''
        self.mass = int(mass)
        self.radius = int(radius)
        self.color = color
        #these two will be calculated from the given parameters;
            #surface area is 4*pi*r^2 and density is mass/volume
        self.surfaceArea = 4 * pi * (self.radius)**2
        self.density = self.mass / ((4*pi)/3 * self.radius**3)
        #initialize a velocity
        self.velocity = vector(0, -2, 0)
        
    def __repr__(self):
        '''Method for printing a string representation of the object.
        '''
        print()

    def generateSphere(self):
        '''Creates a sphere from the given parameters.
        '''
        #set a default position for now, as we'll change these later
        ball = sphere(pos = (0,0,0), radius = self.radius, mass = self.mass,
                      color = self.color, surfaceArea = self.surfaceArea,
                      density = self.density, velocity = self.velocity)
        return ball

#designate how many balls to simulate (change to see different effects)
    '''play around with this!'''
numSpheres = 6

#list to store the spheres we'll soon be creating
balls = []

#first decide whether attributes should be random or manual input
userPreference = input("Would you like to randomly generate ball \
attributes (Y) or manually input ball  attributes yourself (N)? ")

#loop through number of spheres to create one ball for each
for i in range(numSpheres):
    if userPreference.upper() == 'Y':
        #use random.uniform to select numbers randomly from a continuous distribution
        mass = uniform(100, 500)
        radius = uniform(1, 2.5)
    elif userPreference.upper() == 'N':
        #get user input for each attribute (kind of tedious ...)
        mass = input('Select mass of ball ' + str(i) + '... ')
        radius = input('Select radius of ball ' + str(i) + '... ')
    #generate random tuple for color attribute
    color = tuple(uniform(0, 1) for i in (1, 2, 3))
    #add this object to this list of balls
    balls.append(Ball(mass, radius, color).generateSphere())
    #check more than 1 object in list 'balls' so index error won't occur
    if len(balls) != 0:
        balls[i].pos.x = balls[i-1].pos.x + (balls[i-1].radius + balls[i].radius)
    print('Added ball number ' + str(i+1) + '.')

#time-step
dt = .01

#create kinetic energy graph window
scene2 = display()
#create drag force graph window
scene3 = display()


#while loop deals with dynamic variables
while True:
    scene.select()
    rate(750)
    #change each object independently
    #Note: When drag becomes equal to weight, acceleration = 0 and terminal
        #velocity is reached.
    for ball in balls:
        # K = 1/2 * m * v^2
        kineticEnergy = 0.5 * ball.mass * (ball.velocity.y)**2
        # W = mg
        weight = -1 * ball.mass * grav
        #drag coefficient is interpreted as proportional to p and SA
        dragCoefficient = ball.surfaceArea/(18*ball.density)
        #D = C * p * v^2 * A/2
        dragForce = dragCoefficient * airDensity * (ball.velocity.y)**2 * \
                    ball.surfaceArea / 2
        # a = F/m = (W-D)/m
        acceleration = (weight - dragForce)/ball.mass
        if ball.velocity.y < 0:
            if ball.pos.y - ball.radius >= floor.pos.y + floor.height/2:
                #update velocity and position using Euler-Cromer step
                '''note: scaled to avoid overflow errors'''
                ball.velocity.y -= (dt*acceleration)
                ball.pos.y += (dt*ball.velocity.y)
            #bounce back up, if kinetic energy isn't zero
            else:
                ball.velocity.y *= -1
                #ball loses a bit of energy
                ball.velocity.y -= 3
        else:
            ball.velocity.y -= (dt*acceleration)
            ball.pos.y += (dt*ball.velocity.y)
            
        print (ball.velocity)
        ### Switch to kinetic energy graph
        scene2.select()
        

        ### Switch to drag force graph
        scene3.select()
