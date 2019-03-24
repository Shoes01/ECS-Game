import esper
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.combat import CombatComponent
from components.actor.dead import DeadComponent
from components.actor.stats import StatsComponent
from components.corpse import CorpseComponent
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
                self.world.component_for_entity(1, EventComponent).event = 'PlayerKilled'
            else:
                self.world.remove_component(ent, BrainComponent)
            
            self.world.remove_component(ent, ActorComponent)
            self.world.remove_component(ent, CombatComponent)
            self.world.remove_component(ent, DeadComponent)
            self.world.remove_component(ent, StatsComponent)
            
            self.world.add_component(ent, CorpseComponent())