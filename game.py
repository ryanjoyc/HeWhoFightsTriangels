from cmu_graphics import *
from bullet import Bullet
from enemy import Enemy
from room import Room
import math
import random

def onAppStart(app):
    app.width = 1920
    app.height = 900

    #Map Variables
    app.map = createMap()
    app.currentPlatforms = []

    # Find where the player is:
    app.currentRoom = app.map[2][1] # Just to make sure the first room loads properly for testing the function drawRoom()

    #Object Variable 
    app.floorPlatformHeight = 50
    app.floorPlatformY = (app.height - app.floorPlatformHeight)

    #Bullet Variables
    app.bullets = []

    #Enemy Variables
    app.enemies = []

    #Player variables
    app.pr = 30
    app.pcolor = gradient('red', 'black')
    app.px = app.width / 2
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
    halfHeight = app.height / 2
    halfWidth = app.width / 2
    drawRoom(app, app.currentRoom)
    drawCircle(app.px, app.py, app.pr, fill=app.pcolor)
    if app.currentMouseX != None and app.currentMouseY != None:
        drawCursor(app)
    for bullet in app.bullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            drawCircle(bullet.x, bullet.y, bullet.radius, fill=bullet.fill)
    for enemy in app.enemies:
        drawTriangle(enemy.x, enemy.y, enemy.size, enemy.fill)

def onMousePress(app, mouseX, mouseY):
    app.bullets.append(Bullet(app.px, app.py, mouseX, mouseY, 25))

def onMouseMove(app, mouseX, mouseY):
    app.currentMouseX = mouseX
    app.currentMouseY = mouseY


def onStep(app):
    #Recreate variables, some are just for conveniece right now like app.playerBottom which just made the falling calculation more intuitive
    move(app)
    app.playerBottom = app.py + (app.pr)
    fall(app)
    
 
    #Check if the player is on the ground
    if app.playerBottom >= app.height - 50:
        app.isOnGround = True
        app.isJumping = False
        app.pdy = 0
        app.jumps = 2

    #Creating the ability to jump
    if app.isJumping:
        app.pdy += 1

    #Check and update bullets
    for bullet in app.bullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
        else:
            print('delete')
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

# Can possible add a level variable that will incrementally increase the number of enemies in each room
def createMap():
    map = [[Room(False, randomEnemyCount(3, 5), createRoom(), '0011'), Room(False, randomEnemyCount(3, 5), createRoom(), '1011'), Room(False, randomEnemyCount(3, 5), createRoom(), '1001')],
           [Room(False, randomEnemyCount(3, 5), createRoom(), '0111'), Room(False, randomEnemyCount(3, 5), createRoom(), '1111'), Room(False, randomEnemyCount(3, 5), createRoom(), '1101')],
           [Room(False, randomEnemyCount(3, 5), createRoom(), '0110'), Room(True, 0, createRoom(), '1110'),                       Room(False, randomEnemyCount(3, 5), createRoom(), '1100')]]
    return map

def createRoom():
    room = []
    for i in range(2):
        floor = ''
        gapIndex = math.floor(random.random() * 3)
        for i in range(3):
            if i == gapIndex:
                floor += '0'
            else:
                floor += '1'
        room.append(floor)
    return room

def drawRoom(app, room):
    halfHeight = app.height / 2
    halfWidth = app.width / 2
    platformWidth = ((app.width - 100) / 3)

    if int(room.doors[0]) == 1:
        drawRect(0, 0, 50, halfHeight - 50)
        drawRect(0, halfHeight + 50, 50, app.height)
    else:
        drawRect(0, 0, 50, app.height)

    if int(room.doors[1]) == 1:
        drawRect(0, 0, halfWidth - 50, 50)
        drawRect(halfWidth + 50, 0, app.width, 50)
    else:
        drawRect(0, 0, 50, 50)

    if int(room.doors[2]) == 1:
        drawRect(app.width - 50, 0, app.width, halfHeight - 50)
        drawRect(app.width - 50, halfHeight + 50, app.width, app.height)
    else:
        drawRect(app.width - 50, 0, app.width, app.height)
    
    if int(room.doors[3]) == 1:
        drawRect(0, app.height - 50, halfWidth - 50, app.height)
        drawRect(halfWidth + 50, app.height - 50, app.width, app.height)
    else:
        drawRect(0, app.height - 50, app.width, app.height)
    for i in range(2):
        for j in range(3):
            if app.currentRoom.map[i][j] == '1':
                drawRect(50 + platformWidth * j, 550 - 350 * i, platformWidth, 50)
                app.currentPlatforms.append((50 + platformWidth * j, 550 - 350 * i, 50 + platformWidth * j + platformWidth, 550 - 350 * i + 50)) # Convert to top left and bottom right

