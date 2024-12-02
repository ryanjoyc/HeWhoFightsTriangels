class Room:
    def __init__(self, player, enemies, map, doors):
        self.player = player
        self.enemies = enemies
        self.map = map
        self.doors = doors

class BossRoom(Room):
    def __init__(self, player, enemies, map, doors):
        super().__init__(player, enemies, map, doors)
        
