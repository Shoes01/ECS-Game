import numpy as np

from _helper_functions import as_integer
from components.soul import SoulComponent
from data.render import UI_COLORS

def render_soul_sheet(console_object, soul, world):
    console, _, _, w, h = console_object
    color_fg = UI_COLORS['text']
    new_soul = soul
    player_soul = world.component_for_entity(1, SoulComponent).soul
    titles = {
        'hp': 'Health:',
        'attack': 'Attack:',
        'magic': 'Magic:',
        'speed': 'Speed:',
        'defense': 'Defense:',
        'resistance': 'Resist:'
        }

    # Draw sheet.
    console.draw_frame(x=0, y=0, width=w, height=h, title="Soul Consumption", clear=True, fg=UI_COLORS['fg'], bg=UI_COLORS['bg'])

    # Print player soul and new soul.
    x, y = 3, 5
    offset = 30
    row = 0
    col = 0
    console.print(x - 1, y - 1, 'New Player Soul:', color_fg)
    console.print(x - 1 + offset, y - 1, 'Incoming Soul:', color_fg)

    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {as_integer(player_soul[key]):>3} ({as_integer(new_soul.soul[key], signed=True):>3})", color_fg)
        console.print(x + offset + row, y + col, f"{titles[key]:8} {as_integer(new_soul.soul[key], signed=True):>3}", color_fg)
        i += 1
        row += 13
        if i == 3:
            col = 1
            row = 0
