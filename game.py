import esper
import json
import os
import shelve

from _data import ENTITY_COLORS
from cursor import Cursor
from map import Map
from typing import Type

' Components. '
from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.energy import EnergyComponent
from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.player import PlayerComponent
from components.actor.stats import StatsComponent
from components.item.consumable import ConsumableComponent
from components.item.item import ItemComponent
from components.item.modifier import ModifierComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.furniture import FurnitureComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.rarity import RarityComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent

' Processors. '
from processors.action import ActionProcessor
from processors.ai_input import AiInputProcessor
from processors.combat import CombatProcessor
from processors.consumable import ConsumableProcessor
from processors.debug import DebugProcessor
from processors.death import DeathProcessor
from processors.descend import DescendProcessor
from processors.dijkstra import DijkstraProcessor
from processors.drop import DropProcessor
from processors.energy import EnergyProcessor
from processors.event import EventProcessor
from processors.final import FinalProcessor
from processors.initial import InitialProcessor
from processors.input import InputProcessor
from processors.inventory import InventoryProcessor
from processors.mapgen import MapgenProcessor
from processors.movement import MovementProcessor
from processors.pickup import PickupProcessor
from processors.removable import RemovableProcessor
from processors.render import RenderProcessor
from processors.skill import SkillProcessor
from processors.state import StateProcessor
from processors.wearable import WearableProcessor

