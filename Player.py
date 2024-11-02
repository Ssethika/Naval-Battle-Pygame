class Player:
    def __init__(self, terrain, name):
        self.terrain = terrain
        self.score = 0
        self.name = name
        self.shots = 0

    def __repr__(self):
        return f"{self.name}"