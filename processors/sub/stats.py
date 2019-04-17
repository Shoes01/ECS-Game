from _data import SingleLineBox, UI_COLORS
from _helper_functions import calculate_power
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.game.map import MapComponent
from components.game.turn_count import TurnCountComponent
from components.item.slot import SlotComponent

def render_stats(console_bundle, world):
    console, x, y, w, h = console_bundle
        
    color_invalid = UI_COLORS['text_invalid']
    color = UI_COLORS['text']

    # Draw the player stats.
    player_stats_component = world.component_for_entity(2, StatsComponent)

    console.print(0, 0, 'HP: {0}/{1}'.format(player_stats_component.hp, player_stats_component.hp_max), color)
    console.print(0, 1, 'PWR: {0}'.format(calculate_power(2, world)), color)
    console.print(0, 2, 'TURN: {0}'.format(world.component_for_entity(1, TurnCountComponent).turn_count), color)
    console.print(0, 3, 'DPTH: {0}'.format(world.component_for_entity(1, MapComponent).depth), color)


    # Draw the item boxes.
    Q_color, W_color, E_color, A_color, S_color, D_color = color_invalid, color_invalid, color_invalid, color_invalid, color_invalid, color_invalid
    for item in world.component_for_entity(2, EquipmentComponent).equipment:
        slot = world.component_for_entity(item, SlotComponent).slot
        if slot == 'mainhand':
            Q_color = color
        elif slot == 'head':
            W_color = color
        elif slot == 'accessory':
            E_color = color
        elif slot == 'offhand':
            A_color = color
        elif slot == 'torso':
            S_color = color
        elif slot == 'boots':
            D_color = color
    
    y_offset = 4
    draw_letter_box(0, 0 + y_offset, 4, 4, 'Q', console, Q_color) # Slot: mainhand
    draw_letter_box(4, 0 + y_offset, 4, 4, 'W', console, W_color) # Slot: head
    draw_letter_box(8, 0 + y_offset, 4, 4, 'E', console, E_color) # Slot: Accessory
    draw_letter_box(0, 4 + y_offset, 4, 4, 'A', console, A_color) # Slot: offhand
    draw_letter_box(4, 4 + y_offset, 4, 4, 'S', console, S_color) # Slot: torso
    draw_letter_box(8, 4 + y_offset, 4, 4, 'D', console, D_color) # Slot: boots

def draw_letter_box(x, y, w, h, char, console, color):
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