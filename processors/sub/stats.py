from _data import SingleLineBox, UI_COLORS
from _helper_functions import as_decimal, generate_stats
from components.actor.equipment import EquipmentComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.render import RenderComponent

def render_stats(world):
    if world.state == 'MainMenu':
        return 0
        
    console, x, y, w, h = world.consoles['stats']
    
    color = UI_COLORS['text']
    color_invalid = UI_COLORS['text_invalid']
    
    # Draw the player stats.
    player_stats = generate_stats(1, world)
    stats = {'hp': 'HP', 'speed': 'SPD', 'attack': 'ATK', 'defense': 'DEF', 'magic': 'MAG', 'resistance': 'RES'}
    x_offset, y_offset = 0, 0

    for stat, name in stats.items():
        if name == 'HP':
            console.print(x_offset, y_offset, f"{name}:{as_decimal(player_stats[stat]):>6}", color)    
        else:
            console.print(x_offset, y_offset, f"{name}:{as_decimal(player_stats[stat]):>5}", color)

        x_offset += 10
        if x_offset == 20:
            x_offset = 0
            y_offset += 1

    console.print( 0, 3, 'TRN:{:>5}'.format(world.turn), color)
    console.print(10, 3, 'FLR:{:>5}'.format(world.map.floor), color)

    # Draw the item boxes.
    boxes = {'mainhand': None ,'head': None, 'accessory': None, 'offhand': None, 'torso': None, 'feet': None}
    box_char = {'mainhand': 'Q' ,'head': 'W', 'accessory': 'E', 'offhand': 'A', 'torso': 'S', 'feet': 'D'}

    # Figure out which items are in which slots.
    for item in world.component_for_entity(1, EquipmentComponent).equipment:
        slot = world.component_for_entity(item, SlotComponent).slot
        boxes[slot] = item

    # Render the item boxes.
    x, y = 2, 0
    y_offset = 4
    i = 0
    j = 0
    for slot, item in boxes.items():
        char_color = color_invalid
        render_comp = None
        cooldown = None
        
        if item:
            char_color = color
            render_comp = world.component_for_entity(item, RenderComponent)
            if world.has_component(item, ItemSkillComponent):
                cooldown = world.component_for_entity(item, ItemSkillComponent).cooldown_remaining
        
        draw_letter_box(2 + i, 0 + y_offset + j, 4, 4, box_char[slot], console, char_color, render_comp, cooldown)

        i += 4
        if i == 12:
            i = 0
            j = 4

def draw_letter_box(x, y, w, h, char, console, color, item, cooldown):
    # Draw the little box, and put the letter in it.
    box = SingleLineBox()
    
    for xx in range(x, x + w):
        console.print(xx, y, box.horizontal, color)
        console.print(xx, y + h - 1, box.horizontal, color)
    
    for yy in range(y, y + h):
        console.print(x, yy, box.vertical, color)
        console.print(x + w - 1, yy, box.vertical, color)
    
    console.print(x, y, box.top_left, color)
    console.print(x + w - 1, y, box.top_right, color)
    console.print(x, y + h -1, box.bottom_left, color)
    console.print(x + w - 1, y + h -1, box.bottom_right, color)

    console.print(x + 1, y + 1, char, color)
    if item:
        console.print(x + 2, y + 1, item.char, item.color)
        if cooldown:
            console.print(x + 2, y + 2, str(cooldown), UI_COLORS['cooldown'])