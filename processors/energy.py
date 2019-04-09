import esper

from components.actor.combat import CombatComponent
from components.actor.consume import ConsumeComponent
from components.actor.energy import EnergyComponent
from components.actor.pickup import PickupComponent
from components.actor.player import PlayerComponent
from components.actor.velocity import VelocityComponent
from components.actor.wait import WaitComponent
from components.game.redraw import RedrawComponent
from components.game.turn_count import TurnCountComponent

class EnergyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (eng) in self.world.get_component(EnergyComponent):
            if self.world.has_component(ent, CombatComponent):
                eng.energy += 10
                self.world.remove_component(ent, CombatComponent)
            
            elif self.world.has_component(ent, ConsumeComponent):
                eng.energy += 10
                self.world.remove_component(ent, ConsumeComponent)

            elif self.world.has_component(ent, PickupComponent):
                eng.energy += 10
                self.world.remove_component(ent, PickupComponent)

            elif self.world.has_component(ent, VelocityComponent):
                eng.energy += 10
                self.world.remove_component(ent, VelocityComponent)

            elif self.world.has_component(ent, WaitComponent):
                eng.energy += 10
                self.world.remove_component(ent, WaitComponent)
            
            elif ent == 1 and eng.energy == 0:
                # This tracks the turn number.
                eng.energy += 10
                self.world.component_for_entity(ent, TurnCountComponent).turn_count += 1

        deincrement = True
        for ent, (eng, player) in self.world.get_components(EnergyComponent, PlayerComponent):
            if eng.energy == 0:
                self.world.component_for_entity(1, RedrawComponent).redraw = True
                deincrement = False

        if deincrement:
            for ent, (eng) in self.world.get_component(EnergyComponent):
                if eng.energy > 0:
                    eng.energy -= 1