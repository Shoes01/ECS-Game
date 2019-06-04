from _data import UI_COLORS
from _helper_functions import generate_stats

from components.soul import SoulComponent
from components.stats import StatsComponent

def render_character_sheet(world):
    if not world.state == 'ViewCharacterSheet':
        return 0
    
    console, _, _, w, h = world.consoles['map']
    color = UI_COLORS['text']
    player_base_stats = world.component_for_entity(1, StatsComponent).__dict__
    player_stats = generate_stats(1, world)
    soul_stats = world.component_for_entity(1, SoulComponent).soul
    titles = {
        'attack': 'Attack:',
        'defense': 'Defense:',
        'magic': 'Magic:',
        'resistance': 'Resist:',
        'hp': 'Health:',
        'speed': 'Speed:'
        }

    # Draw sheet.
    console.draw_frame(x=0, y=0, width=w, height=h, title="Character Sheet", clear=True, fg=UI_COLORS['fg'], bg=UI_COLORS['bg'])

    # Print base stats.
    x, y = 3, 5
    console.print(x - 1, y - 1, 'Base Stats:', color)
    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {player_base_stats[key]:3}", color)
        i += 1

    # Print soul stats.
    x, y = 20, 5
    console.print(x - 1, y - 1, 'Soul Stats:', color)
    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {soul_stats[key]:3}", color)
        i += 1

    # Print total stats.
    x, y = 3, 14
    console.print(x - 1, y - 1, 'Total Stats:', color)    
    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {player_stats[key]:3} ({player_base_stats[key]:3} + {soul_stats[key]:3})", color)
        i += 1

    # Displays item slots and their items