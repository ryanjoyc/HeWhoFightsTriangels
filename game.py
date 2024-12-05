from cmu_graphics import *
from bullet import Bullet
from bullet import EnemyBullet
from enemy import Enemy
from enemy import Liner
from enemy import Ranger
from enemy import Boss
from room import BossRoom
from room import Room
import math
import random

def story_onScreenActivate(app):
    app.background = 'white'

    #Bullet Variables
    app.playerBullets = []
    app.enemyBullets = []
    app.lightningBullets = []
    app.lightningHitbox = []
    app.currentShots = []

    #Enemy Variables
    app.enemies = []

    #Object Variable 
    app.floorPlatformHeight = 50
    app.floorPlatformY = (app.height - app.floorPlatformHeight)

    #Player variables
    app.playerHealth = 3
    app.pr = 30
    app.pcolor = 'blue'
    app.px = app.width / 2
    app.py = app.floorPlatformY - app.pr
    app.pdy = 0
    app.pdx = 0
    app.jumpHeight = 0.3334 * app.stepsPerSecond
    app.playerImmune = False
    app.iFrameCount = 0
    app.playerBottom = app.py + (app.pr)
    app.jumps = 2
    app.isOnGround = True
    app.isFalling = False
    app.gameOver = False

    #Map Variables
    app.map = createMap(app)
    app.currentPlatforms = []
    app.currentDoors = []
    app.currentDoorColors = ''

    # Find where the player is:
    app.mapCurrentY = 2
    app.mapCurrentX = 1
    app.currentRoom = app.map[app.mapCurrentY][app.mapCurrentX] # Just to make sure the first room loads properly for testing the function drawRoom()
    loadRoom(app)

def onAppStart(app):
    app.width = 1700
    app.height = 900
    app.background = 'black'

    #Important Global Variables
    app.stepsPerSecond = 60

def menu_redrawAll(app):
    drawLabel('HeWhoFightsTriangle', app.width / 2, 100, bold=True, fill='white', size=48)

    drawRect(app.width / 2 - 100, app.height / 2 - 100, 200, 100, opacity=100, borderWidth=5, border='white')
    drawLabel('STORY', app.width / 2, app.height / 2 - 50, size=36, bold=True, fill='white')

    drawRect(app.width / 2 - 100, app.height / 2 + 100, 200, 100, opacity=100, borderWidth=5, border='white')
    drawLabel('Tutorial', app.width / 2, app.height / 2 + 150, size=36, bold=True, fill='white')

def menu_onKeyPress(app, key):
    if key == 'q':
        app.quit()

def menu_onMousePress(app, mouseX, mouseY):
    if (app.width / 2 - 100 <= mouseX and mouseX <= app.width / 2 + 100) and (app.height / 2 - 100 <= mouseY and mouseY <= app.height / 2 ):
        setActiveScreen('story')
    if (app.width / 2 - 100 <= mouseX and mouseX <= app.width / 2 + 100) and (app.height / 2 + 100 <= mouseY and mouseY <= app.height / 2 + 200):
        setActiveScreen('tutorial')
    
def tutorial_onScreenActivate(app):
    app.background = 'black'

