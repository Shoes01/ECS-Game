import esper
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.dead import DeadComponent
from components.actor.stats import StatsComponent
from components.game.message_log import MessageLogComponent

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

            if defender_stats.hp <= 0:
                self.world.add_component(defender_ID, DeadComponent())

            message_log_component.messages.append(
                ('Entity #{0} hits Entity #{1} ({2}/{3} hp).'.format(attacker_ID, defender_ID, defender_stats.hp, defender_stats.hp_max), libtcod.yellow)
            )
            self.world.remove_component(ent, CombatComponent)