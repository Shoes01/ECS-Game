import esper
import tcod as libtcod

from components.position import PositionComponent
from components.tile import TileComponent
from processors.render import RenderProcessor
from queue import Queue

class FOVProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            _fov_build = event.get('fov_build')
            _fov_recompute = event.get('fov_recompute')

            if _fov_build:
                # Create fov map.
                fov_map = libtcod.map.Map(width=self.world.map.width, height=self.world.map.height, order='F')

                for _, (pos, tile) in self.world.get_components(PositionComponent, TileComponent):
                    fov_map.walkable[pos.x, pos.y] = not tile.blocks_path
                    fov_map.transparent[pos.x, pos.y] = not tile.blocks_sight
                
                self.queue.put({'fov_recompute': True})
                self.world.get_processor(RenderProcessor).queue.put({'redraw': True})
                
                self.world.map.fov_map = fov_map
            
            if _fov_recompute:
                # Recompute fov map.
                pos_player = self.world.component_for_entity(1, PositionComponent)
                self.world.map.fov_map.compute_fov(x=pos_player.x, y=pos_player.y, radius=10, light_walls=True, algorithm=0)
                self.world.get_processor(RenderProcessor).queue.put({'redraw': True})