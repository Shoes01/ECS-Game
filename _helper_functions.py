from collections import Counter
from components.actor.equipment import EquipmentComponent
from components.soul import SoulComponent
from components.stats import StatsComponent

def generate_stats(ent, world):    
    ent_stats = Counter(world.component_for_entity(ent, StatsComponent).__dict__)
    
    if ent is not 1: # This is maybe temporary...
        return ent_stats

    if world.has_component(ent, EquipmentComponent):
        for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
            if world.has_component(item_id, StatsComponent):
                item_stats = Counter(world.component_for_entity(item_id, StatsComponent).__dict__)
                ent_stats.update(item_stats)
        
    if world.has_component(ent, SoulComponent):
        ent_soul = Counter(world.component_for_entity(ent, SoulComponent).soul)
        ent_stats.update(ent_soul)

    return dict(ent_stats)

def as_decimal(number, signed=False):
    string = str(number)

    if string == '0':
        string = '0.0'
    else:
        string = string[:-1] + '.' + string[-1]

    if signed:
        if number >= 0:
            string = '+' + string
    
    return string

def as_integer(number, signed=False):
    string = str(number)

    if string != '0':
        string = string[:-1]
    elif string[-1] != '0':
        print('HOLD UP: This digit should be 0, not {}'.format(string[-1]))
        
    if signed:
        if number >= 0:
            string = '+' + string
    
    return string

