class Tile():
    def __init__(self, blocks_path=True, blocks_sight=True, explored=False):
        self.blocks_path = blocks_path
        self.blocks_sight = blocks_sight
        self.explored = explored