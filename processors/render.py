import esper
import numpy as np
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.corpse import CorpseComponent
from components.game.debug import DebugComponent
from components.game.state import StateComponent
from components.position import PositionComponent
from components.tile import TileComponent
from components.render import RenderComponent

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._console = None
    
    def process(self):
        console = self._console
        # Prepare the console.
        console.clear(bg=libtcod.black, fg=libtcod.white)

        if self.world.has_component(1, DebugComponent):
            # The DebugProcessor will print its own stuff.
            return 0

        game_state = self.world.component_for_entity(1, StateComponent).state

        if game_state == 'Game' or game_state == 'GameOver':
            # Print walls and stuff.
            for ent, (pos, ren, tile) in self.world.get_components(PositionComponent, RenderComponent, TileComponent):
                
                if ren.visible:
                    console.print(pos.x, pos.y, ren.char, ren.color)
                
                elif ren.explored:
                    console.print(pos.x, pos.y, ren.char, ren.explored_color)            

            # Print corpses to the console.
            for ent, (corpse, pos, ren) in self.world.get_components(CorpseComponent, PositionComponent, RenderComponent):
                if ren.visible:
                    console.print(pos.x, pos.y, ren.char, ren.color)

            # Print entities to the console.
            for ent, (actor, pos, ren) in self.world.get_components(ActorComponent, PositionComponent, RenderComponent):
                if ren.visible:
                    console.print(pos.x, pos.y, ren.char, ren.color)

            # Print the player (again), on top of everything else.
            player_pos = self.world.component_for_entity(2, PositionComponent)
            player_ren = self.world.component_for_entity(2, RenderComponent)
            console.print(player_pos.x, player_pos.y, player_ren.char, player_ren.color)
            
        if game_state == 'MainMenu':
            console.print(3, 3, 'Welcome to the Main Menu.\nPress any key to begin.\n', libtcod.grey)

        if game_state == 'GameOver':
            console.print(3, 3, 'You have died! Press ESC to return to the Main Menu.', libtcod.grey, bg_blend=libtcod.BKGND_NONE)
        
        console.blit(console)
        libtcod.console_flush()