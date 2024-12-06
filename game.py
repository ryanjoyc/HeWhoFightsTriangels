# Ryan Joyce / ryanjoyc / 15-112-1A

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
    app.stepsPerSecond = 60

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
    app.screenFlashCount = 0
    app.currentBackgroundColor = app.background

    # Find where the player is:
    app.mapCurrentY = 2
    app.mapCurrentX = 1
    app.currentRoom = app.map[app.mapCurrentY][app.mapCurrentX] # Just to make sure the first room loads properly for testing the function drawRoom()
    app.allRoomsCleared = False
    app.gameWon = False

    loadRoom(app)

def onAppStart(app):
    app.width = 1700
    app.height = 900
    app.background = 'black'
    app.currentBackgroundColor = app.background

    #Important Global Variables
    app.stepsPerSecond = 60

def win_onScreenActivate(app):
    app.background = 'black'
    app.currentBackground = app.background

def win_redrawAll(app):
    drawRect(app.width / 2 - 300, app.height / 2 - 200, 600, 400, border='cyan', borderWidth=5)
    drawLabel('YOU WON', app.width / 2, app.height / 2 - 100, fill='white', size=36, bold=True, italic=True)
    drawLabel('and defeated your greatest enemy, yourself.', app.width / 2, app.height / 2 + 50, fill='white', size=24, italic=True)
    drawRect(app.width / 2 - 150, app.height / 2 + 110, 300, 80, borderWidth=5, border='white')
    drawLabel('Return to Menu', app.width / 2, app.height / 2 + 150, size=30, bold=True, fill='white')

def win_onMousePress(app, mouseX, mouseY):
    if (app.width / 2 - 150 <= mouseX and mouseX <= app.width / 2 + 150) and (app.height / 2 + 110 <= mouseY and mouseY <= app.height / 2 + 190):
        setActiveScreen('menu')

def win_onKeyPress(app, key):
    if key == 'q':
        app.quit()

def menu_onScreenActivate(app):
    app.background = 'black'

# This function draws everything in the menu screen
def menu_redrawAll(app):
    drawLabel('HeWhoFightsTriangles', app.width / 2, 100, bold=True, fill='white', size=48)

    drawRect(app.width / 2 - 100, app.height / 2 - 100, 200, 100, opacity=100, borderWidth=5, border='white')
    drawLabel('STORY', app.width / 2, app.height / 2 - 50, size=36, bold=True, fill='white')

    drawRect(app.width / 2 - 100, app.height / 2 + 100, 200, 100, opacity=100, borderWidth=5, border='white')
    drawLabel('Tutorial', app.width / 2, app.height / 2 + 150, size=36, bold=True, fill='white')

def menu_onKeyPress(app, key):
    if key == 'q':
        app.quit()

# Checks if player clicked off to other screens
def menu_onMousePress(app, mouseX, mouseY):
    if (app.width / 2 - 100 <= mouseX and mouseX <= app.width / 2 + 100) and (app.height / 2 - 100 <= mouseY and mouseY <= app.height / 2 ):
        setActiveScreen('story')
    if (app.width / 2 - 100 <= mouseX and mouseX <= app.width / 2 + 100) and (app.height / 2 + 100 <= mouseY and mouseY <= app.height / 2 + 200):
        setActiveScreen('tutorial')

def tutorial_onScreenActivate(app):
    app.background = 'black'

# Draws all the text explaining how to play the game
def tutorial_redrawAll(app):
    drawLabel('HOW TO PLAY', app.width / 2, 100, bold=True, fill='white', size=48)
    
    drawLabel('Movement:', 150, 200, italic=True, fill='white', size=36)
    drawLabel('To move the character, use A to go left, D to go right, and space to jump! Due to your spherical and circular properties, you can', 300, 200, fill='white', size=24, align='left')
    drawLabel('double jump too. You can jump up through the different platforms and land on them to refresh your jumps. To descend a platform, ', 300, 230, fill='white', size=24, align='left')
    drawLabel('simply press S while standing on one. Jump into the red or green squares to move to adjacent rooms. Q to quit!', 300, 260, fill='white', size=24, align='left')

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

