from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.modifier import ModifierComponent

def calculate_atk(ent, world):
    atk = world.component_for_entity(ent, StatsComponent).atk

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        atk += world.component_for_entity(item_id, ModifierComponent).atk

    return atk