class Room:
    def __init__(self, enemies, map, doors):
        self.enemies = enemies
        self.map = map
        self.doors = doors

class BossRoom(Room):
    def __init__(self, level=1):
        self.enemies = []
        self.map = ['1000000001', '1100000011', '1110000111']
        self.doors = '0000'
        

