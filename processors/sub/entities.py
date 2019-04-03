from components.actor.actor import ActorComponent
from components.corpse import CorpseComponent
from components.item.equipped import EquippedComponent
from components.item.item import ItemComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent

def process_entities(console_bundle, world):
    console, x, y, w, h = console_bundle
    for ent, (pos, ren, tile) in world.get_components(PositionComponent, RenderComponent, TileComponent):
        
        if ren.visible:
            console.print(pos.x, pos.y, ren.char, ren.color)
        
        elif ren.explored:
            console.print(pos.x, pos.y, ren.char, ren.explored_color)            

    # Print corpses to the console.
    for ent, (corpse, pos, ren) in world.get_components(CorpseComponent, PositionComponent, RenderComponent):
        if ren.visible:
            console.print(pos.x, pos.y, ren.char, ren.color)

    # Print items.
    for ent, (item, pos, ren) in world.get_components(ItemComponent, PositionComponent, RenderComponent):
        if ren.visible and not world.has_component(ent, EquippedComponent):
            console.print(pos.x, pos.y, ren.char, ren.color)

    # Print entities to the console.
    for ent, (actor, pos, ren) in world.get_components(ActorComponent, PositionComponent, RenderComponent):
        if ren.visible:
            console.print(pos.x, pos.y, ren.char, ren.color)

    # Print the player (again), on top of everything else.
    player_pos = world.component_for_entity(2, PositionComponent)
    player_ren = world.component_for_entity(2, RenderComponent)
    console.print(player_pos.x, player_pos.y, player_ren.char, player_ren.color)