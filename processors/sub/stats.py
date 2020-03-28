from _data import SingleLineBox
from _helper_functions import as_decimal, generate_stats
from components.actor.diary import DiaryComponent
from components.actor.equipment import EquipmentComponent
from components.item.skill_pool import SkillPoolComponent
from components.item.slot import SlotComponent
from components.render import RenderComponent
from data.render import UI_COLORS

def render_stats(console_object, world):
    console = console_object[0]
    
    color_fg = UI_COLORS['text']
    color_fg_invalid = UI_COLORS['text_invalid']
    
    # Draw the player stats.
    player_stats = generate_stats(1, world)
    stats = {'hp': 'HP', 'speed': 'SPD', 'attack': 'ATK', 'defense': 'DEF', 'magic': 'MAG', 'resistance': 'RES'}
    x_offset, y_offset = 0, 0

    for stat, name in stats.items():
        if name == 'HP':
            console.print(x_offset, y_offset, f"{name}:{as_decimal(player_stats[stat]):>6}", color_fg)    
        else:
            console.print(x_offset, y_offset, f"{name}:{as_decimal(player_stats[stat]):>5}", color_fg)

        x_offset += 10
        if x_offset == 20:
            x_offset = 0
            y_offset += 1

    console.print( 0, 3, 'TRN:{:>5}'.format(world.turn), color_fg)
    console.print(10, 3, 'FLR:{:>5}'.format(world.map.floor), color_fg)

    # Draw the item boxes.
    boxes = {'mainhand': None ,'head': None, 'accessory': None, 'offhand': None, 'torso': None, 'feet': None}
    box_char = {'mainhand': 'Q' ,'head': 'W', 'accessory': 'E', 'offhand': 'A', 'torso': 'S', 'feet': 'D'}

    # Figure out which items are in which slots.
    for item in world.component_for_entity(1, EquipmentComponent).equipment:
        boxes[world.component_for_entity(item, SlotComponent).name] = item

    # Render the item boxes.
    x, y = 4, 0
    y_offset = 4
    i = 0
    j = 0
    for slot, item in boxes.items():
        char_color = color_fg_invalid
        cooldown = None
        diary = world.component_for_entity(1, DiaryComponent)

        for skill in diary.active:
            if skill.slot.name == slot:
                char_color = color_fg
                break

        for entry in diary.cooldown:
            if entry.skill.slot.name == slot and entry.skill in diary.active:
                char_color = UI_COLORS['cooldown']
                cooldown = entry.remaining                    
                break
    
        draw_letter_box(x + i, y + y_offset + j, 4, 4, box_char[slot], console, char_color, cooldown)

        i += 4
        if i == 12:
            i = 0
            j = 4

def draw_letter_box(x, y, w, h, char, console, color_fg, cooldown):
    # Draw the little box, and put the letter in it.
    box = SingleLineBox()
    
    for xx in range(x, x + w):
        console.print(xx, y, box.horizontal, color_fg)
        console.print(xx, y + h - 1, box.horizontal, color_fg)
    
    for yy in range(y, y + h):
        console.print(x, yy, box.vertical, color_fg)
        console.print(x + w - 1, yy, box.vertical, color_fg)
    
    console.print(x, y, box.top_left, color_fg)
    console.print(x + w - 1, y, box.top_right, color_fg)
    console.print(x, y + h -1, box.bottom_left, color_fg)
    console.print(x + w - 1, y + h -1, box.bottom_right, color_fg)

    console.print(x + 1, y + 1, char, color_fg)