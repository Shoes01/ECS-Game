import colorsys

class RenderComponent:
    ' Component that holds the graphical information of the entity. '
    def __init__(self, render_data):
        self.char = render_data.char
        self.codepoint = render_data.codepoint
        self.color_bg = render_data.color_bg
        self.color_explored = render_data.color_explored
        self.color_fg = render_data.color_fg
        self.color_highlight = render_data.color_highlight
        self.explored = render_data.explored
        self.stairs = render_data.stairs
        self.visible = render_data.visible

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