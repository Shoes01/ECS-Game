import os
import shelve

from components.actor.actor import ActorComponent
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.modifier import ModifierComponent
from components.position import PositionComponent

def calculate_power(ent, world):        
    power = world.component_for_entity(ent, StatsComponent).power

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        power += world.component_for_entity(item_id, ModifierComponent).power

    return power

def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        next_entity_id = data_file['next_entity_id']
        components = data_file['components']
        entities = data_file['entities']

    return next_entity_id, components, entities

def save_game(next_entity_id, components, entities):
    with shelve.open('savegame', 'n') as data_file:
        data_file['next_entity_id'] = next_entity_id
        data_file['components'] = components
        data_file['entities'] = entities

def tile_occupied(world, x, y):
    for ent, (actor, pos) in world.get_components(ActorComponent, PositionComponent):
        if pos.x == x and pos.y == y:
            return ent
    
    return False