def tutorial_redrawAll(app):
    drawLabel('HOW TO PLAY', app.width / 2, 100, bold=True, fill='white', size=48)
    
    drawLabel('Movement:', 150, 200, italic=True, fill='white', size=36)
    drawLabel('To move the character, use A to go left, D to go right, and space to jump! Due to your spherical and circular properties, you can', 300, 200, fill='white', size=24, align='left')
    drawLabel('double jump too. You can jump up through the different platforms and land on them to refresh your jumps. To descend a platform, ', 300, 230, fill='white', size=24, align='left')
    drawLabel('simply press S while standing on one. Jump into the red or green squares to move to adjacent rooms.', 300, 260, fill='white', size=24, align='left')

    drawLabel('Combat:', 150, 350, italic=True, fill='white', size=36)
    drawLabel('To shoot, simply click and bullet will shoot to that point. Entering a room with a red door means there are enemies in that room. ', 300, 350, fill='white', size=24, align='left')
    drawLabel('The enemies can spawn in various places throughout the room, so it might be smart to scout the room before jumping right in. Also, ', 300, 380, fill='white', size=24, align='left')
    drawLabel('there are various different enemy types with different abilities, movements, and health so analyze and act accordingly.', 300, 410, fill='white', size=24, align='left')
    drawLabel('You can see your health in the bottom left, and when you take damage you go temporarily invulnerable so escape while you can.', 300, 440, fill='white', size=24, align='left')

    drawLabel('Objective:', 150, 540, italic=True, fill='white', size=36)
    drawLabel('Clear all the rooms to unlock the final boss fight(still a work in progress) and try not to lose all three lives.', 300, 540, fill='white', size=24, align='left')

    drawRect(app.width / 2 - 75, app.height - 150, 150, 100, opacity=100, borderWidth=5, border='white')
    drawLabel('BACK', app.width / 2, app.height - 100, bold=True, fill='white', size=36)
    
def tutorial_onKeyPress(app, key):
    if key == 'q':
        app.quit()

def tutorial_onMousePress(app, mouseX, mouseY):
    if (app.width / 2 - 75 <= mouseX and mouseX <= app.width / 2 + 75) and (app.height - 150 <= mouseY and mouseY <= app.height - 50):
        setActiveScreen('menu')

def story_onKeyPress(app, key):
    if key == '1':
        loadBossRoom(BossRoom(), app)
    if key == '2':
        if isinstance(app.currentRoom, BossRoom):
            boss = app.enemies[0]
            boss.count = 0
            boss.isEnraged = True
            boss.isAnimating = True
    if key == 's':
        app.pdy += 2
        app.isFalling = True
    if key == 'a':
        app.pdx -= 100
    if key == 'd':
        app.pdx += 100
    if ((key == 'space') and app.isOnGround) or ((key == 'space') and app.jumps > 0):
        app.isOnGround = False
        if app.isFalling == False:
            app.isFalling = True
            #app.jumps -= 1
            app.py -= 1
            app.pdy -= 20
        else:
            app.pdy = -20
            #app.jumps -= 1
    if key == 'q':
        app.quit()
    if key == 't':
        app.enemies.append(Ranger(app, 2, 200, 10, 'violet'))

def story_onKeyHold(app, keys):
    if 'a' in keys:
        app.pdx -= 20
    elif 'd' in keys:
        app.pdx += 20

def story_redrawAll(app):
    #Check whether to load boss room or regular room because boss room has different template and scale
    if isinstance(app.currentRoom, BossRoom):
        print(app.stepsPerSecond)
        drawBossRoom(app)
        boss = app.enemies[0]
        if boss.isEnraged:
            if boss.targetX != None and boss.targetY != None:
                for i in range(len(app.lightningBullets)):
                    for j in range(1, len(app.lightningBullets[i])):
                        drawLine(app.lightningBullets[i][j-1][0], app.lightningBullets[i][j-1][1], app.lightningBullets[i][j][0], app.lightningBullets[i][j][1], fill='mediumSlateBlue')
    else:
        drawRoom(app, app.currentRoom)
    drawCircle(app.px, app.py, app.pr, fill=app.pcolor)
    drawHealthBar(app)

    if app.gameOver == True:
        drawRect(app.width / 2 - 200, app.height / 2 - 100, 400, 200, border='red', borderWidth=5)
        drawLabel('GAME OVER', app.width / 2, app.height / 2, fill='red', size=48)

    for bullet in app.enemyBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            drawCircle(bullet.x, bullet.y, bullet.radius, fill=bullet.fill)

    for bullet in app.playerBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            drawCircle(bullet.x, bullet.y, bullet.radius, fill=bullet.fill)

    for enemy in app.enemies:
        if isinstance(enemy, Ranger):
            drawTriangle(enemy.x, enemy.y, enemy.size, enemy.fill, 0)
            #save if want to change drawing of ranger or different enemy types
        elif isinstance(enemy, Boss):
            drawCircle(enemy.x, enemy.y, enemy.size, fill=enemy.fill)
        else:
            drawTriangle(enemy.x, enemy.y, enemy.size, enemy.fill, enemy.rotateAngle)

