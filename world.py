import esper
import json
import tcod as libtcod

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.energy import EnergyComponent
from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.player import PlayerComponent
from components.actor.stats import StatsComponent
from components.actor.velocity import VelocityComponent
from components.game.dijgen import DijgenComponent
from components.game.end_game import EndGameComponent
from components.game.map import MapComponent
from components.game.message_log import MessageLogComponent
from components.game.popup import PopupComponent
from components.game.redraw import RedrawComponent
from components.game.state import StateComponent
from components.game.turn_count import TurnCountComponent
from components.item.consumable import ConsumableComponent
from components.item.item import ItemComponent
from components.item.modifier import ModifierComponent
from components.item.pickedup import PickedupComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.furniture import FurnitureComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stairs import StairsComponent
from components.tile import TileComponent
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
from processors.state import StateProcessor
from processors.wearable import WearableProcessor

class CustomWorld(esper.World):
    def __init__(self):
        super().__init__()
        self._json_data = self.load_data()
    
    def load_data(self):
        data = None

        with open("data/items.json", "r") as read_file:
            data = json.load(read_file)
        with open("data/monsters.json", "r") as read_file:
            data.update(json.load(read_file))
        with open("data/tiles.json", "r") as read_file:
            data.update(json.load(read_file))
        
        return data
    
    def create_entity(self, entity):
        # TODO: Fix this somehow? Move the game entity to JSON as well?
        if entity == 'game':
            return super().create_entity(
                EnergyComponent(),
                MapComponent(),
                MessageLogComponent(),
                PersistComponent(),
                PopupComponent(),
                RedrawComponent(),
                StateComponent(),
                TurnCountComponent()
            )
        elif entity == 'player':
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
                    super().add_component(ent, ActorComponent())
                    super().add_component(ent, EnergyComponent())
                    super().add_component(ent, EquipmentComponent())
                    super().add_component(ent, InventoryComponent())
                    super().add_component(ent, PositionComponent())
                elif value == 'item':
                    super().add_component(ent, ItemComponent())
                    super().add_component(ent, PositionComponent())
            
            # Now just look for each and every component possible...
            elif key == 'actor':
                super().add_component(ent, ActorComponent())
            
            elif key == 'boss':
                super().add_component(ent, BossComponent())
            
            elif key == 'brain':
                super().add_component(ent, BrainComponent())
            
            elif key == 'energy':
                super().add_component(ent, EnergyComponent())
            
            elif key == 'equipment':
                super().add_component(ent, EquipmentComponent())
            
            elif key == 'item':
                super().add_component(ent, ItemComponent())
            
            elif key == 'inventory':
                super().add_component(ent, InventoryComponent())
            
            elif key == 'modifier':
                power = value.get('power')
                super().add_component(ent, ModifierComponent(power=power))
            
            elif key == 'name':
                name = value.get('name')
                super().add_component(ent, NameComponent(name=name))
            
            elif key == 'position':
                super().add_component(ent, PositionComponent())
            
            elif key == 'render':
                char = value.get('char')
                color = value.get('color')
                explored_color = value.get('explored_color')
                super().add_component(ent, RenderComponent(char=char, color=ENTITY_COLORS[color], explored_color=ENTITY_COLORS.get('explored_color')))
            
            elif key == 'slot':
                slot = value.get('slot')
                super().add_component(ent, SlotComponent(slot=slot))
            
            elif key == 'stairs':
                super().add_component(ent, StairsComponent())
            
            elif key == 'stats':
                hp = value.get('hp')
                power = value.get('power')
                super().add_component(ent, StatsComponent(hp=hp, power=power))

            elif key == 'tile':
                blocks_path = value.get('blocks_path')
                blocks_sight = value.get('blocks_sight')
                super().add_component(ent, TileComponent(blocks_path=blocks_path, blocks_sight=blocks_sight))
            
            elif key == 'wearable':
                super().add_component(ent, WearableComponent())
        
        return ent

def build_world():
    # Create world.
    world = CustomWorld()

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
    state_processor = StateProcessor()
    wearable_processor = WearableProcessor()
    
    # Add them to the world.
    ## UPKEEP
    world.add_processor(initial_processor, 999)
    ## RENDER
    world.add_processor(render_processor, 40)
    world.add_processor(debug_processor, 39)
    ## INPUT
    world.add_processor(ai_input_processor, 30)
    world.add_processor(input_processor, 30)
    ## UPDATE
    world.add_processor(action_processor, 20)
    world.add_processor(event_processor, 20)    
    world.add_processor(inventory_processor, 15)
    world.add_processor(consumable_processor, 10)
    world.add_processor(descent_processor, 10)
    world.add_processor(pickup_processor, 10)
    world.add_processor(movement_processor, 10)
    world.add_processor(wearable_processor, 10)
    world.add_processor(drop_processor, 10)
    world.add_processor(combat_processor, 5)
    world.add_processor(removable_processor, 5)
    world.add_processor(death_processor, 4)
    world.add_processor(mapgen_processor, 3)
    world.add_processor(dijkstra_processor, 2)
    world.add_processor(energy_processor, 2)
    ## ENDSTEP
    world.add_processor(state_processor, 1)
    world.add_processor(final_processor, 0)

    return world