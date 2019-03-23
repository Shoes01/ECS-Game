from components.actor.actor import ActorComponent
from components.position import PositionComponent

def tile_occupied(world, x, y):
    for ent, (actor, pos) in world.get_components(ActorComponent, PositionComponent):
        if pos.x == x and pos.y == y:
            return True
    
    return False