def story_onMousePress(app, mouseX, mouseY):
    app.playerBullets.append(Bullet(app.px, app.py, mouseX, mouseY, 25))

    if isinstance(app.currentRoom, BossRoom):
        app.currentShots.append((app.px, app.py))


def story_onMouseMove(app, mouseX, mouseY):
    app.currentMouseX = mouseX
    app.currentMouseY = mouseY

def story_onStep(app):
    #function to move the player
    movePlayer(app)

    #Watch player health
    # if app.playerHealth == 0:
    #     app.gameOver = True
    #     app.stepsPerSecond = 1
    
    # Stores all bullets the player shoots for 2 seconds, and then shoots the bullets back out
    if isinstance(app.currentRoom, BossRoom):
        boss = app.enemies[0]
        if boss.count == 0:
            for cord in app.currentShots:
                app.enemyBullets.append(EnemyBullet(boss.x, boss.y, cord[0], cord[1], 15, 10))
            app.currentShots = []
    
    #Mange player Iframes so they don't insta die``1
    if app.playerImmune == True:
        app.pcolor = 'gray'
        if app.iFrameCount == app.stepsPerSecond * 2:
            app.playerImmune = False
            app.iFrameCount = 0
        app.iFrameCount += 1

    #Check if the player is on the ground
    if app.playerBottom >= app.height - 50:
        app.isOnGround = True
        app.isFalling = False
        app.pdy = 0
        app.jumps = 2

    # Change the players current velocity values
    app.pdx = app.pdx - (app.pdx / 5)
    if app.isFalling:
        app.pdy += 1

    #Check and update bullets
    for bullet in app.playerBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
        else:
            app.playerBullets.remove(bullet)
    
    #Check and update enemy bullets
    for bullet in app.enemyBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
            if circleCollidingCircle(app.px, app.py, app.pr, bullet.x, bullet.y, bullet.radius) and app.playerImmune == False:
                app.playerHealth -= 1
                app.playerImmune = True
        else:
            app.enemyBullets.remove(bullet)

    # manages the enemies in the game
    for enemy in app.enemies:
        # Updates the enemies position and where the users position is
        if isinstance(enemy, Liner):
            if enemy.count == 0:
                enemy.count = 60
                enemy.updateTarget(app)
                enemy.x += enemy.dx
                enemy.y += enemy.dy
                enemy.rotateAngle = math.degrees(enemy.angle)
            elif enemy.count <= 15:
                enemy.count -= 1
            else:
                enemy.x += enemy.dx
                enemy.y += enemy.dy
                enemy.count -= 1
        elif isinstance(enemy, Ranger):
            if enemy.count == 0:
                app.enemyBullets.append(EnemyBullet(enemy.x, enemy.y, app.px, app.py, 10, 50))
                enemy.count = app.stepsPerSecond * 2
                #enemy.rotateAngle += 15

                enemy.updateTarget(app)
                enemy.x += enemy.dx
                enemy.y += enemy.dy
            else:
                #enemy.rotateAngle += 15
                enemy.x += enemy.dx
                enemy.y += enemy.dy
                enemy.count -= 1
        elif isinstance(enemy, Boss):
            if not enemy.isEnraged:
                if enemy.health == 25:
                    enemy.count = 0
                    enemy.isEnraged = True
                    enemy.isAnimating = True
                    enemy.targetPlayer(app)
                if enemy.count == 0:
                    enemy.getRandomTarget(app)
                    enemy.x += enemy.dx
                    enemy.y += enemy.dy
                    enemy.count = 120
                elif enemy.count == 60:
                    enemy.getRandomTarget(app)
                    enemy.x += enemy.dx
                    enemy.y += enemy.dy
                    enemy.count -= 1
                else:
                    enemy.count -= 1
                    enemy.x += enemy.dx
                    enemy.y += enemy.dy
            if enemy.isEnraged:
                if enemy.isAnimating == True:
                    if enemy.size >= enemy.originalSize * 1.75:
                        enemy.isAnimating = False
                    if enemy.size < enemy.originalSize * 1.75:
                        enemy.size += 1
                elif enemy.count == 0:
                    app.lightningBullets = []
                    app.lightningHitbox = None
                    enemy.targetPlayer(app)
                    for i in range(5):
                        distance = getDistance(enemy.x, enemy.y, enemy.targetX, enemy.targetY)
                        angle = calculateTheta(enemy.x, enemy.y, enemy.targetX, enemy.targetY)
                        dx = math.cos(angle) * (distance / 15)
                        dy = math.sin(angle) * (distance / 15)
                        if app.lightningHitbox == None:
                            app.lightningHitbox = ((enemy.x + dx, enemy.y), (enemy.y + dy, enemy.x), (enemy.targetX - dx, enemy.targetY), (enemy.targetX, enemy.targetY - dy))
                        app.lightningBullets.append(generateLightningPoints(boss.x, boss.y, boss.targetX, boss.targetY, 15))
                    enemy.count = 120
                elif enemy.count == 115:
                    app.lightningBullets = []
                    for i in range(5):
                        app.lightningBullets.append(generateLightningPoints(boss.x, boss.y, boss.targetX, boss.targetY, 15))
                    enemy.count -= 1
                elif enemy.count == 110:
                    app.lightningBullets = []
                    for i in range(5):
                        app.lightningBullets.append(generateLightningPoints(boss.x, boss.y, boss.targetX, boss.targetY, 15))
                    enemy.count -= 1
                else:
                    enemy.count -= 1
        else:
            enemy.updateTarget(app)
            enemy.x += enemy.dx
            enemy.y += enemy.dy
            enemy.rotateAngle += 15

        #Checks if enemy is in contact with player
        if app.playerImmune == False:
            if isCollidingWithPlayer(enemy, app):
                app.playerHealth -= 1
                app.playerImmune = True
            
        
        # Checks if the enemy is is contact with a bullet and then acts on them if so
        if enemy.fill != enemy.originalFill:
            enemy.fill = enemy.originalFill
        for bullet in app.playerBullets:
            if isinstance(enemy, Boss):
                if circleCollidingCircle(bullet.x, bullet.y, bullet.radius, enemy.x, enemy.y, enemy.size):
                    enemy.health -= 1
                    enemy.fill = 'red'
                    app.playerBullets.remove(bullet)
                    if enemy.health == 0:
                        app.enemies.remove(enemy)
            else:
                if isCollidingWithEnemy(enemy, bullet):
                    enemy.health -= 1
                    enemy.fill = 'red'
                    app.playerBullets.remove(bullet)
                    if enemy.health == 0:
                        app.enemies.remove(enemy)

