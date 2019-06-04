from _data import UI_COLORS
from _helper_functions import generate_stats

from components.soul import SoulComponent
from components.stats import StatsComponent

def render_character_sheet(world):
    if not world.state == 'ViewCharacterSheet':
        return 0
    
    console, _, _, w, h = world.consoles['map']
    console.draw_frame(x=0, y=0, width=w, height=h, title="Character Sheet", clear=True, fg=UI_COLORS['fg'], bg=UI_COLORS['bg'])

    color = UI_COLORS['text']
    # Print base stats.
    player_base_stats = world.component_for_entity(1, StatsComponent).__dict__
    x, y = 3, 5

    console.print(x - 1, y - 1, 'Base Stats:', color)

    console.print(x, y + 0, 'ATK: {0}'.format(player_base_stats['attack']), color)
    console.print(x, y + 1, 'DEF: {0}'.format(player_base_stats['defense']), color)
    console.print(x, y + 2, 'HP:  {0}'.format(player_base_stats['hp']), color)
    console.print(x, y + 3, 'MAG: {0}'.format(player_base_stats['magic']), color)
    console.print(x, y + 4, 'RES: {0}'.format(player_base_stats['resistance']), color)
    console.print(x, y + 5, 'SPD: {0}'.format(player_base_stats['speed']), color)

    # Print soul stats.
    soul_stats = world.component_for_entity(1, SoulComponent).soul
    x, y = 15, 5

    console.print(x - 1, y - 1, 'Soul Stats:', color)

    console.print(x, y + 0, 'ATK: {0}'.format(soul_stats['attack']), color)
    console.print(x, y + 1, 'DEF: {0}'.format(soul_stats['defense']), color)
    console.print(x, y + 2, 'HP:  {0}'.format(soul_stats['hp']), color)
    console.print(x, y + 3, 'MAG: {0}'.format(soul_stats['magic']), color)
    console.print(x, y + 4, 'RES: {0}'.format(soul_stats['resistance']), color)
    console.print(x, y + 5, 'SPD: {0}'.format(soul_stats['speed']), color)

    
    # Print total stats.
    player_stats = generate_stats(1, world)
    x, y = 3, 14

    console.print(x - 1, y - 1, 'Total Stats:', color)

    console.print(x, y + 0, 'ATK: {0}'.format(player_stats['attack']), color)
    console.print(x, y + 1, 'DEF: {0}'.format(player_stats['defense']), color)
    console.print(x, y + 2, 'HP:  {0}'.format(player_stats['hp']), color)
    console.print(x, y + 3, 'MAG: {0}'.format(player_stats['magic']), color)
    console.print(x, y + 4, 'RES: {0}'.format(player_stats['resistance']), color)
    console.print(x, y + 5, 'SPD: {0}'.format(player_stats['speed']), color)

    # Display base stats, soul, and total stats
    # Displays item slots and their items
    # Print to Map