from Quaternion import Quaternion, rotate, qRotation
from mbhandler import MBHandler
import random

t = 0
g = PVector(0,0,-1)
q = PVector(0,0,-1).rotateTo(PVector(0,1,0))

def setup():
    global mb
    size(480,480,P3D)
    mb = MBHandler()
    

def draw():
    global t
    background(255)
    translate(240,240,0)
    scale(1,-1,1)
    #rotate(q)
    rotate(-PI/2,1,0,0)
    rotate(g.rotateTo(mb.data["accelerometer"]))
    line(0,0,0,0,0,100)
    line(0,0,0,0,100,0)
    line(0,0,0,100,0,0)
    translate(35,25,15)
    box(70,50,30)
    t += .05
    if t > 1:
        t = 0

def serialEvent(evt):
    if mb.addEvent(evt):
        return