# Can possible add a level variable that will incrementally increase the number of enemies in each room
def createMap(app):
    map = [[Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '0011'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1011'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1001')],
           [Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '0111'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1111'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1101')],
           [Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '0110'), Room([], createRoom(), '1110'),                                           Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1100')]]
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
        if app.currentDoorColors[0] == '0':
            drawRect(0, halfHeight - 50, 50, halfHeight + 50, fill='green')
        else:
            drawRect(0, halfHeight - 50, 50, halfHeight + 50, fill='red')
        drawRect(0, halfHeight + 50, 50, app.height)
    else:
        drawRect(0, 0, 50, app.height)

    if int(room.doors[1]) == 1:
        drawRect(0, 0, halfWidth - 50, 50)
        if app.currentDoorColors[1] == '0':
            drawRect(halfWidth - 50, 0, halfWidth + 50, 50, fill='green')
        else:
            drawRect(halfWidth - 50, 0, halfWidth + 50, 50, fill='red')
        drawRect(halfWidth + 50, 0, app.width, 50)
    else:
        drawRect(0, 0, app.width, 50)

    if int(room.doors[2]) == 1:
        drawRect(app.width - 50, 0, app.width, halfHeight - 50)
        if app.currentDoorColors[2] == '0':
            drawRect(app.width - 50, halfHeight - 50, app.width, halfHeight + 50, fill='green')
        else:
            drawRect(app.width - 50, halfHeight - 50, app.width, halfHeight + 50, fill='red')
        drawRect(app.width - 50, halfHeight + 50, app.width, app.height)
    else:
        drawRect(app.width - 50, 0, app.width, app.height)
    
    if int(room.doors[3]) == 1:
        drawRect(0, app.height - 50, halfWidth - 50, app.height)
        if app.currentDoorColors[3] == '0':
            drawRect(halfWidth - 50, app.height - 50, halfWidth + 50, app.height, fill='green')
        else:
            drawRect(halfWidth - 50, app.height - 50, halfWidth + 50, app.height, fill='red')
        drawRect(halfWidth + 50, app.height - 50, app.width, app.height)
    else:
        drawRect(0, app.height - 50, app.width, app.height)


    for i in range(2):
        for j in range(3):
            if app.currentRoom.map[i][j] == '1':
                drawRect(50 + platformWidth * j, 550 - 350 * i, platformWidth, 50, fill='brown')