# Movement is controlled here
def story_onKeyPress(app, key):
    if key == '1':
        app.allRoomsCleared = True
    if key == '2':
        enemy = app.enemies[0]
        enemy.x = app.width / 2
        enemy.y = app.height / 2
        enemy.count = 30
        enemy.isEnraged = True
        enemy.isAnimating = True
        enemy.targetPlayer(app)
    if key == 's':
        app.pdy += 2
        app.isFalling = True
    # A and D add and subtract to the change in x position variable app.pdx   
    if key == 'a':
        app.pdx -= 100
    if key == 'd':
        app.pdx += 100
    # Will initiate a jump if certain conditions are met such as being on a platform or on the ground or has jumps left
    if ((key == 'space') and app.isOnGround) or ((key == 'space') and app.jumps > 0):
        app.isOnGround = False
        if app.isFalling == False:
            app.isFalling = True
            app.jumps -= 1
            app.py -= 1
            app.pdy -= 20
        else:
            app.pdy = -20
            app.jumps -= 1
    if key == 'q':
        app.quit()

# Player can hold down the keys to move character horizontally as well
def story_onKeyHold(app, keys):
    if 'a' in keys:
        app.pdx -= 20
    elif 'd' in keys:
        app.pdx += 20

def story_redrawAll(app):
    # Draws a regular room (the walls and doors and platforms) if not a boss room, but then draws BossRoom and Boss Mechanics if in a boss room
    if isinstance(app.currentRoom, BossRoom) and not app.gameWon:
        drawBossRoom(app)
        drawLightningMechanics(app)
    else:
        drawRoom(app, app.currentRoom)

    # Draw the bullets and the enemies
    drawBullets(app)
    drawEnemies(app)

    # Draws player and health bar
    drawCircle(app.px, app.py, app.pr, fill=app.pcolor)
    drawHealthBar(app)

    # Draw the boss prompt if player clears all the rooms, allowing the player to face the final boss
    drawBossPrompt(app)

    # Draws game over menu/prompt if the player dies
    drawGameOverPrompt(app)

def story_onMousePress(app, mouseX, mouseY):
    # Adds the players bullet to the active bulelt list so it gets drawn and can now collide
    app.playerBullets.append(Bullet(app.px, app.py, mouseX, mouseY, 25))

    # If in the boss room, saves the players coordinates so the boss can shoot back at where the player used to be
    if isinstance(app.currentRoom, BossRoom):
        app.currentShots.append((app.px, app.py))
    
    # If the boss pop up appears, allow the plater to load the boss room when they click continue
    if app.allRoomsCleared:
        if (app.width / 2 - 200 <= mouseX and mouseX <= app.width / 2 + 200) and (app.height / 2 + 100 <= mouseY and mouseY <= app.height / 2 + 200):
            loadBossRoom(BossRoom(), app)
    
    # If the game over screen is up, allow the player to click return to menu
    if app.gameOver:
        if (app.width / 2 - 150 <= mouseX and mouseX <= app.width / 2 + 150) and (app.height / 2 + 50 <= mouseY and mouseY <= app.height / 2 + 150):
            setActiveScreen('menu')

def story_onStep(app):
    #function to move the player
    movePlayer(app)

    #Watch player health and end the game if they die
    if app.playerHealth == 0:
        app.gameOver = True
        app.stepsPerSecond = 1
    
    
    #Flash the screen red when the player gets hit
    damageAnimation(app)

    if isinstance(app.currentRoom, BossRoom):
        # Stores all bullets the player shoots for 2 seconds, and then shoots the bullets back out
        bossShoot(app)
        # If boss is enraged, start checking if the player is colliding with the lightning
        lightningCollision(app)

    # Mange player Iframes so they don't insta die
    playerImmuneFrames(app)

    # Check if the player is on the ground and change the players current velocity values
    updatePlayer(app)

    # Check if player's bullets are on screen and if so update their location, if not remove them to save memory
    updatePlayerBullets(app)
    # Check and update enemy bullets, also check if they are colliding with the player and if so damage the player
    updateEnemyBullets(app)

    # manages the enemies in the game
    for enemy in app.enemies:
        # Goes through each enemy and does different actions based on the type of enemy
        if isinstance(enemy, Liner):
            linerActions(app, enemy)
        elif isinstance(enemy, Ranger):
            rangerActions(app, enemy)
        elif isinstance(enemy, Boss):
            bossActions(app, enemy)
        else:
            seekerActions(app, enemy)

        # Checks if enemy is in contact with player
        enemyCollisionWithPlayer(app, enemy)
            
        # Checks if enemy's color isn't original, usually when it just got shot, and turns it back to its original color
        if enemy.fill != enemy.originalFill:
            enemy.fill = enemy.originalFill
        
        # Checks if any of the player's bullets hit any enemies
        for bullet in app.playerBullets:
            enemyCollisionWithBullet(app, enemy, bullet)          

