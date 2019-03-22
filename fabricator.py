import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.has_turn import HasTurnComponent
from components.actor.waiting_turn import WaitingTurnComponent
from components.game.event import EventComponent
from components.game.state import StateComponent
from components.persist import PersistComponent
from components.player import PlayerComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent
from components.velocity import VelocityComponent

def fabricate_entity(ent, world):
    if ent == 'game':
        world.create_entity(
            EventComponent(),
            PersistComponent(),
            StateComponent()
        )

    if ent == 'player':
        world.create_entity(
            ActorComponent(),
            HasTurnComponent(),
            PersistComponent(),
            PlayerComponent(),
            PositionComponent(),
            RenderComponent(char='@', color=libtcod.white),
            WaitingTurnComponent()
        )
    
    if ent == 'zombie':
        world.create_entity(
            ActorComponent(),
            PositionComponent(),
            RenderComponent(char='Z', color=libtcod.green),
            WaitingTurnComponent()
        )