def loadRoom(app):
    #Reset the current platforms everytime the character loads a new room
    app.currentPlatforms = []
    platformWidth = ((app.width - 100) / 3)
    app.playerBullets = []
    app.enemyBullets = []
    #Filter through and add all platforms to a list containing the top right and bottom left corner of all the platforms
    for i in range(2):
        for j in range(3):
            if app.currentRoom.map[i][j] == '1':
                app.currentPlatforms.append((50 + platformWidth * j, 550 - 350 * i, 50 + platformWidth * j + platformWidth, 550 - (350 * i) + 50)) # Convert to top left and bottom right

    #Spawn in the enmies
    app.enemies = app.currentRoom.enemies

    #Add all door paramters into the a list containg the corners of all doors in the currently loaded room
    halfHeight = app.height / 2
    halfWidth = app.width / 2
    doors = app.currentRoom.doors
    app.currentDoors = []
    app.currentDoorColors = ''

    if int(doors[0]) == 1:
        app.currentDoors.append((0, halfHeight - 50, 50, halfHeight + 50))
        if app.map[app.mapCurrentY][app.mapCurrentX - 1].enemies == []:
            app.currentDoorColors += '0'
        else:
            app.currentDoorColors += '1'
    else:
        app.currentDoorColors += '1'
    if int(doors[1]) == 1:
        app.currentDoors.append((halfWidth - 50, 0, halfWidth + 50, 50))
        if app.map[app.mapCurrentY - 1][app.mapCurrentX].enemies == []:
            app.currentDoorColors += '0'
        else:
            app.currentDoorColors += '1'
    else:
        app.currentDoorColors += '1'
    if int(doors[2]) == 1:
        app.currentDoors.append((app.width - 50, halfHeight - 50, app.width, halfHeight + 50))
        if app.map[app.mapCurrentY][app.mapCurrentX + 1].enemies == []:
            app.currentDoorColors += '0'
        else:
            app.currentDoorColors += '1'
    else:
        app.currentDoorColors += '1'
    if int(doors[3]) == 1:
        app.currentDoors.append((halfWidth - 50, app.height - 50, halfWidth + 50, app.height))
        if app.map[app.mapCurrentY + 1][app.mapCurrentX].enemies == []:
            app.currentDoorColors += '0'
        else:
            app.currentDoorColors += '1'
    else:
        app.currentDoorColors += '1'

def generateEnemies(enemyCount, app):
    enemies = []
    for i in range(enemyCount):
        randomEnemyIndex = math.floor(random.random() * 3)
        if randomEnemyIndex == 0: #create basic enemy
            enemies.append(Enemy(app, 5, 50, 5, 'purple'))
        elif randomEnemyIndex == 1: #create line enemy
            enemies.append(Liner(app, 7.5, 100, 10, 'green'))
        elif randomEnemyIndex == 2: #create ranger enemy
            enemies.append(Ranger(app, 2, 200, 10, 'violet'))
    return enemies

