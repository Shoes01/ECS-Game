class RenderComponent():
    def __init__(self, color_bg, char, codepoint, color_fg, color_explored, explored=False, visible=False):
        self.color_bg = (0, 0, 0) if color_bg is None else color_bg
        self.char = "#" if char is None else char
        self.codepoint = 923 if codepoint is None else codepoint
        self.color_fg = (255, 255, 255) if color_fg is None else color_fg
        self.explored = explored
        self.color_explored = (100, 100, 100) if color_explored is None else color_explored
        self.visible = visible
        self.highlight_color = False