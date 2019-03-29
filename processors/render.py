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
        self._consoles = {}
    
    def process(self):        
        con_obj = self._consoles['con'] # type: (console, x, y, w, h)
        eqp_obj = self._consoles['eqp']
        log_obj = self._consoles['log']
        map_obj = self._consoles['map']
        
        # Prepare the console.
        eqp_obj[0].clear(bg=libtcod.black, fg=libtcod.white)
        log_obj[0].clear(bg=libtcod.black, fg=libtcod.white)
        map_obj[0].clear(bg=libtcod.black, fg=libtcod.white)

        if self.world.has_component(1, DebugComponent):
            # The DebugProcessor will print its own stuff.
            return 0

        game_state = self.world.component_for_entity(1, StateComponent).state

        if game_state == 'Game' or game_state == 'GameOver':
            # Print walls and stuff.
            for ent, (pos, ren, tile) in self.world.get_components(PositionComponent, RenderComponent, TileComponent):
                
                if ren.visible:
                    map_obj[0].print(pos.x, pos.y, ren.char, ren.color)
                
                elif ren.explored:
                    map_obj[0].print(pos.x, pos.y, ren.char, ren.explored_color)            

            # Print corpses to the console.
            for ent, (corpse, pos, ren) in self.world.get_components(CorpseComponent, PositionComponent, RenderComponent):
                if ren.visible:
                    map_obj[0].print(pos.x, pos.y, ren.char, ren.color)

            # Print entities to the console.
            for ent, (actor, pos, ren) in self.world.get_components(ActorComponent, PositionComponent, RenderComponent):
                if ren.visible:
                    map_obj[0].print(pos.x, pos.y, ren.char, ren.color)

            # Print the player (again), on top of everything else.
            player_pos = self.world.component_for_entity(2, PositionComponent)
            player_ren = self.world.component_for_entity(2, RenderComponent)
            map_obj[0].print(player_pos.x, player_pos.y, player_ren.char, player_ren.color)
            
        if game_state == 'MainMenu':
            map_obj[0].print(3, 3, 'Welcome to the Main Menu.\nPress any key to begin.\n', libtcod.grey)

        if game_state == 'GameOver':
            map_obj[0].print(3, 3, 'You have died! Press ESC to return to the Main Menu.', libtcod.grey, bg_blend=libtcod.BKGND_NONE)
        
        eqp_obj[0].blit(dest=con_obj[0], dest_x=eqp_obj[1], dest_y=eqp_obj[2], width=eqp_obj[3], height=eqp_obj[4])
        log_obj[0].blit(dest=con_obj[0], dest_x=log_obj[1], dest_y=log_obj[2], width=log_obj[3], height=log_obj[4])
        map_obj[0].blit(dest=con_obj[0], dest_x=map_obj[1], dest_y=map_obj[2], width=map_obj[3], height=map_obj[4])
        libtcod.console_flush()