class Room:
    def __init__(self, enemies, map, doors):
        self.enemies = enemies
        self.map = map
        self.doors = doors

class BossRoom(Room):
    def __init__(self, enemies, map, doors):
        self.enemies = []
        self.map = []
        self.doors = ''
        

