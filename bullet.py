import math
import random

class Bullet:
    def __init__(self, x, y, targetX, targetY, speed):
        self.id = random.random()
        self.radius = 10
        self.fill = 'black'
        self.x = x
        self.y = y
        self.angle = calculateTheta(x, y, targetX, targetY)
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)

    def __eq__(self, other):
        if isinstance(other, Bullet) and self.id == other.id:
            return True
        else:
            return False
    
    

def calculateTheta(x, y, targetX, targetY):
    adjacent = targetX - x
    opposite = targetY - y
    theta = math.atan2(opposite, adjacent)
    return theta