# Creates a map that is randomaly generated, except for the doors as the doors are always in the same place with various different room objects containing enemies, doors, and platforms
def createMap(app):
    map = [[Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '0011'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1011'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1001')],
           [Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '0111'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1111'), Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1101')],
           [Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '0110'), Room([], createRoom(), '1110'),                                           Room(generateEnemies(randomEnemyCount(3, 5), app), createRoom(), '1100')]]
    return map

# Creates a list of two strings of length 3, each with 2 ones and 1 zero, with the 1s denoting where the platforms are and the 0 where the gap in the platforms is
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

# Draws a room based on the room variables such as the doors, door colors, and platforms based on their respective global and Room variables
def drawRoom(app, room):
    # These locals make life a lot easier and more intuitive to read in this function
    halfHeight = app.height / 2
    halfWidth = app.width / 2
    platformWidth = ((app.width - 100) / 3)

    # Goes through the room variable Room.doors which indicates where the doors are in the room and either draws a wall or a door
    # app.currentDoorColors loops through to see if there are enemies and colors the doors based on if there are or are not
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

    # loops through the variable that holds the platforms 'map' and draws them if there is a '1' there
    for i in range(2):
        for j in range(3):
            if app.currentRoom.map[i][j] == '1':
                drawRect(50 + platformWidth * j, 550 - 350 * i, platformWidth, 50, fill='brown')

# Loads all globals variables and updates them everytime the player enters a new room so that the other functions no what to base it off of
def loadRoom(app):
    #Reset platforms and bullets as they logically don't transfer between rooms, platformWidth variable makes programming some of this stuff easier to see
    app.currentPlatforms = []
    platformWidth = ((app.width - 100) / 3)
    app.playerBullets = []
    app.enemyBullets = []

    #Check to see if all rooms are cleared to know if the game should put up the boss prompt
    app.allRoomsCleared = roomsCleared(app)

    #Filter through and add all platforms to a list containing the top right and bottom left (makes it easier for collision) corner of all the platforms
    for i in range(2):
        for j in range(3):
            if app.currentRoom.map[i][j] == '1':
                app.currentPlatforms.append((50 + platformWidth * j, 550 - 350 * i, 50 + platformWidth * j + platformWidth, 550 - (350 * i) + 50)) # Convert to top left and bottom right

    #Spawn in the enmies (set them to the enemies in the current room)
    app.enemies = app.currentRoom.enemies

    # Create convenient local variables and erase old variables from previously loaded rooms
    halfHeight = app.height / 2
    halfWidth = app.width / 2
    doors = app.currentRoom.doors
    app.currentDoors = []
    app.currentDoorColors = ''

    # Adds the current door coordinates if their is a door, so game can check collision with doors easier
    # Also if there is a door, checks if there are enemies in the room in that corresponding direction, so it doesn't cause a index out of range error
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

# Generate the enemy objects to be added to the enemy list
def generateEnemies(enemyCount, app):
    enemies = []
    for i in range(enemyCount):
        randomEnemyIndex = math.floor(random.random() * 3) # Choose a random number so enemy type is different each time
        if randomEnemyIndex == 0: #create basic enemy
            enemies.append(Enemy(app, 5, 50, 5, 'purple'))
        elif randomEnemyIndex == 1: #create line enemy
            enemies.append(Liner(app, 7.5, 100, 10, 'green'))
        elif randomEnemyIndex == 2: #create ranger enemy
            enemies.append(Ranger(app, 2, 200, 10, 'violet'))
    return enemies

# Choose a random number of enemies between the min and the max
def randomEnemyCount(min, max):
    return rounded(random.random() * (max - min)) + min

# Draws hearts using draw polygon based on the number of health the player has left
def drawHealthBar(app):
    for i in range(app.playerHealth):
        drawHeart(50 + 50 * i, app.height - 40, 30, 40)

