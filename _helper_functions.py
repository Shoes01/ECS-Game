from components.actor.actor import ActorComponent
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.modifier import ModifierComponent
from components.position import PositionComponent

def tile_occupied(world, x, y):
    for ent, (actor, pos) in world.get_components(ActorComponent, PositionComponent):
        if pos.x == x and pos.y == y:
            return ent
    
    return False

def calculate_power(ent, world):        
    power = world.component_for_entity(ent, StatsComponent).power

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        power += world.component_for_entity(item_id, ModifierComponent).power

    return power