class Room: # Room class used to manage enemies and the layout of the rooms
    def __init__(self, enemies, map, doors):
        self.enemies = enemies
        self.map = map
        self.doors = doors

class BossRoom(Room):
    def __init__(self, level=1):
        self.enemies = []
        self.map = []
        self.doors = '0000'
        