def randomEnemyCount(min, max):
    return rounded(random.random() * (max - min)) + min

#Currently not in use
def drawCursor(app):
    #Change cursor later
    drawCircle(app.currentMouseX, app.currentMouseY, 20, fill='white', border='black', borderWidth=1, opacity=0)

def drawHealthBar(app):
    for i in range(app.playerHealth):
        drawHeart(50 + 50 * i, app.height - 40, 30, 40)

def movePlayer(app):
    # Variables that make some of the code below a little bit clearer
    futurePX = app.px + (app.pdx / 5)
    futurePY = app.py + app.pdy
    currentPlayerBottom = app.py + app.pr
    futurePlayerBottom = futurePY + app.pr
    halfHeight = app.height / 2
    halfWidth = app.width / 2

    # Make a collision object, that way we don't have to run function multiple times, will store a true or false so we can still easily check
    platformCollision = collisionWithPlatforms(app, futurePX, futurePY)
    doorCollision = collisionWithDoors(app, futurePX, futurePY)
    if platformCollision[0]:
        platform = platformCollision[1]
        if app.pdy > 0 and futurePlayerBottom >= platform[1] and currentPlayerBottom < platform[1]:
            app.isFalling = False
            app.jumps = 2
            app.pdy = 0
            app.py = platform[1] - app.pr
            move(app)
        elif app.pdy <= 0 and currentPlayerBottom > platform[1]:
            move(app)
            fall(app)
        else:
            fall(app)
            move(app)
    elif doorCollision[0]:
        #This gets the top left corner of the door and then checks it with all possible door positions to determine the next room the player is going to
        doorTopLeft = doorCollision[2]
        if doorTopLeft == (0, halfHeight - 50):
            app.mapCurrentX -= 1
            app.currentRoom = app.map[app.mapCurrentY][app.mapCurrentX]
            app.px = (app.width - 50) - app.pr - 10 # the 10 is to make sure it doesn't hit the door again
            loadRoom(app)
        if doorTopLeft == (app.width - 50, halfHeight - 50):
            app.mapCurrentX += 1
            app.px = 50 + app.pr + 10
            app.currentRoom = app.map[app.mapCurrentY][app.mapCurrentX]
            loadRoom(app)
        if doorTopLeft == (halfWidth - 50, 0):
            app.mapCurrentY -= 1
            app.py = app.floorPlatformY - app.pr - 10
            app.currentRoom = app.map[app.mapCurrentY][app.mapCurrentX]
            loadRoom(app)
        if doorTopLeft == (halfWidth - 50, app.height - 50):
            app.mapCurrentY += 1
            app.py = 0 + 50 + app.pr
            app.currentRoom = app.map[app.mapCurrentY][app.mapCurrentX]
            loadRoom(app)
    else:
        app.isFalling = True
        app.pcolor = 'blue'   
        fall(app)
        move(app)
    
def collisionWithDoors(app, futurePX, futurePY):
    door = None
    for door in app.currentDoors:
        if playerIntersectingRectangle(futurePX, futurePY, app.pr, door[0], door[1], door[2], door[3]):
            door = (door[0], door[1], door[2], door[3])
            return (True, door, (door[0], door[1]))
    return (False, None)

def collisionWithPlatforms(app, futurePX, futurePY):
    platform = None

    for platform in app.currentPlatforms:
        if playerIntersectingRectangle(futurePX, futurePY, app.pr, platform[0], platform[1], platform[2], platform[3]):
            platform = (platform[0], platform[1], platform[2], platform[3])
            return (True, platform)
    return (False, None)

def fall(app):
    app.playerBottom = app.py + (app.pr)
    distanceToGround = app.floorPlatformY - app.playerBottom
    distanceToRoof = app.py - 80
    if app.pdy > 0 and app.pdy > distanceToGround:
        app.py = app.floorPlatformY - app.pr
        app.pdy = 0
        app.isFalling = False
    elif app.pdy < 0 and abs(app.pdy) > distanceToRoof:
        app.py = 50 + app.pr
        app.pdy = 0 
    else:
        app.py += app.pdy

