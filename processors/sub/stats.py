from _data import SingleLineBox, UI_COLORS
from _helper_functions import calculate_atk
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.slot import SlotComponent
from components.render import RenderComponent

def render_stats(world):
    if world.state == 'MainMenu':
        return 0
        
    console, x, y, w, h = world.consoles['stats']
    
    color = UI_COLORS['text']
    color_invalid = UI_COLORS['text_invalid']
    
    # Draw the player stats.
    player_stats_component = world.component_for_entity(1, StatsComponent)

    console.print(0, 0, 'HP: {0}/{1}'.format(player_stats_component.hp, player_stats_component.hp_max), color)
    console.print(0, 1, 'PWR: {0}'.format(calculate_atk(1, world)), color)
    console.print(0, 2, 'TURN: {0}'.format(world.turn), color)
    console.print(0, 3, 'FLOOR: {0}'.format(world.map.floor), color)

    # Draw the item boxes.
    Q_color, W_color, E_color, A_color, S_color, D_color = color_invalid, color_invalid, color_invalid, color_invalid, color_invalid, color_invalid
    Q_item, W_item, E_item, A_item, S_item, D_item = None, None, None, None, None, None
    for item in world.component_for_entity(1, EquipmentComponent).equipment:
        slot = world.component_for_entity(item, SlotComponent).slot
        if slot == 'mainhand':
            Q_color = color
            Q_item = world.component_for_entity(item, RenderComponent)
        elif slot == 'head':
            W_color = color
            W_item = world.component_for_entity(item, RenderComponent)
        elif slot == 'accessory':
            E_color = color
            E_item = world.component_for_entity(item, RenderComponent)
        elif slot == 'offhand':
            A_color = color
            A_item = world.component_for_entity(item, RenderComponent)
        elif slot == 'torso':
            S_color = color
            S_item = world.component_for_entity(item, RenderComponent)
        elif slot == 'feet':
            D_color = color
            D_item = world.component_for_entity(item, RenderComponent)

    y_offset = 4
    draw_letter_box(0, 0 + y_offset, 4, 4, 'Q', console, Q_color, Q_item) # Slot: mainhand
    draw_letter_box(4, 0 + y_offset, 4, 4, 'W', console, W_color, W_item) # Slot: head
    draw_letter_box(8, 0 + y_offset, 4, 4, 'E', console, E_color, E_item) # Slot: accessory
    draw_letter_box(0, 4 + y_offset, 4, 4, 'A', console, A_color, A_item) # Slot: offhand
    draw_letter_box(4, 4 + y_offset, 4, 4, 'S', console, S_color, S_item) # Slot: torso
    draw_letter_box(8, 4 + y_offset, 4, 4, 'D', console, D_color, D_item) # Slot: feet

def draw_letter_box(x, y, w, h, char, console, color, item):
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