# Moves the player based on their dx and dy
def movePlayer(app):
    # Variables that make some of the code below a little bit clearer
    futurePX = app.px + (app.pdx / 5)
    futurePY = app.py + app.pdy
    currentPlayerBottom = app.py + app.pr
    futurePlayerBottom = futurePY + app.pr
    halfHeight = app.height / 2
    halfWidth = app.width / 2

    # Make a collision object, that way we don't have to run function multiple times, will store a true or false so we can still easily check, as well as the coordinates of the platform
    platformCollision = collisionWithPlatforms(app, futurePX, futurePY)
    doorCollision = collisionWithDoors(app, futurePX, futurePY)
    if platformCollision[0]: # If the player is colliding with a platform
        platform = platformCollision[1] # Coordinates of top left and bottom right of the platform the player is colliding with
        if app.pdy > 0 and futurePlayerBottom >= platform[1] and currentPlayerBottom < platform[1]: # If the player is falling down on a platform, then stop its dy and stop it from falling while treating platform like ground
            app.isFalling = False
            app.jumps = 2
            app.pdy = 0
            app.py = platform[1] - app.pr
            move(app)
        elif app.pdy <= 0 and currentPlayerBottom > platform[1]: # If player is colliding with a platform but the bottom isn't above the top of the platform, don't do anything
            move(app)
            fall(app)
        else:
            fall(app)
            move(app)
    elif doorCollision[0]: # If the player is colliding with a door
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
    else: # if not hitting a platform just move normally
        app.isFalling = True 
        fall(app)
        move(app)

# Update players dy and dx variables
def updatePlayer(app):
    # Check if the player is on the ground and if so stop from falling and refresh jumps
    if app.playerBottom >= app.height - 50:
        app.isOnGround = True
        app.isFalling = False
        app.pdy = 0
        app.jumps = 2

    # Change the players current velocity values
    app.pdx = app.pdx - (app.pdx / 5)
    if app.isFalling:
        app.pdy += 1

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

# Change the players position based on player's dy, manages collision with floor and ceiling
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
    if isHittingBoundary(futurePX, app): # Checks if the player is hitting the left or right walls
        dx = 0
    else:
        app.px = futurePX

# Checking if the player will be hitting a wall
def isHittingBoundary(px, app):
    doors = app.currentRoom.doors
    halfHeight = app.height / 2
    halfWidth = app.width / 2
    walls = []
    # Similar process to drawing the walls, but I am re-using the code to extract the points (top left and bottom right) for all the rectangles that are the walls
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
    for wall in walls:
        if playerIntersectingRectangle(px, app.py, app.pr, wall[0], wall[1], wall[2], wall[3]):
            if app.pdx > 0:
                app.px = wall[0] - app.pr
            elif app.pdx < 0:
                app.px = wall[2] + app.pr
            return True
    
    return False

#This function will be used to check collision between two circles
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

# Gets the distance from a circle to line segments, very important for checking collision between circle and the line segments of the traingle and even for boss lightning
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

# Checks if a bullet is colliding with the enemy which are triangles
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

# Based on the boss position and the target position of lightning, draws a polygon and uses that as a hitbox
def isCollidingWithLightning(lightningHitbox, app):

    #Just put the points in a list for simple and easy iteration
    points = [lightningHitbox[0], lightningHitbox[1], lightningHitbox[2], lightningHitbox[3]]
    
    # Check collision with vertices
    for point in points:
        if getDistance(app.px, app.py, point[0], point[1]) <= app.pr:
            return True
    
    # Check collision with edges, which are just the three different points I used to draw the triangle
    for point in points:
        for otherPoint in points:
            if point == otherPoint:
                pass
            if pointToSegmentDistance(app.px, app.py, point[0], point[1], otherPoint[0], otherPoint[1]) <= app.pr:
                return True
    
    # If it doesn't collide with any of the points or lines, it isn't colliding, thus it is false
    return False

# Similar to isCollidingWithEnemy, but just for the player
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

# Simple drawTriangle function to draw the enemies
def drawTriangle(centerX, centerY, side, fill, angle, border=None):
    height = (side * math.sqrt(3) / 2)
    if border == None:
        drawPolygon(centerX - side / 2, centerY - height / 2, centerX + side / 2, centerY - height / 2, centerX, centerY + height / 2, fill=fill, rotateAngle=angle)
    elif border != None:
        drawPolygon(centerX - side / 2, centerY - height / 2, centerX + side / 2, centerY - height / 2, centerX, centerY + height / 2, fill=fill, rotateAngle=angle, border=border, borderWidth=2)

