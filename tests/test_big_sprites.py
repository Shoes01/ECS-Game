import colorsys
import tcod
import tcod.event
import tcod.tileset
import numpy as np

from PIL import Image
from time import sleep


# Prepare the console.
tcod.console_set_custom_font('16x16-sb-ascii.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)
console = tcod.console_init_root(70, 40, title='Tileset Explorer', order='F', renderer=tcod.RENDERER_OPENGL2, vsync=True)

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

multiplier = 8

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
    # This image is twice as big as usual. 
    # # It is 1086x1086. It is a 32x32 tilesheet, but each tile is split into four, so it's actually a 64x64 tilesheet.
    t_w, t_h = 16 * multiplier, 16 * multiplier # 16x multiplier
    im = None
    if multiplier == 2:
        im = Image.open('big_ken_mono.png').convert('RGBA')
    if multiplier == 4:
        im = Image.open('4x_ken_m.png').convert('RGBA')
    if multiplier == 8:
        im = Image.open('8x_ken_m.png').convert('RGBA')
    nim = np.array(im)[:, :, 0] # Remove the rgba component.
    tx, ty = nim.shape
    codepoint = ord(u'\uf000') # This is the beginning of the Unicode Private Use Area. It is 57344.

    print(f"Shape: {tx} by {ty}")

    big_array = []

    for x in range(0, tx):
        if x % ((w+1)*multiplier) == 0:
            for y in range(0, ty):
                if y % ((h+1)*multiplier) == 0:
                    x_0 = x
                    x_1 = x+t_w
                    y_0 = y
                    y_1 = y+t_h
                    big_array.append(nim[x_0:x_1, y_0:y_1])
                    
    for tile in big_array: # Multiplier squared # Might be able to automate with two for loops.
        for x in range(0, multiplier):
            for y in range(0, multiplier):
                x_0, x_1 = 16 * x, 16 * (x + 1)
                y_0, y_1 = 16 * y, 16 * (y + 1)
                t.set_tile(codepoint, tile[x_0:x_1, y_0:y_1])
                codepoint += 1
        
def place_tile(x, y, codepoint, fg, bg): # Multiplier squared # Might be able to automate with two for loops
    iter = 0
    for yy in range(0, multiplier):
        for xx in range(0, multiplier):
            console.tiles["ch"][x + xx, y + yy] = 57344 + codepoint*multiplier*multiplier + iter
            console.tiles["fg"][x + xx, y + yy] = fg
            console.tiles["bg"][x + xx, y + yy] = bg
            iter += 1

# Prepare the font, and the tilesheet.
w, h = 16, 16
t = tcod.tileset.Tileset(w, h)

prepare_font(t, w, h)
prepare_tilesheet(t, w, h)
tcod.tileset.set_default(t)

codepoint = 0
while running:
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
    
    # Print things.
    console.print(0, 0, f"Welcome.")

    place_tile(x=0, y=3, codepoint=codepoint, fg=(255, 255, 255, 255), bg=(0, 0, 0, 255))
    codepoint += 1
    sleep(0.1) 
    
    # Send to console.
    console.blit(console, 0, 0)
    tcod.console_flush()
    console.clear()



### TODO
# Cut up the tilesheet into 2x2 np.arrays
# Cut each array into 4 pieces, codepointed sequentially, and loaded into the tcod tilesheet
# Create a function that interprets the requested codepoint
### Codepoint 4 will actually point to 16, and get 16/17/18/19 and print them