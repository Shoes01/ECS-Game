import esper
import tcod as libtcod

class StatsProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = []

    def process(self):
        console, x, y, w, h = self._consoles['eqp'] # type: console, x, y, w, h
        
        console.clear(bg=libtcod.black, fg=libtcod.white)
        
        self.draw_letter_box(0, 0, 4, 4, 'A', console)
        self.draw_letter_box(4, 0, 4, 4, 'B', console)
        self.draw_letter_box(8, 0, 4, 4, 'C', console)
        self.draw_letter_box(0, 4, 4, 4, 'D', console)
        self.draw_letter_box(4, 4, 4, 4, 'E', console)
        self.draw_letter_box(8, 4, 4, 4, 'f', console)

        console.blit(dest=self._consoles['con'][0], dest_x=x, dest_y=y, src_x=0, src_y=0, width=w, height=h)
    
    def draw_letter_box(self, x, y, w, h, char, console):
        # Draw the little box, and put the letter in it.
        for xx in range(x, x + w):
            console.print(xx, y, '+', libtcod.white)
            console.print(xx, y + h - 1, '+', libtcod.white)
        
        for yy in range(y, y + h):
            console.print(x, yy, '+', libtcod.white)
            console.print(x + w - 1, yy, '+', libtcod.white)
        
        console.print(x + 1, y + 1, char, libtcod.white)