import math
import random

class Enemy:
    def __init__(self, app, speed, size, health, fill):
        self.x = random.random() * 1000
        self.y = random.random() * -100
        self.speed = speed
        self.size = size
        self.health = health
        self.angle = calculateTheta(self.x, self.y, app.px, app.py)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
        self.fill = fill

    def updateTarget(self, app):
        self.angle = calculateTheta(self.x, self.y, app.px, app.py)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)



def calculateTheta(x, y, targetX, targetY):
    adjacent = targetX - x
    opposite = targetY - y
    theta = math.atan2(opposite, adjacent)
    return theta