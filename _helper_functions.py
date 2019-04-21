import os
import shelve

from components.actor.actor import ActorComponent
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.item import ItemComponent
from components.item.modifier import ModifierComponent
from components.position import PositionComponent

def calculate_power(ent, world):
    power = world.component_for_entity(ent, StatsComponent).power

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        power += world.component_for_entity(item_id, ModifierComponent).power

    return power

def load_game(world):
    if not os.path.isfile('savegame.dat'):
        state = world.state

        if state is not 'MainMenu':
            message = 'There is no save file to load.'
            world.messages.append({'error': message})
        return 0

    with shelve.open('savegame', 'r') as data_file:
        world._next_entity_id = data_file['next_entity_id']
        world._components = data_file['components']
        world._entities = data_file['entities']
        world.messages = data_file['log']
        world.state_stack = data_file['state']
        world.ticker = data_file['ticker']
        world.map = data_file['map']

def loot_algorithm(chance, monster, item, floor):
    net_rarity = (1 + (monster)*5 - (item - 3)*5 + (floor)*5)
    if chance > (100 - net_rarity):
        return True
    return False

def save_game(world):
    with shelve.open('savegame', 'n') as data_file:
        data_file['next_entity_id'] = world._next_entity_id
        data_file['components'] = world._components
        data_file['entities'] = world._entities
        data_file['log'] = world.messages
        data_file['state'] = world.state_stack
        data_file['ticker'] = world.ticker
        data_file['map'] = world.map