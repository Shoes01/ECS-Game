from _data import UI_COLORS
from _helper_functions import as_decimal, as_integer, generate_stats
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.item.skills import SkillsComponent
from components.item.slot import SlotComponent 
from components.name import NameComponent
from components.soul import SoulComponent
from components.stats import StatsComponent

def render_character_sheet(console_object, world):
    console, _, _, w, h = console_object
    color_fg = UI_COLORS['text']
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
    skill_directory = world.component_for_entity(1, SkillDirectoryComponent).skill_directory
    soul_stats = world.component_for_entity(1, SoulComponent).soul
    titles = {
        'hp': 'Health:',
        'attack': 'Attack:',
        'magic': 'Magic:',
        'speed': 'Speed:',
        'defense': 'Defense:',
        'resistance': 'Resist:'
        }
    upkeep_stats = world.component_for_entity(1, JobComponent).upkeep

    equipped_items = generate_equipped_items(titles, world)

    # Draw sheet.
    console.draw_frame(x=0, y=0, width=w, height=h, title="Character Sheet", clear=True, fg=UI_COLORS['fg'], bg=UI_COLORS['bg'])

    # Print base stats.
    x, y = 3, 5
    console.print(x - 1, y - 1, 'Base Stats:', color_fg)
    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {as_decimal(player_base_stats[key]):>5}", color_fg)
        i += 1

    # Print soul stats.
    x, y = 20, 5
    console.print(x - 1, y - 1, 'Soul Stats:', color_fg)
    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {as_integer(soul_stats[key]):>3}", color_fg)
        i += 1

    # Print job upkeep.
    x, y = 37, 5
    console.print(x - 1, y - 1, 'Job Upkeep:', color_fg)
    i = 0
    for key in titles:
        console.print(x, y + i, f"{titles[key]:8} {as_integer(upkeep_stats[key]):>3}", color_fg)
        i += 1

    # Print total stats.
    x, y = 3, 14
    console.print(x - 1, y - 1, 'Total Stats:', color_fg)    
    i = 0
    for key in titles:
        console.print(
            x, y + i, 
            f"{titles[key]:8} {as_decimal(player_stats[key]):>5} ({as_decimal(player_base_stats[key]):>5} + {as_integer(soul_stats[key]):>3} + {as_integer(upkeep_stats[key]):>3})", 
            color_fg)
        i += 1

    # Displays item slots and their items
    ### Mainhand: Sword
    ###   Skill: Lunge
    ###   Description: This is where the skill description goes.
    x, y = 57, 5
    console.print(x - 1, y - 1, 'Equipped Items:', color_fg)
    i = 0
    for key in slots:
        item_name, item_skill, item_bonus, item_skill_description = None, None, None, None

        if equipped_items.get(key):
            item_name, item_skill, item_bonus, item_skill_description = equipped_items[key]

        text_1 = f"{slots[key]} {item_name}"
        text_2 = f"  Skill: {str(item_skill).capitalize()}"
        text_3 = f"  Bonus: {item_bonus}"
        text_4 = f"  Description: {item_skill_description}"
                
        console.print(x, y + i, text_1, color_fg)
        i += 1
        console.print(x, y + i, text_2, color_fg)
        i += 1
        console.print(x, y + i, text_3, color_fg)
        i += 1
        console.print_box(x, y + i, 40, 2, text_4, color_fg)
        i += 3
    
    # Display skill directory.
    x, y = 77, 5
    console.print(x - 1, y - 1, 'Skill Directory:', color_fg)
    i = 0
    for job, skill_info in skill_directory.items():
        if skill_info:
            for skill_name, ap in skill_info.items():
                console.print(x, y + i, f"{skill_name.capitalize()}: {ap[0]}/{ap[1]}")
                i += 1

def generate_equipped_items(titles, world):
    equipment = world.component_for_entity(1, EquipmentComponent).equipment
    equipped_items = {}

    for item in equipment:
        slot = world.component_for_entity(item, SlotComponent).slot
        name = world.component_for_entity(item, NameComponent)._name
        skill_comp = None
        
        for temp_skill in world.component_for_entity(item, SkillsComponent).skills:
            if temp_skill.active:
                skill_comp = temp_skill

        bonus = f""
        description = ""
        skill = "None"
        
        if skill_comp:
            description = skill_comp.description
            skill = skill_comp.name
        
        for stat, value in world.component_for_entity(item, StatsComponent).__dict__.items():
            if value:
                bonus += f"{titles[stat][:-1]} {as_integer(value, signed=True)}, "
        bonus = bonus[:-2]
        if not bonus:
            bonus = "None"
        
        equipped_items[slot] = (name, skill, bonus, description)
    
    return equipped_items
