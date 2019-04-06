import esper
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.combat import CombatComponent
from components.actor.corpse import CorpseComponent
from components.actor.dead import DeadComponent
from components.actor.stats import StatsComponent
from components.actor.velocity import VelocityComponent
from components.game.event import EventComponent
from components.render import RenderComponent

class DeathProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (dead) in self.world.get_component(DeadComponent):
            render_component = self.world.component_for_entity(ent, RenderComponent)

            render_component.char = '%'
            render_component.color = libtcod.red

            if ent == 2:
                self.world.add_component(1, EventComponent(event={'player_killed': True}))
            else:
                self.world.remove_component(ent, BrainComponent)
            
            self.world.remove_component(ent, ActorComponent)
            if self.world.has_component(ent, CombatComponent): self.world.remove_component(ent, CombatComponent)
            self.world.remove_component(ent, DeadComponent)
            if self.world.has_component(ent, VelocityComponent): self.world.remove_component(ent, VelocityComponent)
            
            self.world.add_component(ent, CorpseComponent())