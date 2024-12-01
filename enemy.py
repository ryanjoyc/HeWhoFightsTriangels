import math
import random

class Enemy:
    def __init__(self, app, speed, size, health, fill):
        if app.px < app.width / 2:
            self.x = random.random() * app.width / 2 + app.width / 2
            self.y = random.random() * -100
        else:
            self.x = random.random() * app.width / 2
            self.y = random.random() * - 100
        self.speed = speed
        self.angle = int(random.random() * 360)
        self.size = size
        self.health = health
        self.angle = calculateTheta(self.x, self.y, app.px, app.py)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
        self.originalFill = fill
        self.fill = fill
        self.rotateAngle = int(random.random() * 360)

    def updateTarget(self, app):
        self.angle = calculateTheta(self.x, self.y, app.px, app.py)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

class Liner(Enemy):
    def __init__(self, app, speed, size, health, fill):
        super().__init__(app, speed, size, health, fill)
        self.rotateAngle = self.angle
        self.count = 0
    def updateTarget(self, app):
        super().updateTarget(app)

class Ranger(Enemy):
    def __init__(self, app, speed, size, health, fill):
        super().__init__(app, 0, size, health, fill)
        self.y = random.random() * app.height
        self.count = app.stepsPerSecond * 2
    def updateTarget(self, app):
        super().updateTarget(app)
        


def calculateTheta(x, y, targetX, targetY):
    adjacent = targetX - x
    opposite = targetY - y
    theta = math.atan2(opposite, adjacent)
    return theta