def randomEnemyCount(min, max):
    return rounded(random.random() * (max - min)) + min

def drawCursor(app):
    drawCircle(app.currentMouseX, app.currentMouseY, 20, fill='white', border='black', borderWidth=1, opacity=100)

def fall(app):
    distanceToGround = app.floorPlatformY - app.playerBottom
    distanceToRoof = app.py - 100
    if app.pdy > 0 and app.pdy > distanceToGround:
        app.py = app.floorPlatformY - app.pr
        app.pdy = 0
        # for platform in app.currentPlatforms:
        #     distanceToPlatform = platform[1] - app.playerBottom
        #     if app.pdy > distanceToPlatform:
        #         app.py = platform[1] - app.pr
        #         app.pdy = 0
    elif app.pdy < 0 and abs(app.pdy) > distanceToRoof:
        app.py = 100 + app.pr
        app.pdy = 0 
    else:
        app.py += app.pdy

# Here is the move function, but we are also gonna incorporate the collision and registering those effects on movement here too
def move(app):
    dx = app.changepx / 5
    app.changepx -= dx
    futurePX = app.px + dx
    if isHittingBoundary(futurePX, app):
        dx = 0
    else:
        app.px += dx

# Checking if the player will be hitting a wall
def isHittingBoundary(px, app):
    doors = app.currentRoom.doors
    halfHeight = app.height / 2
    halfWidth = app.width / 2
    walls = []
    # Similar process to drawing the walls, but I am re-using the code to extract the points for all the rectangles that are the walls
    # This works at the moment, but might actually be bugged...
    if int(doors[0]) == 1:
        walls.append((0, 0, 50, halfHeight - 50))
        walls.append((0, halfHeight + 50, 50, app.height))
    else:
        walls.append((0, 0, 50, app.height))

    if int(doors[2]) == 1:
        walls.append((app.width - 50, 0, app.width, halfHeight - 50))
        walls.append((app.width - 50, halfHeight + 50, app.width, app.height))
    else:
        walls.append((app.width - 50, 0, app.width, app.height))

    # Now that we have all the points for the walls of the rectangle, we can check if the player intersects with any of them
    # Side Notes : I thought that by extracting the walls of every room would be easier as the walls change every time the player moves a room
    # This will also allow me to be more playful later on if I want to change the design of how the walls are lined...

    for wall in walls:
        if playerIntersectingWall(px, app.py, app.pr, wall[0], wall[1], wall[2], wall[3]):
            if app.changepx > 0:
                app.px = wall[0] - app.pr
            elif app.changepx < 0:
                app.px = wall[2] + app.pr
            return True
    
    return False

    
# This is a function that's job is simple, but it's process is somewhat hard to understand intuitively. I want to thank again ChatGPT for helping me come up with it.
def playerIntersectingWall(cx, cy, r, x1, y1, x2, y2):
  
    closest_x = max(x1, min(cx, x2)) # the rectacles bound is between its top right, x1, or its bottom left, x2, otherwise its between the two so we get cx
    closest_y = max(y1, min(cy, y2)) # same principle applies here too

    # Calculate the distance between the circle's center and this closest point
    distance_x = cx - closest_x
    distance_y = cy - closest_y

    # Check if the distance is less than or equal to the radius
    return (distance_x ** 2 + distance_y ** 2) <= (r ** 2)

    
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

def findPlayer(app):
    for level in app.map:
        for room in level:
            if room.player == True:
                app.currentRoom = room

cmu_graphics.runApp()