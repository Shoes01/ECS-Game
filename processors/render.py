import esper
import numpy as np
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.game.state import StateComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent

class RenderProcessor(esper.Processor):
    def __init__(self, console):
        super().__init__()
        self.console = console
    
    def process(self):
        # Prepare the console.
        self.console.clear(bg=libtcod.black, fg=libtcod.white)

        game_state = self.world.component_for_entity(1, StateComponent).state

        if game_state == 'Game':
            # Print walls and stuff.
            for ent, (pos, ren, tile) in self.world.get_components(PositionComponent, RenderComponent, TileComponent):
                
                if ren.visible:
                    self.console.print(pos.x, pos.y, ren.char, ren.color)
                
                elif ren.explored:
                    self.console.print(pos.x, pos.y, ren.char, ren.explored_color)            

            # Print entities to the console.
            for ent, (actor, pos, ren) in self.world.get_components(ActorComponent, PositionComponent, RenderComponent):
                if ren.visible:
                    self.console.print(pos.x, pos.y, ren.char, ren.color)
        
        elif game_state == 'MainMenu':
            self.console.print(3, 3, 'Welcome to the Main Menu.\nPress any key to begin.', libtcod.grey)
        
        # Blit console.
        self.console.blit(self.console)

        # Flush console.
        libtcod.console_flush()