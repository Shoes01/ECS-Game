from components.actor.equipment import EquipmentComponent
from components.stats import StatsComponent

def calculate_attack(ent, world):
    attack = world.component_for_entity(ent, StatsComponent).attack

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        attack += world.component_for_entity(item_id, StatsComponent).attack

    return attack