class RenderComponent():
    def __init__(self, char='#', color=(255, 255, 255), explored=False, explored_color=(100, 100, 100), visible=False):
        self.char = char
        self.color = color
        self.explored = explored
        self.explored_color = explored_color
        self.visible = visible