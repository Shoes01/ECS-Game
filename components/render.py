import colorsys

from _data import ENTITY_COLORS

class RenderComponent:
    ' Component that holds the graphical information of the entity. '
    def __init__(self, color_bg, char, codepoint, color_fg, color_explored, explored=False, visible=False):
        self.char = "#" if char is None else char
        self.codepoint = 923 if codepoint is None else codepoint
        self.color_fg = ENTITY_COLORS['floor'] if color_fg is None else color_fg
        self.color_bg = ENTITY_COLORS['floor_bg'] if color_bg is None else color_bg
        self.color_explored = ENTITY_COLORS['floor_explored'] if color_explored is None else color_explored
        self.explored = explored
        self.visible = visible
        self.highlight_color = False

        ' Convert colors from hsv to rgb, if applicable. '
        self.color_fg = convert_color(self.color_fg)
        self.color_bg = convert_color(self.color_bg)
        self.color_explored = convert_color(self.color_explored)

def convert_color(rgb_color):
    if rgb_color[-1] == 'hsv':
        color = [x / 100.0 for x in rgb_color[0:3]]
        color = colorsys.hsv_to_rgb(color[0], color[1], color[2])
        rgb_color = tuple([int(x * 255) for x in color])
    return rgb_color