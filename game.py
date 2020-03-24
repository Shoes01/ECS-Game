import data.components_master as Components
import esper
import os
import shelve
import tcod as libtcod

from _data import con, eqp, log, map, MULTIPLIER
from camera import Camera
from components.position import PositionComponent
from cursor import Cursor
from load_tileset import load_tileset
from fsm import MainMenu
from map import Map
from typing import Type

' Processors. '
from processors.ai_input import AiInputProcessor
from processors.camera import CameraProcessor
from processors.combat import CombatProcessor
from processors.consumable import ConsumableProcessor
from processors.cooldown import CooldownProcessor
from processors.debug import DebugProcessor
from processors.death import DeathProcessor
from processors.descend import DescendProcessor
from processors.dijkstra import DijkstraProcessor
from processors.discovery import DiscoveryProcessor
from processors.drop import DropProcessor
from processors.energy import EnergyProcessor
from processors.event import EventProcessor
from processors.final import FinalProcessor
from processors.fov import FOVProcessor
from processors.initial import InitialProcessor
from processors.input import InputProcessor
from processors.inventory import InventoryProcessor
from processors.job import JobProcessor
from processors.mapgen import MapgenProcessor
from processors.movement import MovementProcessor
from processors.new_game import NewGameProcessor
from processors.pickup import PickupProcessor
from processors.removable import RemovableProcessor
from processors.render import RenderProcessor
from processors.skill import SkillProcessor
from processors.skill_menu import SkillMenuProcessor
from processors.skill_progression import SkillProgressionProcessor
from processors.soul import SoulProcessor
from processors.state import StateProcessor
from processors.wearable import WearableProcessor

class GameWorld(esper.World):
    def __init__(self):
        super().__init__()
        
        self.build_world()
        
        ' Data. '
        self.key = None
        self.messages = []
        self.messages_offset = 0
        self.mouse_pos = None
        self.popup_menus = []
        self.previous_state = MainMenu
        self.running = True
        self.state = MainMenu
        self.ticker = 0
        self.turn = 0
        self.toggle_debug_mode = False

        ' Objects. '
        self.camera = Camera(x=0, y=0, w=map.w // MULTIPLIER, h=map.h // MULTIPLIER, leash=3) # TODO: The map values from _data might need to be renamed...
        self.consoles = {}
        self.cursor = Cursor()
        self.map = Map(w=50, h=50)

        # Prepare tilset.
        load_tileset()

        # Prepare console.
        self.consoles['con'] = libtcod.console_init_root(con.w, con.h, title='ECS Game', order='F', renderer=libtcod.RENDERER_SDL2, vsync=True), con.x, con.y, con.w, con.h
        self.consoles['stats'] = libtcod.console.Console(eqp.w, eqp.h, order='F'), eqp.x, eqp.y, eqp.w, eqp.h
        self.consoles['log'] = libtcod.console.Console(log.w, log.h, order='F'), log.x, log.y, log.w, log.h
        self.consoles['map'] = libtcod.console.Console(map.w, map.h, order='F'), map.x, map.y, map.w, map.h

    def build_world(self):
        ' Upkeep. '
        self.add_processor(InitialProcessor(), 999)
        ' Render. '
        self.add_processor(CameraProcessor(), 41)
        self.add_processor(RenderProcessor(), 40)
        self.add_processor(DebugProcessor(), 39)
        ' Input. '
        self.add_processor(AiInputProcessor(), 30)
        self.add_processor(InputProcessor(), 30)
        ' Update. '
        self.add_processor(NewGameProcessor(), 25)
        self.add_processor(DiscoveryProcessor(), 21)
        self.add_processor(EventProcessor(), 20)    
        self.add_processor(InventoryProcessor(), 15)
        self.add_processor(SkillProcessor(), 15)
        self.add_processor(ConsumableProcessor(), 10)
        self.add_processor(DescendProcessor(), 10)
        self.add_processor(PickupProcessor(), 10)
        self.add_processor(MovementProcessor(), 10)
        self.add_processor(WearableProcessor(), 10)
        self.add_processor(DropProcessor(), 10)
        self.add_processor(JobProcessor(), 10)
        self.add_processor(CombatProcessor(), 6)
        self.add_processor(SoulProcessor(), 6)
        self.add_processor(RemovableProcessor(), 6)
        self.add_processor(DeathProcessor(), 5)
        self.add_processor(MapgenProcessor(), 4)
        self.add_processor(DijkstraProcessor(), 3)
        self.add_processor(EnergyProcessor(), 3)
        self.add_processor(SkillMenuProcessor(), 3)
        ' Endstep. '
        self.add_processor(SkillProgressionProcessor(), 2)
        self.add_processor(CooldownProcessor(), 2)
        self.add_processor(FOVProcessor(), 1)
        self.add_processor(StateProcessor(), 1)
        self.add_processor(FinalProcessor(), 0)

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
    
    def load_game(self):
        if not os.path.isfile('savegame.dat'):
            state = self.state

            if state is not 'MainMenu':
                message = 'There is no save file to load.'
                self.messages.append({'error': message})
            return 0

        with shelve.open('savegame', 'r') as data_file:
            self.camera = data_file['camera']
            self.map = data_file['map']
            self.messages = data_file['log']
            self.state = data_file['state']
            self.ticker = data_file['ticker']
            self.turn = data_file['turn']
            self._components = data_file['components']
            self._entities = data_file['entities']
            self._next_entity_id = data_file['next_entity_id']

    def save_game(self):
        with shelve.open('savegame', 'n') as data_file:
            data_file['camera'] = self.camera
            data_file['map'] = self.map
            data_file['log'] = self.messages
            data_file['state'] = self.state
            data_file['ticker'] = self.ticker
            data_file['turn'] = self.turn
            data_file['components'] = self._components
            data_file['entities'] = self._entities
            data_file['next_entity_id'] = self._next_entity_id

    def create_entity(self, entity):
        ent = super().create_entity()
        
        for key, value in entity.items():
            if key in Components._fluid_components.values():
                # The entity should receive its own instance of this component.
                self.add_component(ent, key(*value))
            else:
                # All entities can share this component.
                self.add_component(ent, value)
        
        return ent
