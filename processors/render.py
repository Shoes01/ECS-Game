import esper
import numpy as np
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.game.state import StateComponent
from components.position import PositionComponent
from components.tile import TileComponent
from components.render import RenderComponent

class RenderProcessor(esper.Processor):
    def __init__(self, console):
        super().__init__()
        self.console = console
        self.debug_mode = False # The DebugProcessor changes this.
    
    def process(self):
        # Prepare the console.
        self.console.clear(bg=libtcod.black, fg=libtcod.white)

        if self.debug_mode:
            return 0

        game_state = self.world.component_for_entity(1, StateComponent).state

        if game_state == 'Game':
            # Print walls and stuff.
            for ent, (pos, ren, tile) in self.world.get_components(PositionComponent, RenderComponent, TileComponent):
                
                if ren.visible or True: # DEBUG
                    self.console.print(pos.x, pos.y, ren.char, ren.color)
                
                elif ren.explored:
                    self.console.print(pos.x, pos.y, ren.char, ren.explored_color)            

            # Print entities to the console.
            for ent, (actor, pos, ren) in self.world.get_components(ActorComponent, PositionComponent, RenderComponent):
                if ren.visible or True: # DEBUG
                    self.console.print(pos.x, pos.y, ren.char, ren.color)

            # Print the player.
            player_pos = self.world.component_for_entity(2, PositionComponent)
            player_ren = self.world.component_for_entity(2, RenderComponent)
            self.console.print(player_pos.x, player_pos.y, player_ren.char, player_ren.color)
            

        elif game_state == 'MainMenu':
            self.console.print(3, 3, 'Welcome to the Main Menu.\nPress any key to begin.', libtcod.grey)
        
        # Blit console.
        self.console.blit(self.console)

        # Flush console.
        libtcod.console_flush()