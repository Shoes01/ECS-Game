import esper
import numpy as np
import random
import tcod as libtcod

from components.game.mapgen import MapgenComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent
from fabricator import fabricate_entity
from processors.dijkstra import DijkstraProcessor
from processors.prerender import PrerenderProcessor

class MapgenProcessor(esper.Processor):
    def __init__(self, height, width):
        super().__init__()
        self.height = height        
        self.width = width

        self.tiles = None
        self.rooms = []
        self.leaf_rooms = []

    def process(self):
        if self.world.has_component(1, MapgenComponent):
            # Create new map.
            self.create_map()
            
            # Create fov map.
            self.create_fov_map()

            # Create dijkstra map directory.
            self.world.add_processor(DijkstraProcessor(), 55)
            self.create_directory()
            
            # Finished. Remove the component.
            self.world.remove_component(1, MapgenComponent)

    def create_map(self):
        self.tiles = np.ones([self.width, self.height], dtype=int, order='F')
        self.rooms = []
        self.leaf_rooms = []

        bsp = libtcod.bsp.BSP(x=0, y=0, width=self.width, height=self.height)
        bsp.split_recursive(
            depth=5,
            min_width=6,
            min_height=6,
            max_horizontal_ratio=1.5,
            max_vertical_ratio=1.5,
        )

        for node in bsp.pre_order():
            if node.children:
                node1, node2 = node.children
                self.connect_rooms(node1, node2)
            else:
                self.dig_room(node)
        
        self.clear_entities()
        self.place_tiles()
        self.place_player()
        self.place_monsters()

    def connect_rooms(self, node1, node2):
        ' Connect the middle of the rooms. Or nodes. '
        x1c = node1.x + ( node1.w ) // 2
        y1c = node1.y + ( node1.h ) // 2
        x2c = node2.x + ( node2.w ) // 2
        y2c = node2.y + ( node2.h ) // 2
        if x1c == x2c:
            start = 99
            end = 0
            if y1c < y2c:
                start = y1c
                end = y2c
            else:
                end = y1c
                start = y2c
        
            for y in range(start + 1, end):
                self.tiles[x1c, y] = 0
        if y1c == y2c:
            start = 99
            end = 0
            if x1c < x2c:
                start = x1c
                end = x2c
            else:
                end = x1c
                start = x2c
        
            for x in range(start + 1, end):
                self.tiles[x, y1c] = 0
    
    def dig_room(self, node):
        ' Dig out a room in the center. Nothing fancy. '
        self.rooms.append(node)
        if len(node.children) == 0:
            self.leaf_rooms.append(node)
        for x in range(node.x + 1, node.x + node.w - 1):
            for y in range(node.y + 1, node.y + node.h - 1):
                self.tiles[x, y] = 0

    def place_player(self):
        player_pos = self.world.component_for_entity(2, PositionComponent)
        room = self.leaf_rooms.pop(random.randint(0, len(self.leaf_rooms) - 1))
        self.rooms.remove(room)

        player_pos.x = random.randint(room.x, room.x + room.w - 1)
        player_pos.y = random.randint(room.y, room.y + room.h - 1)

    def clear_entities(self):
        # Clear literally all entities, except game and player.
        for ent in self.world._entities.keys():
            if not self.world.has_component(ent, PersistComponent):
                self.world.delete_entity(ent)

    def place_tiles(self):
        for (x, y), value in np.ndenumerate(self.tiles):
            if value == 0:
                self.world.create_entity(
                    PositionComponent(x=x, y=y),
                    RenderComponent(char='.', color=libtcod.white, explored_color=libtcod.darkest_grey),
                    TileComponent(blocks_path=False, blocks_sight=False)
                )
            if value == 1:
                self.world.create_entity(
                    PositionComponent(x=x, y=y),
                    RenderComponent(char='#', color=libtcod.white, explored_color=libtcod.darkest_grey),
                    TileComponent(blocks_path=True, blocks_sight=True)
                )

    def place_monsters(self):
        for ent, (pos, tile) in self.world.get_components(PositionComponent, TileComponent):
            if tile.blocks_path == False and random.randint(0, 10) > 9:
                new_ent = fabricate_entity('zombie', self.world)
                new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
                new_ent_pos.x = pos.x
                new_ent_pos.y = pos.y

    def create_fov_map(self):
        fov_map = libtcod.map.Map(self.width, self.height, order='F')

        for ent, (pos, tile) in self.world.get_components(PositionComponent, TileComponent):
            fov_map.walkable[pos.x, pos.y] = not tile.blocks_path
            fov_map.transparent[pos.x, pos.y] = not tile.blocks_sight
        
        self.world.get_processor(PrerenderProcessor).fov_map = fov_map
    
    def create_directory(self):
        directory = {}

        directions = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]
        # Build neighborhood directory.
        for (x, y), _ in np.ndenumerate(self.tiles):
            results = []
            for direction in directions:
                neighbor = (x + direction[0], y + direction[1])
                if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height and self.tiles[neighbor[0], neighbor[1]] == 0:
                    results.append(neighbor)
            
            directory[(x, y)] = results
        
        self.world.get_processor(DijkstraProcessor).directory = directory
        self.world.get_processor(DijkstraProcessor).blank_dijkstra_map = np.ones((self.width, self.height), dtype=int, order='F') * 999