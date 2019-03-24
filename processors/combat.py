import esper

from components.actor.combat import CombatComponent
from components.actor.stats import StatsComponents

class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (com) in self.world.get_component(CombatComponent):
            attacker_ID = ent
            defender_ID = self.world.component_for_entity(attacker_ID, CombatComponent).defender_ID

            attacker_stats = self.world.component_for_entity(attacker_ID, StatsComponents)
            defender_stats = self.world.component_for_entity(defender_ID, StatsComponents)

            defender_stats.hp -= attacker_stats.power