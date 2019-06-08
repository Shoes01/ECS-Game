from _data import UI_COLORS
from components.soul import SoulComponent
from processors.soul import SoulProcessor

def render_soul_sheet(world):
    if world.state is not 'SoulState':
        return 0
    
    console, _, _, w, h = world.consoles['map']
    color = UI_COLORS['text']
    new_soul = world.get_processor(SoulProcessor).soul.soul
    player_soul = world.component_for_entity(1, SoulComponent).soul
    titles = {
        'attack': 'Attack:',
        'defense': 'Defense:',
        'magic': 'Magic:',
        'resistance': 'Resist:',
        'hp': 'Health:',
        'speed': 'Speed:'
        }

    # Draw sheet.
    console.draw_frame(x=0, y=0, width=w, height=h, title="Soul Consumption", clear=True, fg=UI_COLORS['fg'], bg=UI_COLORS['bg'])

    # Print player soul and new soul.
    x, y = 3, 5
    console.print(x - 1, y - 1, 'Player Soul:', color)

    offset = 20
    console.print(x - 1 + offset, y - 1, 'New Soul:', color)

    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {player_soul[key]:3}", color)
        console.print(x + offset, y + i, f"{titles[key]:8} {new_soul[key]:3}", color)
        i += 1
