import esper

from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.energy import EnergyComponent
from components.actor.equip import EquipComponent
from components.actor.player import PlayerComponent
from components.actor.velocity import VelocityComponent
from components.actor.wait import WaitComponent
from components.game.redraw import RedrawComponent

class EnergyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (actor, eng) in self.world.get_components(ActorComponent, EnergyComponent):
            if self.world.has_component(ent, CombatComponent):
                eng.energy += 10
                self.world.remove_component(ent, CombatComponent)
            
            elif self.world.has_component(ent, EquipComponent):
                eng.energy += 10
                self.world.remove_component(ent, EquipComponent)

            elif self.world.has_component(ent, VelocityComponent):
                eng.energy += 10
                self.world.remove_component(ent, VelocityComponent)

            elif self.world.has_component(ent, WaitComponent):
                eng.energy += 10
                self.world.remove_component(ent, WaitComponent)

        deincrement = True
        for ent, (eng, player) in self.world.get_components(EnergyComponent, PlayerComponent):
            if eng.energy == 0:
                self.world.component_for_entity(1, RedrawComponent).redraw = True
                deincrement = False

        if deincrement:
            for ent, (actor, eng) in self.world.get_components(ActorComponent, EnergyComponent):
                if eng.energy > 0:
                    eng.energy -= 1