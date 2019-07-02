import colorsys
import tcod
import tcod.event
import tcod.tileset
import numpy as np
from PIL import Image

# Prepare the console.
tcod.console_set_custom_font('16x16-sb-ascii.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)
console = tcod.console_init_root(70, 40, title='Tileset Explorer', order='F', renderer=tcod.RENDERER_SDL2, vsync=True)

# Prepare constants.
COLOR_THEME = {
    "Black": (36,36,38),
    "Blue": (0,129,255),
    "BrightBlack": (84,84,84),
    "BrightBlue": (0,0,255),
    "BrightCyan": (0,205,205),
    "BrightGreen": (0,238,0),
    "BrightMagenta": (255,0,255),
    "BrightRed": (255,0,0),
    "BrightWhite": (255, 255, 255),
    "BrightYellow": (255, 255, 0),
    "Cyan": (0,139,139),
    "Green": (0,139,0),
    "Magenta": (188,0,202),
    "Red": (159,0,0),
    "White": (187,187,187),
    "Yellow": (255,207,0),
    "Background": (0, 0, 0)
}
codepoint, fg_pos, bg_pos, bg_h_pos, bg_s_pos, bg_v_pos, fg_h_pos, fg_s_pos, fg_v_pos = (0,)*9
fg_edit = False
bg_edit = False
running = True
fg_column = True
pos = 0 # H S V position.
state = "codepoint" # States are "codepoint", "rgb", "hsv".
color_list = []
for k, value in COLOR_THEME.items():
    color_list.append(k)

# Helper functions.
def prepare_font(t, w, h):
    iterator = 0
    cp437 = np.array(
        [
            0x0000, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022,
            0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C,
            0x25BA, 0x25C4, 0x2195, 0x203C, 0x00B6, 0x00A7, 0x25AC, 0x21A8,
            0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC,
            0x0020, 0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027,
            0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x002D, 0x002E, 0x002F,
            0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037,
            0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F,
            0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047,
            0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F,
            0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057,
            0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x005F,
            0x0060, 0x0061, 0x0062, 0x0063, 0x0064, 0x0065, 0x0066, 0x0067,
            0x0068, 0x0069, 0x006A, 0x006B, 0x006C, 0x006D, 0x006E, 0x006F,
            0x0070, 0x0071, 0x0072, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077,
            0x0078, 0x0079, 0x007A, 0x007B, 0x007C, 0x007D, 0x007E, 0x007F,
            0x00C7, 0x00FC, 0x00E9, 0x00E2, 0x00E4, 0x00E0, 0x00E5, 0x00E7,
            0x00EA, 0x00EB, 0x00E8, 0x00EF, 0x00EE, 0x00EC, 0x00C4, 0x00C5,
            0x00C9, 0x00E6, 0x00C6, 0x00F4, 0x00F6, 0x00F2, 0x00FB, 0x00F9,
            0x00FF, 0x00D6, 0x00DC, 0x00A2, 0x00A3, 0x00A5, 0x20A7, 0x0192,
            0x00E1, 0x00ED, 0x00F3, 0x00FA, 0x00F1, 0x00D1, 0x00AA, 0x00BA,
            0x00BF, 0x2310, 0x00AC, 0x00BD, 0x00BC, 0x00A1, 0x00AB, 0x00BB,
            0x2591, 0x2592, 0x2593, 0x2502, 0x2524, 0x2561, 0x2562, 0x2556,
            0x2555, 0x2563, 0x2551, 0x2557, 0x255D, 0x255C, 0x255B, 0x2510,
            0x2514, 0x2534, 0x252C, 0x251C, 0x2500, 0x253C, 0x255E, 0x255F,
            0x255A, 0x2554, 0x2569, 0x2566, 0x2560, 0x2550, 0x256C, 0x2567,
            0x2568, 0x2564, 0x2565, 0x2559, 0x2558, 0x2552, 0x2553, 0x256B,
            0x256A, 0x2518, 0x250C, 0x2588, 0x2584, 0x258C, 0x2590, 0x2580,
            0x03B1, 0x00DF, 0x0393, 0x03C0, 0x03A3, 0x03C3, 0x00B5, 0x03C4,
            0x03A6, 0x0398, 0x03A9, 0x03B4, 0x221E, 0x03C6, 0x03B5, 0x2229,
            0x2261, 0x00B1, 0x2265, 0x2264, 0x2320, 0x2321, 0x00F7, 0x2248,
            0x00B0, 0x2219, 0x00B7, 0x221A, 0x207F, 0x00B2, 0x25A0, 0x00A0,
        ], order='F'
    )

    im = Image.open('16x16-sb-ascii.png').convert('RGBA')
    nim = np.array(im)[:, :, 0] # Remove the rgba component.

    dim = 16
    for x in range(0, dim):
        for y in range(0, dim):
            x_0 = x*w
            x_1 = (x+1)*w
            y_0 = y*h
            y_1 = (y+1)*h
            t.set_tile(cp437[iterator], nim[x_0:x_1, y_0:y_1])
            iterator += 1

def prepare_tilesheet(t, w, h):
    # w, h = 16, 16
    im = Image.open('ken_monochrome.png').convert('RGBA')
    nim = np.array(im)[:, :, 0] # Remove the rgba component.
    tx, ty = nim.shape
    codepoint = ord(u'\ue000') # This is the beginning of the Unicode Private Use Area. It is 57344.

    print(f"Shape: {tx} by {ty}")

    for x in range(0, tx):
        if x % (w+1) == 0:
            for y in range(0, ty):
                if y % (h+1) == 0:
                    x_0 = x
                    x_1 = x+w
                    y_0 = y
                    y_1 = y+h
                    if codepoint - 57344 > 500: print(f"Codepoint: {codepoint - 57344}. w: {x_1}-{x_0}, h:{y_1}-{y_0}.")
                    t.set_tile(codepoint, nim[x_0:x_1, y_0:y_1])
                    codepoint += 1

def handle_input(bg_pos, codepoint, fg_column, fg_pos, running, state, bg_h_pos, bg_s_pos, bg_v_pos, fg_h_pos, fg_s_pos, fg_v_pos, pos):
    key = None
    key_char = None
    key_scancode = None

    for event in tcod.event.get():
        if event.type == "KEYDOWN":
            key = event
    
    try:    
        key_char = chr(key.sym)
    except:
        key_char = None
    
    if key:
        key_scancode = key.scancode
    
    # Global keys.
    if key_char == "x" or key_char == "q":
        running = False
    elif key_char == "c":
        state = "codepoint"
    elif key_char == "r":
        state = "rgb"
    elif key_char == "h":
        state = "hsv"

    # Handle codepoint input.
    if state == "codepoint":
        if key_char == "c":
            codepoint = int(input('Choose codepoint value between 0 and 1023.'))
        elif key_scancode == tcod.event.SCANCODE_UP:
            codepoint -= 32
        elif key_scancode == tcod.event.SCANCODE_DOWN:
            codepoint += 32
        elif key_scancode == tcod.event.SCANCODE_RIGHT:
            codepoint += 1
        elif key_scancode == tcod.event.SCANCODE_LEFT:
            codepoint -= 1

        # Ensure codepoint is within the tilesheet.
        if codepoint < 0:
            codepoint = 1024 + codepoint
        elif codepoint > 1023:
            codepoint = codepoint - 1024

    # Handle rgb input.
    elif state == "rgb":
        direction = 0
        if key_scancode == tcod.event.SCANCODE_UP:
            direction -= 1
        elif key_scancode == tcod.event.SCANCODE_DOWN:
            direction += 1
        elif key_scancode == tcod.event.SCANCODE_RIGHT:
            fg_column = not fg_column
        elif key_scancode == tcod.event.SCANCODE_LEFT:
            fg_column = not fg_column

        if fg_column:
            fg_pos += direction
            
            if fg_pos < 0:
                fg_pos = len(color_list) - 1
            elif fg_pos > len(color_list) - 1:
                fg_pos = 0
        else:
            bg_pos += direction

            if bg_pos < 0:
                bg_pos = len(color_list) - 1
            elif bg_pos > len(color_list) - 1:
                bg_pos = 0

    # Handle hsv input.
    elif state == "hsv":
        direction = 0
        # Handle input.
        if key_scancode == tcod.event.SCANCODE_UP:
            direction += 10
        elif key_scancode == tcod.event.SCANCODE_DOWN:
            direction -= 10
        elif key_scancode == tcod.event.SCANCODE_RIGHT:
            pos += 1
            if pos == 3: pos = 0
        elif key_scancode == tcod.event.SCANCODE_LEFT:
            pos -= 1
            if pos == -1: pos = 2
        elif key_scancode == tcod.event.SCANCODE_SPACE:
            fg_column = not fg_column
        
        if fg_column:
            if pos == 0:
                fg_h_pos += direction
                if fg_h_pos < 0:
                    fg_h_pos = 100
                elif fg_h_pos > 100:
                    fg_h_pos = 0
            elif pos == 1:
                fg_s_pos += direction
                if fg_s_pos < 0:
                    fg_s_pos = 100
                elif fg_s_pos > 100:
                    fg_s_pos = 0
            elif pos == 2:
                fg_v_pos += direction
                if fg_v_pos < 0:
                    fg_v_pos = 100
                elif fg_v_pos > 100:
                    fg_v_pos = 0
        else:
            if pos == 0:
                bg_h_pos += direction
                if bg_h_pos < 0:
                    bg_h_pos = 100
                elif bg_h_pos > 100:
                    bg_h_pos = 0
            elif pos == 1:
                bg_s_pos += direction
                if bg_s_pos < 0:
                    bg_s_pos = 100
                elif bg_s_pos > 100:
                    bg_s_pos = 0
            elif pos == 2:
                bg_v_pos += direction
                if bg_v_pos < 0:
                    bg_v_pos = 100
                elif bg_v_pos > 100:
                    bg_v_pos = 0
    
    return bg_pos, codepoint, fg_column, fg_pos, running, state, bg_h_pos, bg_s_pos, bg_v_pos, fg_h_pos, fg_s_pos, fg_v_pos, pos

def print_codepoint():
    console.print(19, 2, f"Codepoint: {codepoint:>4}")
    for row in range(0, len(color_list)):
        for col in range(0, len(color_list)):
            x = 19 + row
            y = 3 + col
            console.tiles["ch"][x, y] = 57344 + codepoint
            console.tiles["fg"][x, y] = COLOR_THEME[color_list[row]] + (255,)
            console.tiles["bg"][x, y] = COLOR_THEME[color_list[col]] + (255,)
    
    x0 = 37
    y0 = 3
    cp = 0
    row_max, col_max = 32, 32
    for col in range(0, col_max):
        for row in range(0, row_max):
            x = x0 + row
            y = y0 + col
            console.tiles["ch"][x, y] = 57344 + cp
            console.tiles["fg"][x, y] = (255, 255, 255, 255)
            console.tiles["bg"][x, y] = (0, 0, 0, 255)
            if cp == codepoint:
                console.tiles["fg"][x, y] = (0, 0, 0, 255)
                console.tiles["bg"][x, y] = (255, 255, 255, 255)
            cp += 1

def print_rgb():
    fg_color = (255, 255, 255)
    bg_color = (255, 255, 255)
    
    if not fg_column:
        fg_color = (155, 155, 155)
    else:
        bg_color = (155, 155, 155)
    
    console.print(19, 2, f" fg ", fg_color)
    console.print(23, 2, f" bg ", bg_color)
    x, y = 19, 3
    for row in range(0, len(color_list)):
        fg_tick = "  "
        bg_tick = "  "
        if fg_pos == row:
            fg_tick = "--"
        if bg_pos == row:
            bg_tick = "--"
        console.print(x, y + row, f"[{fg_tick}][{bg_tick}]", bg=COLOR_THEME[color_list[row]])

    x0 = 37
    y0 = 3
    cp = 0
    row_max, col_max = 32, 32
    for col in range(0, col_max):
        for row in range(0, row_max):
            x = x0 + row
            y = y0 + col
            console.tiles["ch"][x, y] = 57344 + cp
            console.tiles["fg"][x, y] = COLOR_THEME[color_list[fg_pos]] + (255,)
            console.tiles["bg"][x, y] = COLOR_THEME[color_list[bg_pos]] + (255,)
            cp += 1

def print_hsv():
    br, bg, bb = colorsys.hsv_to_rgb(bg_h_pos/100, bg_s_pos/100, bg_v_pos/100)
    fr, fg, fb = colorsys.hsv_to_rgb(fg_h_pos/100, fg_s_pos/100, fg_v_pos/100)
    
    fg_color = (255, 255, 255)
    bg_color = (255, 255, 255)

    if not fg_column:
        fg_color = (155, 155, 155)
    else:
        bg_color = (155, 155, 155)

    console.print(19, 1, f"FG HSV color: ({fg_h_pos:>3}, {fg_s_pos:>3}, {fg_v_pos:>3})", fg_color)
    console.print(19, 2, f"BG HSV color: ({bg_h_pos:>3}, {bg_s_pos:>3}, {bg_v_pos:>3})", bg_color)

    x0 = 37
    y0 = 3
    cp = 0
    row_max, col_max = 32, 32
    for col in range(0, col_max):
        for row in range(0, row_max):
            x = x0 + row
            y = y0 + col
            console.tiles["ch"][x, y] = 57344 + cp
            console.tiles["fg"][x, y] = (fr*255, fg*255, fb*255, 255)
            console.tiles["bg"][x, y] = (br*255, bg*255, bb*255, 255)
            cp += 1


# Prepare the font, and the tilesheet.
w, h = 16, 16
t = tcod.tileset.Tileset(w, h)

prepare_font(t, w, h)
prepare_tilesheet(t, w, h)
tcod.tileset.set_default(t)

# Run the explorer.
while running:
    # Static content.
    console.print(0, 0, "Welcome to the Tileset Explorer.")

    count = 0
    for k, value in COLOR_THEME.items():
        console.print(1, 3 + count, f"{count:>2}: {k}")
        count += 1

    # Handle input.
    bg_pos, codepoint, fg_column, fg_pos, running, state, bg_h_pos, bg_s_pos, bg_v_pos, fg_h_pos, fg_s_pos, fg_v_pos, pos = handle_input(bg_pos, codepoint, fg_column, fg_pos, running, state, bg_h_pos, bg_s_pos, bg_v_pos, fg_h_pos, fg_s_pos, fg_v_pos, pos)

    # Print things.
    if state == "codepoint":
        print_codepoint()
    elif state == "rgb":
        print_rgb()
    elif state == "hsv":
        print_hsv()

    # Send to console.
    console.blit(console, 0, 0)
    tcod.console_flush()
    console.clear()
