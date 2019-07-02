class RenderComponent():
    def __init__(self, bg_color, char, codepoint, color, explored_color, explored=False, visible=False):
        self.bg_color = (0, 0, 0) if bg_color is None else bg_color
        self.char = "#" if char is None else char
        self.codepoint = 57344 + 923 if codepoint is None else 57344 + codepoint
        self.color = (255, 255, 255) if color is None else color
        self.explored = explored
        self.explored_color = (100, 100, 100) if explored_color is None else explored_color
        self.visible = visible
        self.highlight_color = False