# Here is the move function, but we are also gonna incorporate the collision and registering those effects on movement here too
def move(app):
    futurePX = app.px + (app.pdx / 5)
    if isHittingBoundary(futurePX, app):
        dx = 0
    else:
        app.px = futurePX

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
        if playerIntersectingRectangle(px, app.py, app.pr, wall[0], wall[1], wall[2], wall[3]):
            if app.pdx > 0:
                app.px = wall[0] - app.pr
            elif app.pdx < 0:
                app.px = wall[2] + app.pr
            return True
    
    return False

#This function will be used to check collision between enemy and player
def circleCollidingCircle(x1, y1, r1, x2, y2, r2):
    distance = getDistance(x1, y1, x2, y2)
    sumRadii = r1 + r2
    if distance <= sumRadii:
        return True
    else:
        return False
      
# This is a function that's job is simple, but it's process is somewhat hard to understand intuitively. I want to thank again ChatGPT for helping me come up with it.
def playerIntersectingRectangle(cx, cy, r, x1, y1, x2, y2):
  
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

def isCollidingWithEnemy(enemy, bullet):
    
    # Define triangle points
    side = enemy.size
    height = side * math.sqrt(3) / 2

    x1, y1 = enemy.x - side / 2, enemy.y - height / 2 # Top-left vertex
    x2, y2 = enemy.x + side / 2, enemy.y - height / 2 # Top-right vertex
    x3, y3 = enemy.x, enemy.y + height / 2  # Bottom vertex
    
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

def isCollidingWithLightning(lightningHitbox, app):

    #Just put the points in a list for simple and easy iteration
    points = [lightningHitbox[0], lightningHitbox[1], lightningHitbox[2], lightningHitbox[3]]
    
    # Check collision with vertices
    for point in points:
        if getDistance(app.px, app.py, point[0], point[1]) <= app.pr:
            return True
    
    # Check collision with edges, which are just the three different points I used to draw the triangle
    edges = [(x1, y1, x2, y2), (x2, y2, x3, y3), (x3, y3, x1, y1)]
    for edge in edges:
        if pointToSegmentDistance(app.px, app.py, edge[0], edge[1], edge[2], edge[3]) <= app.pr:
            return True
    
    # If it doesn't collide with any of the points or lines, it isn't colliding, thus it is false
    return False

def isCollidingWithPlayer(enemy, app):
    
    # Define triangle points
    side = enemy.size
    height = side * math.sqrt(3) / 2

    x1, y1 = enemy.x - side / 2, enemy.y - height / 2 # Top-left vertex
    x2, y2 = enemy.x + side / 2, enemy.y - height / 2 # Top-right vertex
    x3, y3 = enemy.x, enemy.y + height / 2  # Bottom vertex
    
    #Just put the points in a list for simple and easy iteration
    trianglePoints = [(x1, y1), (x2, y2), (x3, y3)]
    
    # Check collision with vertices
    for point in trianglePoints:
        if getDistance(app.px, app.py, point[0], point[1]) <= app.pr:
            return True
    
    # Check collision with edges, which are just the three different points I used to draw the triangle
    edges = [(x1, y1, x2, y2), (x2, y2, x3, y3), (x3, y3, x1, y1)]
    for edge in edges:
        if pointToSegmentDistance(app.px, app.py, edge[0], edge[1], edge[2], edge[3]) <= app.pr:
            return True
    
    # If it doesn't collide with any of the points or lines, it isn't colliding, thus it is false
    return False

# Simple drawTriangle function that can take 
def drawTriangle(centerX, centerY, side, fill, angle, border=None):
    height = (side * math.sqrt(3) / 2)
    if border == None:
        drawPolygon(centerX - side / 2, centerY - height / 2, centerX + side / 2, centerY - height / 2, centerX, centerY + height / 2, fill=fill, rotateAngle=angle)
    elif border != None:
        drawPolygon(centerX - side / 2, centerY - height / 2, centerX + side / 2, centerY - height / 2, centerX, centerY + height / 2, fill=fill, rotateAngle=angle, border=border, borderWidth=2)

