import esper

from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from components.actor.skill_execute import SkillExecutionComponent
from queue import Queue

class EnergyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            _bump_attack = event.get('bump_attack')
            _consume = event.get('consume')
            _descend = event.get('descend')
            _drop = event.get('drop')
            _move = event.get('move')
            _pick_up = event.get('pick_up')
            _remove = event.get('remove')
            _wear = event.get('wear')

            if _bump_attack:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _consume:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _descend:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _drop:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _move:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _pick_up:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _remove:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _wear:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10

        if self.world.component_for_entity(1, EnergyComponent).energy == 0:
            return 0

        self.world.redraw = True

        for ent, (eng) in self.world.get_component(EnergyComponent):
            if eng.energy > 0:
                eng.energy -= 1
