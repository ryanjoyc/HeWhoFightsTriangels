import math
import random

# Standard bullet that calculates its path and change in position to reach that path
class Bullet:
    def __init__(self, x, y, targetX, targetY, speed):
        self.radius = 10
        self.fill = 'black'
        self.x = x
        self.y = y
        self.angle = calculateTheta(x, y, targetX, targetY)
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)
# Enemy bullet to go into enemy lists, also with changeable radius
class EnemyBullet(Bullet):
    def __init__(self, x, y, targetX, targetY, speed, radius):
        super().__init__(x, y, targetX, targetY, speed)
        self.radius = radius

def calculateTheta(x, y, targetX, targetY):
    adjacent = targetX - x
    opposite = targetY - y
    theta = math.atan2(opposite, adjacent)
    return theta
