from collections import Counter
from components.actor.equipment import EquipmentComponent
from components.stats import StatsComponent

def generate_stats(ent, world):
    ent_stats = world.component_for_entity(ent, StatsComponent).__dict__
    if not world.has_component(ent, EquipmentComponent):
        return ent_stats
    
    ent_stats = Counter(ent_stats)

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        if world.has_component(item_id, StatsComponent):
            item_stats = Counter(world.component_for_entity(item_id, StatsComponent).__dict__)
            ent_stats.update(item_stats)

    return ent_stats