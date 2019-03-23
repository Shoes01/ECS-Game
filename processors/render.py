import esper
import numpy as np
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.game.console import ConsoleComponent
from components.game.debug import DebugComponent
from components.game.state import StateComponent
from components.position import PositionComponent
from components.tile import TileComponent
from components.render import RenderComponent

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        console = self.world.component_for_entity(1, ConsoleComponent).console
        # Prepare the console.
        console.clear(bg=libtcod.black, fg=libtcod.white)

        if self.world.has_component(1, DebugComponent):
            return 0

        game_state = self.world.component_for_entity(1, StateComponent).state

        if game_state == 'Game':
            # Print walls and stuff.
            for ent, (pos, ren, tile) in self.world.get_components(PositionComponent, RenderComponent, TileComponent):
                
                if ren.visible:
                    console.print(pos.x, pos.y, ren.char, ren.color)
                
                elif ren.explored:
                    console.print(pos.x, pos.y, ren.char, ren.explored_color)            

            # Print entities to the console.
            for ent, (actor, pos, ren) in self.world.get_components(ActorComponent, PositionComponent, RenderComponent):
                if ren.visible:
                    console.print(pos.x, pos.y, ren.char, ren.color)

            # Print the player.
            player_pos = self.world.component_for_entity(2, PositionComponent)
            player_ren = self.world.component_for_entity(2, RenderComponent)
            console.print(player_pos.x, player_pos.y, player_ren.char, player_ren.color)
            

        elif game_state == 'MainMenu':
            console.print(3, 3, 'Welcome to the Main Menu.\nPress any key to begin.', libtcod.grey)
        
        # Blit console.
        console.blit(console)

        # Flush console.
        libtcod.console_flush()