import esper
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.combat import CombatComponent
from components.actor.corpse import CorpseComponent
from components.actor.dead import DeadComponent
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.actor.velocity import VelocityComponent
from components.game.events import EventsComponent
from components.item.equipped import EquippedComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent

class DeathProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (dead, eqp, name, pos, ren) in self.world.get_components(DeadComponent, EquipmentComponent, NameComponent, PositionComponent, RenderComponent):
            equipment = eqp.equipment
            name.name = 'corspe of ' + name.name
            ren.char = '%'
            ren.color = libtcod.red

            for item in equipment:
                self.world.remove_component(item, EquippedComponent)
                item_pos = self.world.component_for_entity(item, PositionComponent)
                item_pos.x, item_pos.y = pos.x, pos.y

            if ent == 2:
                self.world.add_component(1, EventsComponent(events=[{'player_killed': True}]))
            else:
                self.world.remove_component(ent, BrainComponent)
            
            self.world.remove_component(ent, ActorComponent)
            if self.world.has_component(ent, CombatComponent): self.world.remove_component(ent, CombatComponent)
            self.world.remove_component(ent, DeadComponent)
            if self.world.has_component(ent, VelocityComponent): self.world.remove_component(ent, VelocityComponent)
            
            self.world.add_component(ent, CorpseComponent())