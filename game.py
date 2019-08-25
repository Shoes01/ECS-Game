import esper
import json
import os
import shelve
import tcod as libtcod

from _data import ENTITY_COLORS, con, eqp, log, map, SPRITES, MULTIPLIER
from camera import Camera
from cursor import Cursor
from load_tileset import load_tileset
from map import Map
from typing import Type

' Components. '
from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.energy import EnergyComponent
from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.actor.job import JobComponent
from components.actor.player import PlayerComponent
from components.actor.race import RaceComponent
from components.item.consumable import ConsumableComponent
from components.item.item import ItemComponent
from components.item.jobreq import JobReqComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.furniture import FurnitureComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.rarity import RarityComponent
from components.render import RenderComponent
from components.soul import SoulComponent
from components.stairs import StairsComponent
from components.stats import StatsComponent
from components.tile import TileComponent

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
from processors.pickup import PickupProcessor
from processors.removable import RemovableProcessor
from processors.render import RenderProcessor
from processors.skill import SkillProcessor
from processors.skill_directory import SkillDirectoryProcessor
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
        self.running = True
        self.state = 'MainMenu'
        self.ticker = 0
        self.turn = 0
        self.toggle_debug_mode = False
        self._json_data = self.load_data()

        ' Tables. '
        self.item_table, self.job_skill_table, self.monster_table = self.load_tables()

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
        ' Endstep. '
        self.add_processor(SkillDirectoryProcessor(), 2)
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

    def load_data(self):
        data = None

        with open("data/consumables.json", "r") as read_file:
            data = json.load(read_file)
        with open("data/equipment.json", "r") as read_file:
            data.update(json.load(read_file))
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
            self.camera = data_file['camera']
            self.map = data_file['map']
            self.messages = data_file['log']
            self.state = data_file['state']
            self.ticker = data_file['ticker']
            self.turn = data_file['turn']
            self._components = data_file['components']
            self._entities = data_file['entities']
            self._next_entity_id = data_file['next_entity_id']
            
    def load_tables(self):
        item_table = [[] for i in range(8)] # There are 8 levels of rarity, starting at 0
        monster_table = [[] for i in range(8)]
        job_skill_table = {}
        
        for ent, components in self._json_data.items():
            if ent == 'comment': continue
            rarity = components.get('rarity')
            archtype = components.get('archtype')
            if rarity is not None:
                job, skill = None, None
                if archtype == 'monster':
                    monster_table[rarity].append(ent)
                elif archtype == 'item':
                    item_table[rarity].append(ent)
                    job = components.get('job requirement').get('job')
                    skill = components.get('skill')
                if job and skill:
                    if job in job_skill_table:
                        job_skill_table[job].append(skill)
                    else:
                        job_skill_table[job] = [skill,]
                    
        
        return item_table, job_skill_table, monster_table

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
        # TODO: Fix this somehow? Move the game entity to JSON as well?
        if entity == 'player':
            return super().create_entity(
                ActorComponent(),
                EnergyComponent(energy=0),
                EquipmentComponent(),
                InventoryComponent(),
                JobComponent(job='soldier', upkeep={}), # TODO: This doesn't talk to JOBS found in _jobs.py ...
                NameComponent(name='Player'),
                PersistComponent(),
                PlayerComponent(),
                RaceComponent(race='human'),
                PositionComponent(),
                RenderComponent(color_bg=None, char='@', codepoint=SPRITES['player'], color_fg=ENTITY_COLORS['player'], color_explored=None),
                SkillDirectoryComponent(),
                SoulComponent(eccentricity=5, max_rarity=10),
                StatsComponent(hp=500, attack=10)
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
                    self.add_component(ent, SkillDirectoryComponent())
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
            
            elif key == 'consumable':
                self.add_component(ent, ConsumableComponent(effects=value))

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

            elif key == 'job requirement':
                job = value.get('job')
                self.add_component(ent, JobReqComponent(job_req=job))
            
            elif key == 'name':
                name = value.get('name')
                self.add_component(ent, NameComponent(name=name))
            
            elif key == 'position':
                self.add_component(ent, PositionComponent())
            
            elif key == 'rarity':
                rarity = value
                self.add_component(ent, RarityComponent(rarity=rarity))

            elif key == 'render':
                color_bg = value.get('color_bg')
                char = value.get('char')
                codepoint = value.get('codepoint')
                color_fg = value.get('color_fg')
                color_explored = value.get('color_explored')
                self.add_component(ent, RenderComponent(color_bg=ENTITY_COLORS.get(color_bg), char=char, codepoint=SPRITES[codepoint], color_fg=ENTITY_COLORS[color_fg], color_explored=ENTITY_COLORS.get(color_explored)))

            elif key == 'skill':
                name = value
                ap_max = self._json_data.get(name).get('ap_max')
                cooldown = self._json_data.get(name).get('cooldown')
                cost_energy = self._json_data.get(name).get('cost_energy')
                cost_soul = self._json_data.get(name).get('cost_soul')
                damage_type = self._json_data.get(name).get('damage_type')
                description = self._json_data.get(name).get('description')
                east = self._json_data.get(name).get('east')
                north_east = self._json_data.get(name).get('north_east')
                self.add_component(ent, ItemSkillComponent(ap_max=ap_max, cooldown=cooldown, cost_energy=cost_energy, cost_soul=cost_soul, damage_type=damage_type, description=description, name=name, east=east, north_east=north_east))

            elif key == 'slot':
                slot = value.get('slot')
                self.add_component(ent, SlotComponent(slot=slot))
            
            elif key == 'soul':
                eccentricity = value.get('eccentricity')
                max_rarity = value.get('max_rarity')
                self.add_component(ent, SoulComponent(eccentricity=eccentricity, max_rarity=max_rarity))

            elif key == 'stairs':
                self.add_component(ent, StairsComponent())
            
            elif key == 'stats':
                hp = value.get('hp')
                attack = value.get('attack')
                defense = value.get('defense')
                magic = value.get('magic')
                resistance = value.get('resistance')
                speed = value.get('speed')
                self.add_component(ent, StatsComponent(hp=hp, attack=attack, defense=defense, magic=magic, resistance=resistance, speed=speed))

            elif key == 'tile':
                blocks_path = value.get('blocks_path')
                blocks_sight = value.get('blocks_sight')
                self.add_component(ent, TileComponent(blocks_path=blocks_path, blocks_sight=blocks_sight))
            
            elif key == 'wearable':
                self.add_component(ent, WearableComponent())
        
        return ent