def loadBossRoom(bossRoom, app):
    app.background = gradient('gray', 'white')
    app.currentRoom = bossRoom
    app.enemies = [Boss(app)]
    app.currentPlatforms = []
    app.recentShots = []
    platformWidth = app.width / 10

    for i in range(3):
        for j in range(10):
            if bossRoom.map[i][j] == '1':
                app.currentPlatforms.append((app.width + 50 + (platformWidth * j), app.height - 250 - (100 * i), app.width + 50 + platformWidth + platformWidth * j, app.height - 250 - (100 * i) + 50 ))

    app.currentDoors = []
    app.playerBullets = []
    app.enemyBullets = []

    app.px = app.width / 2
    app.pr = 30
    app.py = app.floorPlatformY - app.pr
    app.pdy = 0
    app.pdx = 0

def drawBossRoom(app):
    drawRect(0, 0, 50, app.height)
    drawRect(0, 0, app.width, 50)
    drawRect(app.width - 50, 0, app.width, app.height)
    drawRect(0, app.height - 50, app.width, app.height)
    drawBossHealthBar(app)

    platformWidth = app.width / 10

def generateLightningPoints(startX, startY, targetX, targetY, totalPoints):
    return generateLightningPointsHelper(startX, startY, startX, startY, targetX, targetY, totalPoints, totalPoints, [])

def generateLightningPointsHelper(startX, startY, currentX, currentY, targetX, targetY, totalPoints, currentPoints, cords):
    # If there are no more points to draw, return the coordinates of the points
    if currentPoints == 0:
        cords.append((targetX, targetY))
        return cords
    
    # recursive case is a lil bit trickier
    else:
        cords.append((currentX, currentY))

        distance = getDistance(startX, startY, targetX, targetY)
        angle = calculateTheta(startX, startY, targetX, targetY)
        dx = math.cos(angle) * (distance / totalPoints)
        dy = math.sin(angle) * (distance / totalPoints)

        minYThreshold = startY + (dy * (totalPoints - currentPoints))
        minXThreshold = startX + (dx * (totalPoints - currentPoints))

        if abs(dx) < 30:
            currentX = minXThreshold + ((random.random() * 60 - 30) * 3)
        else:
            currentX = minXThreshold + (random.random() * dx * 3)
        if abs(dy) < 30:
            currentY = minYThreshold + ((random.random() * 60 - 30) * 3)
        else:
            currentY = minYThreshold + (random.random() * dy * 3)

        return generateLightningPointsHelper(startX, startY, currentX, currentY, targetX, targetY, totalPoints, currentPoints - 1, cords)
    


def drawBossHealthBar(app):
    boss = app.enemies[0]
    drawRect(app.width / 2 - 200, 10, 400, 30, fill='lightGray')
    drawRect(app.width / 2 - 200, 10, (boss.health) * (400 / boss.maxHealth), 30, fill=gradient('crimson', 'darkRed'))
    drawRect(app.width / 2 - 150, 40, 300, 40, fill='black')
    drawRect(app.width / 2 - 145, 44, 290, 32, fill='gray')
    drawLabel('You?', app.width / 2, 60, fill='black', bold=True, italic=True, size=36)
    drawLabel(f'{boss.health}', app.width / 2, 25, size=24, bold=True)

def drawHeart(topLeftX, topLeftY, height, width):
    drawPolygon(topLeftX, topLeftY, topLeftX + width / 4, topLeftY - height / 4, topLeftX + width / 2, topLeftY, topLeftX + (3 * (width / 4)), topLeftY - height / 4, topLeftX + width, topLeftY, topLeftX + width / 2, topLeftY + height * (3 / 4), fill='red') 

def calculateTheta(x, y, targetX, targetY):
    adjacent = targetX - x
    opposite = targetY - y
    theta = math.atan2(opposite, adjacent)
    return theta

cmu_graphics.runAppWithScreens(initialScreen='menu')