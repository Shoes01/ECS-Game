import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.player_input import PlayerInputComponent
from components.actor.stats import StatsComponent
from components.game.dijgen import DijgenComponent
from components.game.event import EventComponent
from components.game.map import MapComponent
from components.game.message_log import MessageLogComponent
from components.game.processor import ProcessorComponent
from components.game.state import StateComponent
from components.persist import PersistComponent
from components.player import PlayerComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent
from components.velocity import VelocityComponent

def fabricate_entity(ent, world):
    if ent == 'game':
        return world.create_entity(
            EventComponent(),
            MapComponent(),
            MessageLogComponent(),
            PersistComponent(),
            ProcessorComponent(),
            StateComponent()
        )

    if ent == 'player':
        return world.create_entity(
            ActorComponent(),
            PlayerInputComponent(),
            PersistComponent(),
            PlayerComponent(),
            PositionComponent(),
            RenderComponent(char='@', color=libtcod.pink),
            StatsComponent(hp=50, power=10)
        )
    
    if ent == 'zombie':
        return world.create_entity(
            ActorComponent(),
            BrainComponent(),
            PositionComponent(),
            RenderComponent(char='Z', color=libtcod.green),
            StatsComponent(hp=11, power=5)
        )