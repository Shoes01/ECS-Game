class Camera:
    def __init__(self, w, h, x=0, y=0, leash=10):
        self.x = x # Top left coordinate.
        self.y = y
        self.width = w
        self.height = h
        self.leash = leash # Leash is calculated as a radius from the center. Manhattan distance.