from _data import UI_COLORS
from _helper_functions import generate_stats
from components.actor.equipment import EquipmentComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.name import NameComponent
from components.soul import SoulComponent
from components.stats import StatsComponent

def render_character_sheet(world):
    if not world.state == 'ViewCharacterSheet':
        return 0
    
    console, _, _, w, h = world.consoles['map']
    color = UI_COLORS['text']
    equipped_items = generate_equipped_items(world)
    player_base_stats = world.component_for_entity(1, StatsComponent).__dict__
    player_stats = generate_stats(1, world)
    slots = {
        'mainhand': 'Mainhand:',
        'offhand': 'Offhand:',
        'torso': 'Torso:',
        'head': 'Head:',
        'feet': 'Feet:',
        'accessory': 'Accessory:'
        }
    soul_stats = world.component_for_entity(1, SoulComponent).soul
    titles = {
        'hp': 'Health:',
        'attack': 'Attack:',
        'magic': 'Magic:',
        'speed': 'Speed:',
        'defense': 'Defense:',
        'resistance': 'Resist:'
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
    ### Mainhand: Sword
    ###   Skill: Lunge
    ###   Description: This is where the skill description goes.
    x, y = 40, 5
    console.print(x - 1, y - 1, 'Equipped Items:', color)
    i = 0
    for key in slots:
        item_name, item_skill = None, None
        if equipped_items.get(key):
            item_name, item_skill = equipped_items[key]

        text_1 = f"{slots[key]} {item_name}"
        text_2 = f"  Skill: {str(item_skill).capitalize()}"
        
        console.print(x, y + i, text_1, color)
        i += 1
        console.print(x, y + i, text_2, color)
        i += 2

def generate_equipped_items(world):
    equipment = world.component_for_entity(1, EquipmentComponent).equipment
    equipped_items = {}

    for item in equipment:
        slot = world.component_for_entity(item, SlotComponent).slot
        name = world.component_for_entity(item, NameComponent)._name
        skill = "None" if not world.has_component(item, ItemSkillComponent) else world.component_for_entity(item, ItemSkillComponent).name

        equipped_items[slot] = (name, skill)
    
    return equipped_items