# Like loadRoom, but specialized for the BossRoom
def loadBossRoom(bossRoom, app):
    app.background = gradient('gray', 'white')
    app.currentBackgroundColor = app.background
    app.currentRoom = bossRoom
    app.enemies = [Boss(app)]
    app.currentPlatforms = []
    app.recentShots = []

    app.currentDoors = []
    app.playerBullets = []
    app.enemyBullets = []

    app.px = app.width / 2
    app.pr = 30
    app.py = app.floorPlatformY - app.pr
    app.pdy = 0
    app.pdx = 0

# Draws the special BossRoom
def drawBossRoom(app):
    drawRect(0, 0, 50, app.height)
    drawRect(0, 0, app.width, 50)
    drawRect(app.width - 50, 0, app.width, app.height)
    drawRect(0, app.height - 50, app.width, app.height)
    drawBossHealthBar(app)

# generates the points that will be used to draw the lightning
def generateLightningPoints(startX, startY, targetX, targetY, totalPoints):
    return generateLightningPointsHelper(startX, startY, startX, startY, targetX, targetY, totalPoints, totalPoints, [])

# Recursive function that creates all the points
def generateLightningPointsHelper(startX, startY, currentX, currentY, targetX, targetY, totalPoints, currentPoints, cords):
    # If there are no more points to draw, return the coordinates of the points
    if currentPoints == 0:
        cords.append((targetX, targetY))
        return cords
    
    # Keeps drawing until all points are drawn
    else:
        cords.append((currentX, currentY))

        # These variables keep the lightning on track
        distance = getDistance(startX, startY, targetX, targetY)
        angle = calculateTheta(startX, startY, targetX, targetY)
        dx = math.cos(angle) * (distance / totalPoints)
        dy = math.sin(angle) * (distance / totalPoints)

        # Makes sure that the points keep travleing relativelely towards the player, or else some lightning could look really weird
        minYThreshold = startY + (dy * (totalPoints - currentPoints))
        minXThreshold = startX + (dx * (totalPoints - currentPoints))
        
        # If dx or dy is to small, some lightning becomes too straight, if that's the case just draws with fixed range
        if abs(dx) < 30:
            currentX = minXThreshold + ((random.random() * 60 - 30) * 3)
        else:
            currentX = minXThreshold + (random.random() * dx * 3)
        if abs(dy) < 30:
            currentY = minYThreshold + ((random.random() * 60 - 30) * 3)
        else:
            currentY = minYThreshold + (random.random() * dy * 3)

        return generateLightningPointsHelper(startX, startY, currentX, currentY, targetX, targetY, totalPoints, currentPoints - 1, cords)

# Draws the boss prompt where the player can click to start the boss 
def drawBossPrompt(app):
    if app.allRoomsCleared and not isinstance(app.currentRoom, BossRoom):
        drawRect(app.width / 2 - 300, app.height / 2 - 300, 600, 600, fill=gradient('black', 'crimson'), borderWidth=10, border='black')
        drawLabel('An ominous figure awaits,', app.width / 2, app.height / 2 - 100, size=36, bold=True, italic=True, fill='gainsboro')
        drawLabel('but it reminds you of someone...', app.width / 2, app.height / 2 - 60, size=36, bold=True, italic=True, fill='gainsboro')
        drawRect(app.width / 2 - 200, app.height / 2 + 100, 400, 100, fill=gradient('white', 'gray'), border='black', borderWidth=10)
        drawLabel('Continue to your fate', app.width / 2, app.height / 2 + 150, size=30, fill='darkRed', bold=True)

# Draws the boss' health bar at the top of the boss room
def drawBossHealthBar(app):
    boss = app.enemies[0]
    drawRect(app.width / 2 - 200, 10, 400, 30, fill='lightGray')
    drawRect(app.width / 2 - 200, 10, (boss.health) * (400 / boss.maxHealth), 30, fill=gradient('crimson', 'darkRed'))
    drawRect(app.width / 2 - 150, 40, 300, 40, fill='black')
    drawRect(app.width / 2 - 145, 44, 290, 32, fill='gray')
    drawLabel('You?', app.width / 2, 60, fill='black', bold=True, italic=True, size=36)
    drawLabel(f'{boss.health}', app.width / 2, 25, size=24, bold=True)

