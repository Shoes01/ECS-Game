import esper
import tcod as libtcod

from _helper_functions import calculate_power
from components.actor.stats import StatsComponent

class StatsProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = []

    def process(self):
        console, x, y, w, h = self._consoles['eqp'] # type: console, x, y, w, h
        
        console.clear(bg=libtcod.black, fg=libtcod.white)
        
        color = libtcod.white

        # Draw the player stats.
        player_stats_component = self.world.component_for_entity(2, StatsComponent)

        console.print(0, 0, 'HP: {0}/{1}'.format(player_stats_component.hp, player_stats_component.hp_max), color)
        console.print(0, 1, 'PWR: {0}'.format(calculate_power(2, self.world)), color)

        # Draw the item boxes.
        
        y_offset = 3
        self.draw_letter_box(0, 0 + y_offset, 4, 4, 'Q', console, color)
        self.draw_letter_box(4, 0 + y_offset, 4, 4, 'W', console, color)
        self.draw_letter_box(8, 0 + y_offset, 4, 4, 'E', console, color)
        self.draw_letter_box(0, 4 + y_offset, 4, 4, 'A', console, color)
        self.draw_letter_box(4, 4 + y_offset, 4, 4, 'S', console, color)
        self.draw_letter_box(8, 4 + y_offset, 4, 4, 'D', console, color)

        console.blit(dest=self._consoles['con'][0], dest_x=x, dest_y=y, src_x=0, src_y=0, width=w, height=h)
    
    def draw_letter_box(self, x, y, w, h, char, console, color):
        # Draw the little box, and put the letter in it.
        for xx in range(x, x + w):
            console.print(xx, y, '-', color)
            console.print(xx, y + h - 1, '-', color)
        
        for yy in range(y, y + h):
            console.print(x, yy, '|', color)
            console.print(x + w - 1, yy, '|', color)
        
        console.print(x, y, '+', color)
        console.print(x + w - 1, y, '+', color)
        console.print(x, y + h -1, '+', color)
        console.print(x + w - 1, y + h -1, '+', color)


        console.print(x + 1, y + 1, char, color)