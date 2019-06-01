from components.actor.equipment import EquipmentComponent
from components.stats import StatsComponent

def calculate_attack(ent, world):
    attack = world.component_for_entity(ent, StatsComponent).attack

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        attack += world.component_for_entity(item_id, StatsComponent).attack

    return attack

def calculate_magic_attack(ent, world):
    magic = world.component_for_entity(ent, StatsComponent).magic

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        magic += world.component_for_entity(item_id, StatsComponent).magic

    return magic