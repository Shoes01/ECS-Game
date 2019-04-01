import esper
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.dead import DeadComponent
from components.actor.stats import StatsComponent
from components.game.message_log import MessageLogComponent
from components.render import RenderComponent

class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (act, com) in self.world.get_components(ActorComponent, CombatComponent):
            attacker_ID = ent
            defender_ID = self.world.component_for_entity(attacker_ID, CombatComponent).defender_ID

            message_log_component = self.world.component_for_entity(1, MessageLogComponent)

            if not self.world.has_component(defender_ID, ActorComponent):
                return 0

            attacker_stats = self.world.component_for_entity(attacker_ID, StatsComponent)
            defender_stats = self.world.component_for_entity(defender_ID, StatsComponent)

            defender_stats.hp -= attacker_stats.power

            att_ren = self.world.component_for_entity(attacker_ID, RenderComponent)
            def_ren = self.world.component_for_entity(defender_ID, RenderComponent)

            message_log_component.messages.insert(0, {'combat': (att_ren.char, att_ren.color, def_ren.char, def_ren.color)})

            if defender_stats.hp <= 0:
                self.world.add_component(defender_ID, DeadComponent())
                message_log_component.messages.insert(0, {'death': (def_ren.char, def_ren.color)})



            self.world.remove_component(ent, CombatComponent)