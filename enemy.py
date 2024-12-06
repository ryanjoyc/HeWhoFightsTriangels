import math
import random

class Enemy: # This basic enemy class is the seeker, and the other classes build off of it
    def __init__(self, app, speed, size, health, fill):
        # Sets random spawn based on where the player first enters the room
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

class Liner(Enemy): # Has a count and rotate angle so it can update its position and change direction every once in a while
    def __init__(self, app, speed, size, health, fill):
        super().__init__(app, speed, size, health, fill)
        self.rotateAngle = self.angle
        self.count = 0
    def updateTarget(self, app):
        super().updateTarget(app)

class Ranger(Enemy): # Has count as well and random spawn position so it can shoot every certain amount of time
    def __init__(self, app, speed, size, health, fill):
        super().__init__(app, 0, size, health, fill)
        self.y = random.random() * app.height
        self.count = app.stepsPerSecond * 2
    def updateTarget(self, app):
        super().updateTarget(app)

class Boss(Enemy):
    def __init__(self, app):
        self.fill = 'blue'
        self.originalFill = 'blue'
        self.maxHealth = 75
        self.health = 75
        self.targetX = None
        self.targetY = None
        self.x = app.width / 2
        self.y = app.height / 2
        self.dx = 0
        self.dy = 0
        self.originalSize = app.pr
        self.size = app.pr
        self.speed = 0
        self.angle = 0
        self.count = 0
        self.isAnimating = False
        self.isImmune = False
        self.isEnraged = False
        self.enragedAttackCount = 0
    
    # Finds a random place to move that is not close to the player, this mode is supposed to be pretty passive
    def getRandomTarget(self, app):
        randomX = randomValue(50 + self.size, app.width - 50 - self.size)
        randomY = randomValue(50 + self.size, app.height - 50 - self.size)
        if getDistance(randomX, randomY, app.px, app.py) <= 250:
            self.getRandomTarget(app)
        else:
            self.angle = calculateTheta(self.x, self.y, randomX, randomY)
            self.speed = getDistance(self.x, self.y, randomX, randomY) / app.stepsPerSecond
            self.dx = self.speed * math.cos(self.angle)
            self.dy = self.speed * math.sin(self.angle)
        
    # Sets its target to the player's current position, for the lightning
    def targetPlayer(self, app):
        self.targetX = app.px
        self.targetY = app.py

 

def calculateTheta(x, y, targetX, targetY):
    adjacent = targetX - x
    opposite = targetY - y
    theta = math.atan2(opposite, adjacent)
    return theta

def randomValue(min, max):
    return round(random.random() * (max - min)) + min

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)