# Shoots bullets at all the stored positions that the player used to be at
def bossShoot(app):
    boss = app.enemies[0]
    if boss.count == 0:
        # Boss shoots all bullets stored back at the player
        for cord in app.currentShots:
            app.enemyBullets.append(EnemyBullet(boss.x, boss.y, cord[0], cord[1], 15, 10))
        # Resets and starts storing new bullets for cycle
        app.currentShots = []

# Check if the player is colliding with the lightningHitbox
def lightningCollision(app):
    boss = app.enemies[0]
    if boss.isEnraged:
            if app.lightningHitbox != []:
                if not app.playerImmune and isCollidingWithLightning(app.lightningHitbox, app):
                    app.playerHealth -= 1
                    app.background = 'crimson'
                    app.playerImmune = True

# Helper function to just draw a heart, used in draw health bar
def drawHeart(topLeftX, topLeftY, height, width):
    drawPolygon(topLeftX, topLeftY, topLeftX + width / 4, topLeftY - height / 4, topLeftX + width / 2, topLeftY, topLeftX + (3 * (width / 4)), topLeftY - height / 4, topLeftX + width, topLeftY, topLeftX + width / 2, topLeftY + height * (3 / 4), fill='red') 

# Check if all the rooms were cleared
def roomsCleared(app):
    for floor in app.map:
        for room in floor:
            if room.enemies != []:
                return False
    return True

# Simply calculates the angle between two points
def calculateTheta(x, y, targetX, targetY):
    adjacent = targetX - x
    opposite = targetY - y
    theta = math.atan2(opposite, adjacent)
    return theta

# Flashes the screen when the player takes damage
def damageAnimation(app):
    if app.background != app.currentBackgroundColor or app.screenFlashCount != 0:
        if app.screenFlashCount == 20:
            app.background = app.currentBackgroundColor
            app.screenFlashCount = 0
        elif app.screenFlashCount % 5 == 0:
            app.background = app.currentBackgroundColor
            app.screenFlashCount += 1
        else:
            app.background = 'crimson'
            app.screenFlashCount += 1

# Draw the line showing where the lightning will strike and draws the lightning
def drawLightningMechanics(app):
    boss = app.enemies[0]
    if boss.isEnraged:
        if boss.targetX != None and boss.targetY != None:
            if app.lightningBullets == []:
                drawLine(boss.x, boss.y, boss.targetX, boss.targetY, fill='mediumSlateBlue', lineWidth=10)
            elif app.lightningBullets != []:
                for i in range(len(app.lightningBullets)):
                    for j in range(1, len(app.lightningBullets[i])):
                        drawLine(app.lightningBullets[i][j-1][0], app.lightningBullets[i][j-1][1], app.lightningBullets[i][j][0], app.lightningBullets[i][j][1], fill='mediumSlateBlue')
      
def drawGameOverPrompt(app):
    if app.gameOver == True:
        drawRect(app.width / 2 - 200, app.height / 2 - 300, 400, 600, border='red', borderWidth=5)
        drawLabel('GAME OVER', app.width / 2, app.height / 2 - 200, fill='red', size=48)
        drawRect(app.width / 2 - 150, app.height / 2 + 50, 300, 100, border='white', borderWidth=5, fill='black')
        drawLabel('Exit to menu', app.width / 2, app.height / 2 + 100, fill='white', size=36, bold=True)

def drawBullets(app):
    for bullet in app.enemyBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            drawCircle(bullet.x, bullet.y, bullet.radius, fill=bullet.fill)

    for bullet in app.playerBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            drawCircle(bullet.x, bullet.y, bullet.radius, fill=bullet.fill)

def updatePlayerBullets(app):
    for bullet in app.playerBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
        else:
            app.playerBullets.remove(bullet)

def updateEnemyBullets(app):
    for bullet in app.enemyBullets:
        if bullet.x > 0 and bullet.x < app.width and bullet.y > 0 and bullet.y < app.height:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
            if circleCollidingCircle(app.px, app.py, app.pr, bullet.x, bullet.y, bullet.radius) and app.playerImmune == False:
                app.playerHealth -= 1
                app.playerImmune = True
                app.background = 'crimson'
        else:
            app.enemyBullets.remove(bullet)

