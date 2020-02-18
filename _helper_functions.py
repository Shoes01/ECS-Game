from collections import Counter
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.skill import SkillComponent
from components.soul import SoulComponent
from components.stats import StatsComponent

def generate_stats(ent, world, include_upkeep=True):    
    ent_stats = Counter(world.component_for_entity(ent, StatsComponent).__dict__)
    
    if ent is not 1: # This is maybe temporary...
        return ent_stats

    # Stat changes based on equipment.
    if world.has_component(ent, EquipmentComponent):
        for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
            if world.has_component(item_id, StatsComponent):
                item_stats = Counter(world.component_for_entity(item_id, StatsComponent).__dict__)
                ent_stats.update(item_stats)

    # Stat changes based on job.
    if include_upkeep:
        ent_stats.update(Counter(world.component_for_entity(ent, JobComponent).upkeep))
        
    # Stat changes based on soul.
    if world.has_component(ent, SoulComponent):
        ent_soul = Counter(world.component_for_entity(ent, SoulComponent).soul)
        ent_stats.update(ent_soul)

    return dict(ent_stats)

def as_decimal(number, signed=False):
    string = str(number)

    if string == '0':
        string = '0.0'
    elif len(string) == 1:
        string = "0." + string
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

def create_skill(_json_data, name, slot=""):
    ap_max = _json_data[name].get('ap_max')
    cooldown = _json_data[name].get('cooldown')
    cost_energy = _json_data[name].get('cost_energy')
    cost_soul = _json_data[name].get('cost_soul')
    damage_type = _json_data[name].get('damage_type')
    description = _json_data[name].get('description')
    east = _json_data[name].get('east')
    if _json_data[name].get('job_requirement') is None: print(f"Item {name} has no job_requirement.")
    job_req = _json_data[name].get('job_requirement')
    north_east = _json_data[name].get('north_east')

    return SkillComponent(ap_max=ap_max, cooldown=cooldown, cost_energy=cost_energy, cost_soul=cost_soul, damage_type=damage_type, description=description, job_req=job_req, name=name, east=east, north_east=north_east, slot=slot)