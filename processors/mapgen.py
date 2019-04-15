import esper
import numpy as np
import random
import tcod as libtcod

from _data import FINAL_FLOOR
from _helper_functions import tile_occupied
from components.game.map import MapComponent
from components.game.mapgen import MapgenComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent
from fabricator import fabricate_entity

class MapgenProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._rooms = []
        self._leaf_rooms = []

    def process(self):
        if self.world.has_component(1, MapgenComponent):
            game_map = self.world.component_for_entity(1, MapComponent)
            game_map.depth += 1

            # Create new map.
            game_map.tiles = self.create_map(game_map.depth, game_map.height, game_map.width)
            
            # Create directory of map.
            game_map.directory = self.create_directory(game_map.height, game_map.tiles, game_map.width)

            # Create fov map.
            game_map.fov_map = self.create_fov_map(game_map.height, game_map.width)

    def create_map(self, depth, h, w):
        tiles = np.ones([w, h], dtype=int, order='F')
        self._rooms = []
        self._leaf_rooms = []

        bsp = libtcod.bsp.BSP(x=0, y=0, width=w, height=h)
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
                tiles = self.connect_rooms(node1, node2, tiles)
            else:
                tiles = self.dig_room(node, tiles)
        
        self.clear_entities()
        self.place_tiles(tiles)
        self.place_player()
        self.place_stairs(depth)
        self.place_monsters(depth, tiles)
        self.place_loot(tiles)

        return tiles

    def connect_rooms(self, node1, node2, tiles):
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
                tiles[x1c, y] = 0
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
                tiles[x, y1c] = 0
        
        return tiles
    
    def dig_room(self, node, tiles):
        ' Dig out a room in the center. Nothing fancy. '
        self._rooms.append(node)
        if len(node.children) == 0:
            self._leaf_rooms.append(node)
        for x in range(node.x + 1, node.x + node.w - 1):
            for y in range(node.y + 1, node.y + node.h - 1):
                tiles[x, y] = 0
        
        return tiles

    def place_player(self):
        player_pos = self.world.component_for_entity(2, PositionComponent)
        room = self._leaf_rooms.pop(random.randint(0, len(self._leaf_rooms) - 1))
        self._rooms.remove(room)

        player_pos.x = random.randint(room.x + 1, room.x + room.w - 2)
        player_pos.y = random.randint(room.y + 1, room.y + room.h - 2)

        ### DEBUG 
        """
        new_ent = fabricate_entity('stairs', self.world)
        
        new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
        new_ent_pos.x = player_pos.x
        new_ent_pos.y = player_pos.y
        """

    def place_stairs(self, depth):
        if depth == FINAL_FLOOR:
            return 0

        new_ent = fabricate_entity('stairs', self.world)
        
        new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
        room = self._leaf_rooms.pop(random.randint(0, len(self._leaf_rooms) - 1))
        new_ent_pos.x = random.randint(room.x + 1, room.x + room.w - 2)
        new_ent_pos.y = random.randint(room.y + 1, room.y + room.h - 2)

    def clear_entities(self):
        # Clear literally all entities, except game, player, and things picked up by the player.
        for ent in self.world._entities.keys():
            if not self.world.has_component(ent, PersistComponent):
                self.world.delete_entity(ent)

    def place_tiles(self, tiles):
        for (x, y), value in np.ndenumerate(tiles):
            if value == 0:
                new_ent = fabricate_entity('floor', self.world)
                new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
                new_ent_pos.x = x
                new_ent_pos.y = y
            if value == 1:
                new_ent = fabricate_entity('wall', self.world)
                new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
                new_ent_pos.x = x
                new_ent_pos.y = y

    def place_monsters(self, depth, tiles):
        if depth == FINAL_FLOOR:
            boss_room = self._leaf_rooms.pop(random.randint(0, len(self._leaf_rooms) - 1))
            self._rooms.remove(boss_room)

            x = random.randint(boss_room.x, boss_room.x + boss_room.w - 1)
            y = random.randint(boss_room.y, boss_room.y + boss_room.h - 1)

            if not tiles[x, y] and not tile_occupied(self.world, x, y):
                new_ent = fabricate_entity('demon', self.world)
                new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
                new_ent_pos.x = x
                new_ent_pos.y = y            


        for room in self._rooms:
            size = room.h + room.w
            number_of_monsters = size // 5  # This controls monster density

            while number_of_monsters > 0:
                x = random.randint(room.x, room.x + room.w - 1)
                y = random.randint(room.y, room.y + room.h - 1)
                
                if not tiles[x, y] and not tile_occupied(self.world, x, y):
                    new_ent = fabricate_entity('zombie', self.world)
                    new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
                    new_ent_pos.x = x
                    new_ent_pos.y = y
                    
                number_of_monsters -= 1

    def place_loot(self, tiles):
        for room in self._rooms:
            size = room.h + room.w
            number_of_items = size // 5 - 3

            while number_of_items > 0:
                x = random.randint(room.x, room.x + room.w - 1)
                y = random.randint(room.y, room.y + room.h - 1)
                
                if not tiles[x, y] and not tile_occupied(self.world, x, y):
                    chance = random.randint(0, 100)
                    if chance > 80:
                        new_ent = fabricate_entity('sword', self.world)
                    else:
                        new_ent = fabricate_entity('titan_potion', self.world)
                    new_ent_pos = self.world.component_for_entity(new_ent, PositionComponent)
                    new_ent_pos.x = x
                    new_ent_pos.y = y
                    
                number_of_items -= 1


    def create_directory(self, h, tiles, w):
        directory = {}
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        
        for (x, y), _ in np.ndenumerate(tiles):
            results = []
            for direction in directions:
                neighbor = (x + direction[0], y + direction[1])
                if 0 <= neighbor[0] < w and 0 <= neighbor[1] < h and tiles[neighbor[0], neighbor[1]] == 0:
                    results.append(neighbor)
            
            directory[(x, y)] = results
        
        return directory

    def create_fov_map(self, h, w):
        fov_map = libtcod.map.Map(w, h, order='F')

        for ent, (pos, tile) in self.world.get_components(PositionComponent, TileComponent):
            fov_map.walkable[pos.x, pos.y] = not tile.blocks_path
            fov_map.transparent[pos.x, pos.y] = not tile.blocks_sight
        
        return fov_map