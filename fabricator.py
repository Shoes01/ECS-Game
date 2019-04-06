import tcod as libtcod

from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.energy import EnergyComponent
from components.actor.equipment import EquipmentComponent
from components.actor.player import PlayerComponent
from components.actor.stats import StatsComponent
from components.actor.velocity import VelocityComponent
from components.game.dijgen import DijgenComponent
from components.game.end_game import EndGameComponent
from components.game.map import MapComponent
from components.game.message_log import MessageLogComponent
from components.game.state import StateComponent
from components.game.turn_count import TurnCountComponent
from components.item.equipped import EquippedComponent
from components.item.item import ItemComponent
from components.item.modifier import ModifierComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent

def fabricate_entity(ent, world):
    if ent == 'game':
        return world.create_entity(
            MapComponent(),
            MessageLogComponent(),
            PersistComponent(),
            StateComponent(),
            TurnCountComponent()
        )

    if ent == 'player':
        return world.create_entity(
            ActorComponent(),
            EnergyComponent(energy=0),
            EquipmentComponent(),
            PersistComponent(),
            PlayerComponent(),
            PositionComponent(),
            RenderComponent(char='@', color=libtcod.pink),
            StatsComponent(hp=50, power=10)
        )
    
    if ent == 'sword':
        return world.create_entity(
            ItemComponent(),
            ModifierComponent(power=5),
            PositionComponent(),
            RenderComponent(char=')', color=libtcod.blue)
        )

    if ent == 'sword_equipped':
        return world.create_entity(
            EquippedComponent(),
            ItemComponent(),
            ModifierComponent(power=2),
            PositionComponent(),
            RenderComponent(char=')', color=libtcod.green)
        )

    if ent == 'zombie':
        return world.create_entity(
            ActorComponent(),
            BrainComponent(),
            EnergyComponent(),
            EquipmentComponent(equipment=[fabricate_entity('sword_equipped', world)]),
            PositionComponent(),
            RenderComponent(char='Z', color=libtcod.green),
            StatsComponent(hp=11, power=5)
        )