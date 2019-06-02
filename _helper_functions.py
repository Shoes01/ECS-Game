from collections import Counter
from components.actor.equipment import EquipmentComponent
from components.soul import SoulComponent
from components.stats import StatsComponent

def generate_stats(ent, world):
    ent_stats = world.component_for_entity(ent, StatsComponent).__dict__
    
    if world.has_component(ent, EquipmentComponent):
        for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
            if world.has_component(item_id, StatsComponent):
                item_stats = Counter(world.component_for_entity(item_id, StatsComponent).__dict__)
                Counter(ent_stats).update(item_stats)

    if world.has_component(ent, SoulComponent):
        ent_soul = world.component_for_entity(ent, SoulComponent)

        # Each position in the soul represents a stat. See soul.py for more details.
        # [[  HP, ATK, MAG],
        #  [ SPD, DEF, RES]]
        ent_stats['hp'] += ent_soul[0][0]
        ent_stats['speed'] += ent_soul[1][0]
        ent_stats['attack'] += ent_soul[0][1]
        ent_stats['defense'] += ent_soul[1][1]
        ent_stats['magic'] += ent_soul[0][2]
        ent_stats['resistance'] += ent_soul[1][2]

    return ent_stats