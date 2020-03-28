from collections import Counter
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.soul import SoulComponent
from components.stats import StatsComponent

import data.stats as Stats

# TODO: Things have changed big time. I should probably check that this still works.
# It should be easy though... ATK = stats[Stats.ATK] + item[Stats.ATK] - job.upkeep[Stats.ATK] + soul[Stats.ATK]

def generate_stats(ent, world, include_upkeep=True):
    blank = {stat: 0 for stat in Stats.all.values()}
    stats = world.component_for_entity(ent, StatsComponent).as_dict

    # At the moment, only the player entity gains stats from items, soul, etc.
    if ent is not 1:
        return stats

    # Stat changes based on equipment.
    item_stats = blank.copy()
    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        single_item_stats = world.component_for_entity(item_id, StatsComponent).as_dict
        for stat in Stats.all.values():
            if single_item_stats.get(stat):
                item_stats[stat] += single_item_stats[stat]
    
    # Stat changes based on job upkeep.
    job_upkeep = world.component_for_entity(ent, JobComponent).upkeep
    for stat in Stats.all.values():
        if job_upkeep.get(stat) is None:
            job_upkeep[stat] = 0
    if not include_upkeep:
        job_upkeep = blank.copy()
    
    # Stat changes based on soul.
    soul = world.component_for_entity(ent, SoulComponent).soul

    for stat in Stats.all.values():
        stats[stat] = stats[stat] + item_stats[stat] - job_upkeep[stat] + soul[stat]
    
    return stats

def as_decimal(number, signed=False):
    string = str(number)
    # TODO: This is commented out, as I find a way to change how pseudo-decimals work.
    """
    if string == '0':
        string = '0.0'
    elif len(string) == 1:
        string = "0." + string
    else:
        string = string[:-1] + '.' + string[-1]
    """
    if signed:
        if number >= 0:
            string = '+' + string
    
    return string

def as_integer(number, signed=False):    
    string = str(number)
    # TODO: This is commented out, as I find a way to change how pseudo-decimals work.
    """
    if string != '0':
        string = string[:-1]
    elif string[-1] != '0':
        print('HOLD UP: This digit should be 0, not {}'.format(string[-1]))
    """
        
    if signed:
        if number >= 0:
            string = '+' + string
    
    return string
