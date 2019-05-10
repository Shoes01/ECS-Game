import esper

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.corpse import CorpseComponent
from components.actor.inventory import InventoryComponent
from components.actor.stats import StatsComponent
from components.furniture import FurnitureComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.render import RenderComponent
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

            is_furniture = self.world.has_component(ent, FurnitureComponent)
            self.world.messages.append({'death': (ren.char, ren.color, self.world.turn, is_furniture)})
            
            inventory = inv.inventory
            name.name = 'corspe of ' + name.name
            ren.char = '%'
            ren.color = ENTITY_COLORS['corpse']

            for item in inventory:
                self.world.add_component(item, PositionComponent(x=pos.x, y=pos.y))
                if self.world.has_component(item, PersistComponent):
                    self.world.remove_component(item, PersistComponent)

            if is_furniture:
                self.world.delete_entity(ent)
                return 0
            elif ent == 1:
                self.world.events.append({'player_killed': True})
            else:
                self.world.remove_component(ent, BrainComponent)
            
            if self.world.has_component(ent, BossComponent):
                self.world.events.append({'boss_killed': True})

            self.world.remove_component(ent, ActorComponent)
            
            self.world.add_component(ent, CorpseComponent())