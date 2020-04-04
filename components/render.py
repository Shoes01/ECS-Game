import colorsys

class RenderComponent:
    ' Component that holds the graphical information of the entity. '
    def __init__(self, char, color_bg, color_explored, color_fg, color_highlight, codepoint, explored, stairs, visible):
        self.char = char
        self.codepoint = codepoint
        self.codepoint_highlight = codepoint
        self.color_bg = color_bg
        self.color_explored = color_explored
        self.color_fg = color_fg
        self.color_highlight = color_highlight
        self.explored = explored
        self.stairs = stairs
        self.visible = visible

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