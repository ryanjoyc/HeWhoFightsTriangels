from cmu_graphics import *
from bullet import Bullet
from enemy import Enemy
import math
import random

def onAppStart(app):
    app.width = 1980
    app.height = 900

    #Object Variable 
    app.floorPlatformHeight = 100
    app.floorPlatformY = (app.height - app.floorPlatformHeight)

    #Bullet Variables
    app.bullets = []

    #Enemy Variables
    app.enemies = []

    #Player variables
    app.pr = 30
    app.pcolor = gradient('red', 'black')
    app.px = 50
    app.changepx = 0
    app.changepy = 0
    app.py = app.floorPlatformY - app.pr
    app.pdy = 0

    #Useful Player variables
    app.playerBottom = app.py + (app.pr)

    #Important Global Variables
    app.currentMouseX = None
    app.currentMouseY = None
    app.isOnGround = True
    app.isJumping = False
    app.jumps = 2

    app.stepsPerSecond = 60

def onKeyPress(app, key):
    if key == 'a':
        app.changepx -= 100
    if key == 'd':
        app.changepx += 100
    if key == 'space' and app.isOnGround or key == 'space' and app.jumps > 0:
        app.isOnGround = False
        if app.isJumping == False:
            app.isJumping = True
            app.jumps -= 1
            app.py -= 1
            app.pdy -= 20
        else:
            app.pdy = -20
            app.jumps -= 1
    if key == 'q':
        app.quit()
    if key == 't':
        app.enemies.append(Enemy(app, 10, 50, 5, 'black'))


def onKeyHold(app, keys):
    if 'a' in keys:
        app.changepx -= 20
    elif 'd' in keys:
        app.changepx += 20

def redrawAll(app):
    drawMap(app)
    drawCircle(app.px, app.py, app.pr, fill=app.pcolor)
    if app.currentMouseX != None and app.currentMouseY != None:
        drawCursor(app)
    for bullet in app.bullets:
        if bullet.x > 0 and bullet.x < 1000 and bullet.y > 0 and bullet.y < 1000:
            drawCircle(bullet.x, bullet.y, bullet.radius, fill=bullet.fill)
    for enemy in app.enemies:
        drawTriangle(enemy.x, enemy.y, enemy.size, enemy.fill)

def onMousePress(app, mouseX, mouseY):
    app.bullets.append(Bullet(app.px, app.py, mouseX, mouseY, 25))

def onMouseMove(app, mouseX, mouseY):
    app.currentMouseX = mouseX
    app.currentMouseY = mouseY


def onStep(app):
    #Recreate variables
    dx = app.changepx / 5
    app.changepx -= dx
    app.px += dx
    app.playerBottom = app.py + (app.pr)
    fall(app)
    
 
    #Check if the player is on the ground
    if app.playerBottom >= app.floorPlatformY:
        app.isOnGround = True
        app.isJumping = False
        app.pdy = 0
        app.jumps = 2

    #Creating the ability to jump
    if app.isJumping:
        app.pdy += 1

    #Check and update bullets
    for bullet in app.bullets:
        if bullet.x > 0 and bullet.x < 1000 and bullet.y > 0 and bullet.y < 1000:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
        else:
            app.bullets.remove(bullet)
    # manages the enemies in the game
    for enemy in app.enemies:
        # Updates the enemies position and where the users position is
        enemy.updateTarget(app)
        enemy.x += enemy.dx
        enemy.y += enemy.dy

        # Checks if the enemy is is contact with a bullet and then acts on them if so
        if enemy.fill == 'red':
            enemy.fill = 'black'
        for bullet in app.bullets:
            if isColliding(enemy, bullet):
                enemy.health -= 1
                enemy.fill = 'red'
                app.bullets.remove(bullet)
                if enemy.health == 0:
                    app.enemies.remove(enemy)


def takeStep(app):
    pass

def drawMap(app):
    drawRect(0, app.height - app.floorPlatformHeight, app.width, app.floorPlatformHeight)

def drawCursor(app):
    drawCircle(app.currentMouseX, app.currentMouseY, 20, fill='white', border='black', borderWidth=1, opacity=100)

def fall(app):
    distanceToGround = app.floorPlatformY - app.playerBottom
    if app.pdy > 0 and app.pdy > distanceToGround:
        app.py = app.floorPlatformY - app.pr
        app.pdy = 0
    else:
        app.py += app.pdy

def isColliding(enemy, bullet):
    if not isinstance(enemy, Enemy) or not isinstance(bullet, Bullet):
        return False
    enemyPoints = [(enemy.x, enemy.y), (enemy.x + enemy.size, enemy.y), (enemy.x + (enemy.size / 2), enemy.y + (enemy.size *(math.sqrt(3) / 2))), (enemy.x + (enemy.size / 2), (enemy.y + (enemy.size *(math.sqrt(3) / 2))) / 2)]

    for point in enemyPoints:
        distance = getDistance(bullet.x, bullet.y, point[0], point[1])
        if distance <= bullet.radius:
            return True
        
    return False
    
def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def pointToSegmentDistance(px, py, x1, y1, x2, y2):
    # Shortest distance from point (px, py) to the line segment (x1, y1) -> (x2, y2)
    lineLengthSQ = (x2 - x1)**2 + (y2 - y1)**2
    
    # This is an edge case, won't be used all the time
    if lineLengthSQ == 0:  # The segment is a point
        return getDistance(px, py, x1, y1)
    
    # As it follows, this is some advanced math type shit to calculate whether or not my point intercepts anywhere on the line segment
    # I would like to thank chatGPT for inspiring this rather advanced programming
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / lineLengthSQ))
    projectionX = x1 + t * (x2 - x1)
    projectionY = y1 + t * (y2 - y1)
    return getDistance(px, py, projectionX, projectionY)

def isColliding(enemy, bullet):
    # First check if btoh enemy and bullet are of correct classes
    if not isinstance(enemy, Enemy) or not isinstance(bullet, Bullet):
        return False
    
    # Define triangle points
    x1, y1 = enemy.x, enemy.y  # Bottom-left vertex
    x2, y2 = enemy.x + enemy.size, enemy.y  # Bottom-right vertex
    x3, y3 = enemy.x + (enemy.size / 2), enemy.y + (enemy.size * (math.sqrt(3) / 2))  # Top vertex
    
    #Just put the points in a list for simple and easy iteration
    trianglePoints = [(x1, y1), (x2, y2), (x3, y3)]
    
    # Check collision with vertices
    for point in trianglePoints:
        if getDistance(bullet.x, bullet.y, point[0], point[1]) <= bullet.radius:
            return True
    
    # Check collision with edges, which are just the three different points I used to draw the triangle
    edges = [(x1, y1, x2, y2), (x2, y2, x3, y3), (x3, y3, x1, y1)]
    for edge in edges:
        if pointToSegmentDistance(bullet.x, bullet.y, edge[0], edge[1], edge[2], edge[3]) <= bullet.radius:
            return True
    
    # If it doesn't collide with any of the points or lines, it isn't colliding, thus it is false
    return False

# Simple drawTriangle function that can take 
def drawTriangle(topLeftX, topLeftY, side, fill):
    drawPolygon(topLeftX, topLeftY, topLeftX + side, topLeftY, topLeftX + side / 2, topLeftY + (side * (math.sqrt(3)  / 2)), fill=fill)

cmu_graphics.runApp()