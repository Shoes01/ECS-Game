import data.entities as Entities
import esper

from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.corpse import CorpseComponent
from components.actor.inventory import InventoryComponent
from components.actor.player import PlayerComponent
from components.furniture import FurnitureComponent
from components.item.consumable import ConsumableComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.soul import SoulComponent
from data.render import ENTITY_COLORS, SPRITES
from processors.state import StateProcessor
from queue import Queue

class DeathProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            inv = self.world.component_for_entity(ent, InventoryComponent)
            name = self.world.component_for_entity(ent, NameComponent)
            pos = self.world.component_for_entity(ent, PositionComponent)
            ren = self.world.component_for_entity(ent, RenderComponent)

            if self.world.has_component(ent, CorpseComponent):
                print(f"Entity {name.original_name} has died an additional time. Position: {pos.x}, {pos.y}")
                return 0

            is_furniture = self.world.has_component(ent, FurnitureComponent)
            self.world.messages.append({'death': (ren.char, ren.color_fg, self.world.turn, is_furniture)})
            
            inventory = inv.inventory
            name.name = 'corspe of ' + name.name
            ren.char = '%'
            ren.codepoint = SPRITES['corpse']
            ren.color_fg = ENTITY_COLORS['corpse']
            
            # Drop the items the entity is carrying.
            for item in inventory:
                self.world.add_component(item, PositionComponent(x=pos.x, y=pos.y))
                if self.world.has_component(item, PersistComponent):
                    self.world.remove_component(item, PersistComponent)

            # Drop the soul the entity is carrying.
            if self.world.has_component(ent, SoulComponent):
                # Create an item. Give it a position and a render component. Make it consumable. Name it a Soul Jar.
                soul_jar = self.world.create_entity(Entities.SOUL_JAR)
                soul = self.world.component_for_entity(ent, SoulComponent)
                soul_jar_con = self.world.component_for_entity(soul_jar, ConsumableComponent)
                soul_jar_con.effects['soul'] = soul # BUG: At some point, this dict gets turned into a None.
                soul_jar_pos = self.world.component_for_entity(soul_jar, PositionComponent)
                soul_jar_pos.x = pos.x
                soul_jar_pos.y = pos.y

            if is_furniture:
                self.world.delete_entity(ent)
                return 0
            elif ent == 1:
                self.world.remove_component(ent, PlayerComponent)
                self.world.get_processor(StateProcessor).queue.put({'player_killed': True})
            else:
                self.world.remove_component(ent, BrainComponent)
            
            if self.world.has_component(ent, BossComponent):
                self.world.get_processor(StateProcessor).queue.put({'boss_killed': True})

            self.world.remove_component(ent, ActorComponent)
            
            self.world.add_component(ent, CorpseComponent())