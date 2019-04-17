import esper

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.combat import CombatComponent
from components.actor.corpse import CorpseComponent
from components.actor.dead import DeadComponent
from components.actor.inventory import InventoryComponent
from components.actor.stats import StatsComponent
from components.actor.velocity import VelocityComponent
from components.game.events import EventsComponent
from components.game.message_log import MessageLogComponent
from components.game.turn_count import TurnCountComponent
from components.item.pickedup import PickedupComponent
from components.furniture import FurnitureComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.render import RenderComponent

class DeathProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (dead, inv, name, pos, ren) in self.world.get_components(DeadComponent, InventoryComponent, NameComponent, PositionComponent, RenderComponent):
            turn = self.world.component_for_entity(1, TurnCountComponent).turn_count
            is_furniture = self.world.has_component(ent, FurnitureComponent)
            self.world.component_for_entity(1, MessageLogComponent).messages.append({'death': (ren.char, ren.color, turn, is_furniture)})
            
            inventory = inv.inventory
            name.name = 'corspe of ' + name.name
            ren.char = '%'
            ren.color = ENTITY_COLORS['corpse']

            for item in inventory:
                self.world.remove_component(item, PickedupComponent)
                item_pos = self.world.component_for_entity(item, PositionComponent)
                item_pos.x, item_pos.y = pos.x, pos.y
                if self.world.has_component(item, PersistComponent):
                    self.world.remove_component(item, PersistComponent)

            if is_furniture:
                self.world.delete_entity(ent)
                return 0
            elif ent == 2:
                self.world.add_component(1, EventsComponent(events=[{'player_killed': True}]))
            else:
                self.world.remove_component(ent, BrainComponent)
            
            if self.world.has_component(ent, BossComponent):
                self.world.add_component(1, EventsComponent(events=[{'boss_killed': True}]))

            self.world.remove_component(ent, ActorComponent)
            if self.world.has_component(ent, CombatComponent): self.world.remove_component(ent, CombatComponent)
            self.world.remove_component(ent, DeadComponent)
            if self.world.has_component(ent, VelocityComponent): self.world.remove_component(ent, VelocityComponent)
            
            self.world.add_component(ent, CorpseComponent())