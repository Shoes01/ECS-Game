from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.modifier import ModifierComponent

def calculate_power(ent, world):
    power = world.component_for_entity(ent, StatsComponent).power

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        power += world.component_for_entity(item_id, ModifierComponent).power

    return power