class GameWorld(esper.World):
    def __init__(self):
        super().__init__()
        self.build_world()
        
        ' Flags. ' 
        self.flag_create_dijkstra_map = False
        self.flag_generate_map = False
        self.flag_pop_state = False
        self.flag_recompute_fov = True
        self.flag_reset_game = False
        self.flag_victory = False
        self.flag_view_log = False
        
        ' Data. '
        self.events = []
        self.key = None
        self.messages = []
        self.messages_offset = 0
        self.mouse_pos = None
        self.popup_menus = []
        self.redraw = True # This information needs to communicate cross-tick.
        self.state_stack = ['MainMenu']
        self.ticker = 0
        self.toggle_debug_mode = False
        self.toggle_skill_targeting = False
        self._json_data = self.load_data()

        ' Tables. '
        self.item_table, self.monster_table = self.load_tables()

        ' Objects. '
        self.consoles = None
        self.cursor = Cursor()
        self.map = Map()

    @property
    def state(self):
        try:
            return self.state_stack[-1]
        except:
            return None
    
    @property
    def turn(self):
        return self.ticker # // 10

    def build_world(self):
        # Instantiate Processors.
        action_processor = ActionProcessor()
        ai_input_processor = AiInputProcessor()
        combat_processor = CombatProcessor()
        consumable_processor = ConsumableProcessor()
        debug_processor = DebugProcessor()
        death_processor = DeathProcessor()
        descent_processor = DescendProcessor()
        dijkstra_processor = DijkstraProcessor()
        drop_processor = DropProcessor()
        energy_processor = EnergyProcessor()
        event_processor = EventProcessor()
        final_processor = FinalProcessor()
        initial_processor = InitialProcessor()
        input_processor = InputProcessor()
        inventory_processor = InventoryProcessor()
        mapgen_processor = MapgenProcessor()
        movement_processor = MovementProcessor()
        pickup_processor = PickupProcessor()
        removable_processor = RemovableProcessor()
        render_processor = RenderProcessor()
        skill_processor = SkillProcessor()
        state_processor = StateProcessor()
        wearable_processor = WearableProcessor()
        
        # Add them to the self.
        ## UPKEEP
        self.add_processor(initial_processor, 999)
        ## RENDER
        self.add_processor(render_processor, 40)
        self.add_processor(debug_processor, 39)
        ## INPUT
        self.add_processor(ai_input_processor, 30)
        self.add_processor(input_processor, 30)
        ## UPDATE
        self.add_processor(action_processor, 20)
        self.add_processor(event_processor, 20)    
        self.add_processor(inventory_processor, 15)
        self.add_processor(skill_processor, 15)
        self.add_processor(consumable_processor, 10)
        self.add_processor(descent_processor, 10)
        self.add_processor(pickup_processor, 10)
        self.add_processor(movement_processor, 10)
        self.add_processor(wearable_processor, 10)
        self.add_processor(drop_processor, 10)
        self.add_processor(combat_processor, 5)
        self.add_processor(removable_processor, 5)
        self.add_processor(death_processor, 4)
        self.add_processor(mapgen_processor, 3)
        self.add_processor(dijkstra_processor, 2)
        self.add_processor(energy_processor, 2)
        ## ENDSTEP
        self.add_processor(state_processor, 1)
        self.add_processor(final_processor, 0)

    def get_entities_at(self, x: int, y: int, *component_types: Type):
            """Get a list of entities with position (x, y) that have the desired components.

            :param component_type: The Component types to retrieve.
            :return: A list of Entities.
            """
            ents = []
            for ent, (pos, *_) in self.get_components(PositionComponent, *component_types):
                if pos.x == x and pos.y == y:
                    ents.append(ent)
            return ents

    def load_data(self):
        data = None

        with open("data/items.json", "r") as read_file:
            data = json.load(read_file)
        with open("data/monsters.json", "r") as read_file:
            data.update(json.load(read_file))
        with open("data/other.json", "r") as read_file:
            data.update(json.load(read_file))
        with open("data/skills.json", "r") as read_file:
            data.update(json.load(read_file))
        with open("data/tiles.json", "r") as read_file:
            data.update(json.load(read_file))
        
        return data
    
    def load_game(self):
        if not os.path.isfile('savegame.dat'):
            state = self.state

            if state is not 'MainMenu':
                message = 'There is no save file to load.'
                self.messages.append({'error': message})
            return 0

        with shelve.open('savegame', 'r') as data_file:
            self.map = data_file['map']
            self.messages = data_file['log']
            self.state_stack = data_file['state']
            self.ticker = data_file['ticker']
            self._components = data_file['components']
            self._entities = data_file['entities']
            self._next_entity_id = data_file['next_entity_id']
            
    def load_tables(self):
        item_table = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        monster_table = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        
        for ent, components in self._json_data.items():
            if ent == 'comment': continue
            rarity = components.get('rarity')
            archtype = components.get('archtype')
            if rarity is not None:
                if archtype == 'monster':
                    monster_table[rarity].append(ent)
                elif archtype == 'item':
                    item_table[rarity].append(ent)
        
        return item_table, monster_table

    def save_game(self):
        with shelve.open('savegame', 'n') as data_file:
            data_file['map'] = self.map
            data_file['log'] = self.messages
            data_file['state'] = self.state_stack
            data_file['ticker'] = self.ticker
            data_file['components'] = self._components
            data_file['entities'] = self._entities
            data_file['next_entity_id'] = self._next_entity_id
            
    def reset_flags(self):
        self.flag_create_dijkstra_map = False
        self.flag_generate_map = False
        self.flag_pop_state = False
        self.flag_reset_game = False
        self.flag_victory = False
        self.flag_view_log = False

    def create_entity(self, entity):
        # TODO: Fix this somehow? Move the game entity to JSON as well?
        if entity == 'player':
            return super().create_entity(
                ActorComponent(),
                EnergyComponent(energy=0),
                EquipmentComponent(),
                InventoryComponent(),
                NameComponent(name='Player'),
                PersistComponent(),
                PlayerComponent(),
                PositionComponent(),
                RenderComponent(char='@', color=ENTITY_COLORS['player']),
                StatsComponent(hp=500, power=10)
            )
        
        ent = super().create_entity()

        for key, value in self._json_data[entity].items():
            # Check for archtypes. This makes JSONing the data easier.
            if key == 'archtype':
                if value == 'monster':
                    self.add_component(ent, ActorComponent())
                    self.add_component(ent, EnergyComponent())
                    self.add_component(ent, EquipmentComponent())
                    self.add_component(ent, InventoryComponent())
                    self.add_component(ent, PositionComponent())
                elif value == 'item':
                    self.add_component(ent, ItemComponent())
                    self.add_component(ent, PositionComponent())
            
            # Now just look for each and every component possible...
            elif key == 'actor':
                self.add_component(ent, ActorComponent())
            
            elif key == 'boss':
                self.add_component(ent, BossComponent())
            
            elif key == 'brain':
                self.add_component(ent, BrainComponent())
            
            elif key == 'energy':
                self.add_component(ent, EnergyComponent())
            
            elif key == 'equipment':
                self.add_component(ent, EquipmentComponent())
            
            elif key == 'furniture':
                self.add_component(ent, FurnitureComponent())
            
            elif key == 'item':
                self.add_component(ent, ItemComponent())
            
            elif key == 'inventory':
                self.add_component(ent, InventoryComponent())
            
            elif key == 'modifier':
                power = value.get('power')
                self.add_component(ent, ModifierComponent(power=power))
            
            elif key == 'name':
                name = value.get('name')
                self.add_component(ent, NameComponent(name=name))
            
            elif key == 'position':
                self.add_component(ent, PositionComponent())
            
            elif key == 'rarity':
                rarity = value
                self.add_component(ent, RarityComponent(rarity=rarity))

            elif key == 'render':
                char = value.get('char')
                color = value.get('color')
                explored_color = value.get('explored_color')
                self.add_component(ent, RenderComponent(char=char, color=ENTITY_COLORS[color], explored_color=ENTITY_COLORS.get(explored_color)))

            elif key == 'skill':
                name = value
                description = self._json_data.get(name).get('description')
                cost = self._json_data.get(name).get('cost')
                east = self._json_data.get(name).get('east')
                north_east = self._json_data.get(name).get('north_east')
                self.add_component(ent, ItemSkillComponent(cost=cost, name=name, description=description, east=east, north_east=north_east))

            elif key == 'slot':
                slot = value.get('slot')
                self.add_component(ent, SlotComponent(slot=slot))
            
            elif key == 'stairs':
                self.add_component(ent, StairsComponent())
            
            elif key == 'stats':
                hp = value.get('hp')
                power = value.get('power')
                self.add_component(ent, StatsComponent(hp=hp, power=power))

            elif key == 'tile':
                blocks_path = value.get('blocks_path')
                blocks_sight = value.get('blocks_sight')
                self.add_component(ent, TileComponent(blocks_path=blocks_path, blocks_sight=blocks_sight))
            
            elif key == 'wearable':
                self.add_component(ent, WearableComponent())
        
        return ent