def drawEnemies(app):
    for enemy in app.enemies:
        if isinstance(enemy, Ranger):
            drawTriangle(enemy.x, enemy.y, enemy.size, enemy.fill, 0)
            #save if want to change drawing of ranger or different enemy types
        elif isinstance(enemy, Boss):
            drawCircle(enemy.x, enemy.y, enemy.size, fill=enemy.fill)
        else:
            drawTriangle(enemy.x, enemy.y, enemy.size, enemy.fill, enemy.rotateAngle)

def playerImmuneFrames(app):
    if app.playerImmune == True:
        app.pcolor = 'gray'
        if app.iFrameCount == app.stepsPerSecond * 2:
            app.playerImmune = False
            app.iFrameCount = 0
            app.pcolor = 'blue'
        app.iFrameCount += 1

def linerActions(app, enemy):
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

def rangerActions(app, enemy):
    if enemy.count == 0:
        app.enemyBullets.append(EnemyBullet(enemy.x, enemy.y, app.px, app.py, 10, 50))
        enemy.count = app.stepsPerSecond * 2
        enemy.updateTarget(app)
        enemy.x += enemy.dx
        enemy.y += enemy.dy
    else:
        enemy.x += enemy.dx
        enemy.y += enemy.dy
        enemy.count -= 1

# makes the Boss shoot every 2 seconds and shoot lightning if it is enraged
def bossActions(app, enemy):
    if not enemy.isEnraged:
        if enemy.health == 50:
            enemy.x = app.width / 2
            enemy.y = app.height / 2
            enemy.count = 30
            enemy.fill = 'crimson'
            enemy.originalFill = 'crimson'
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
            app.lightningHitbox = []
            for i in range(5):
                distance = getDistance(enemy.x, enemy.y, enemy.targetX, enemy.targetY)
                angle = calculateTheta(enemy.x, enemy.y, enemy.targetX, enemy.targetY)
                dx = math.cos(angle) * (distance / 15)
                dy = math.sin(angle) * (distance / 15)
                if app.lightningHitbox == []:
                    if abs(dx) < 30:
                        app.lightningHitbox.extend([(enemy.x + 90, enemy.y), (enemy.targetX - 90, enemy.targetY)])
                    else:
                        app.lightningHitbox.extend([(enemy.x + dx, enemy.y), (enemy.targetX - dx, enemy.targetY)])
                    if abs(dy) < 30:
                        app.lightningHitbox.insert(1, (enemy.x, enemy.y + 90))
                        app.lightningHitbox.append((enemy.targetX, enemy.targetY - 90))
                    else:
                        app.lightningHitbox.insert(1, (enemy.x, enemy.y + 90))
                        app.lightningHitbox.append((enemy.targetX, enemy.targetY - dy))
                app.lightningBullets.append(generateLightningPoints(enemy.x, enemy.y, enemy.targetX, enemy.targetY, 15))
                enemy.count = 120
        elif enemy.count == 115:
            app.lightningBullets = []
            for i in range(5):
                app.lightningBullets.append(generateLightningPoints(enemy.x, enemy.y, enemy.targetX, enemy.targetY, 15))
            enemy.count -= 1
        elif enemy.count == 110:
            app.lightningBullets = []
            for i in range(5):
                app.lightningBullets.append(generateLightningPoints(enemy.x, enemy.y, enemy.targetX, enemy.targetY, 15))
            enemy.count -= 1
        elif enemy.count == 30:
            app.lightningBullets = []
            enemy.targetPlayer(app)
            enemy.count -= 1
        else:
            enemy.count -= 1

# Makes the seeker enemy keep following current player location
def seekerActions(app, enemy):
    enemy.updateTarget(app)
    enemy.x += enemy.dx
    enemy.y += enemy.dy
    enemy.rotateAngle += 15

def enemyCollisionWithPlayer(app, enemy):
    if app.playerImmune == False:
        if isCollidingWithPlayer(enemy, app):
            app.playerHealth -= 1
            app.playerImmune = True
            app.background = 'crimson'

def enemyCollisionWithBullet(app, enemy, bullet):
    if isinstance(enemy, Boss):
        if circleCollidingCircle(bullet.x, bullet.y, bullet.radius, enemy.x, enemy.y, enemy.size):
            enemy.health -= 1
            if enemy.health == 0:
                setActiveScreen('win')
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

cmu_graphics.runAppWithScreens(initialScreen='menu')