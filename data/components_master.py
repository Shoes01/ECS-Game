import data.stats as Stats

from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.corpse import CorpseComponent
from components.actor.diary import DiaryComponent
from components.actor.energy import EnergyComponent
from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.job import JobComponent
from components.actor.player import PlayerComponent
from components.actor.race import RaceComponent
from components.item.consumable import ConsumableComponent
from components.item.item import ItemComponent
from components.item.jobreq import JobReqComponent
from components.item.skill_pool import SkillPoolComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.furniture import FurnitureComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.rarity import RarityComponent
from components.render import RenderComponent
from components.soul import SoulComponent
from components.stairs import StairsComponent
from components.stats import StatsComponent
from components.tile import TileComponent

# Actor Components
ACTOR = ActorComponent
BOSS = BossComponent
BRAIN = BrainComponent
CORPSE = CorpseComponent
DIARY = DiaryComponent
ENERGY = EnergyComponent
EQUIPMENT = EquipmentComponent
INVENTORY = InventoryComponent
PLAYER = PlayerComponent
class RACES:
    MONSTER =   RaceComponent(name='monster')
    HUMAN =     RaceComponent(name='human')
    ELF =       RaceComponent(name='elf')
    KOBOLD =    RaceComponent(name='kobold')
    ORC =       RaceComponent(name='orc')
    GOBLIN =    RaceComponent(name='goblin')
class JOBS:
    # GENERIC #################################################################
    MONSTER = JobComponent(
        description="Placeholder job for monsters.",
        name='monster job',
        races=(RACES.MONSTER,)
    )
    # TIER 0 ###################################################################
    BERSERKER = JobComponent(
        description='Classic orc.',
        name='berserker',
        races=(RACES.ORC,),
        skills={},
        upkeep={Stats.HP: 1, Stats.ATK: 0, Stats.DEF: 0, Stats.MAG: 0, Stats.RES: 0, Stats.SPD: 1}
    )
    SOLDIER = JobComponent(
        description="Baby's first job.",
        name='soldier', 
        races=(RACES.HUMAN,)
    )
    THIEF = JobComponent(
        description='A stealer.',
        name='thief',
        races=(RACES.HUMAN,)
    )
    WARRIOR = JobComponent(
        description='Has access to more devastating skills.', # Not rly.
        name='warrior',
        races=(RACES.HUMAN,),
        skills={},
        upkeep={Stats.HP: 0, Stats.ATK: 0, Stats.DEF: 0, Stats.MAG: 1, Stats.RES: 0, Stats.SPD: 2}
    )
    _tier0 = {'BERSERKER': BERSERKER, 'SOLDIER': SOLDIER, 'THIEF': THIEF, 'WARRIOR': WARRIOR}
    # TIER 1 ###################################################################
    ROGUE = JobComponent(
        description='A job for seasoned fighters.',
        name='rogue',
        races=(RACES.HUMAN, RACES.GOBLIN, RACES.ELF),
        skills={SOLDIER.name: 1},
        upkeep={Stats.HP: 15, Stats.ATK: 2, Stats.DEF: 0, Stats.MAG: 0, Stats.RES: 0, Stats.SPD: 0}
    )
    _tier1 = {'ROGUE': ROGUE}
    # ALL #####################################################################
    all = {'MONSTER': MONSTER, **_tier0, **_tier1}

_actor_components = {'ACTOR': ACTOR, 'BOSS': BOSS, 'BRAIN': BRAIN, 'CORPSE': CORPSE, 'DIARY': DIARY, 'ENERGY': ENERGY, 'EQUIPMENT': EQUIPMENT, 'INVENTORY': INVENTORY, 'JOBS': JOBS, 'PLAYER': PLAYER, 'RACES': RACES}

# Item Components
CONSUMABLE = ConsumableComponent
ITEM = ItemComponent
JOB_REQ = JobReqComponent
SKILL_POOL = SkillPoolComponent
class SLOTS:
    HEAD =      SlotComponent(name='head',        key='w')
    TORSO =     SlotComponent(name='torso',       key='s')
    MAINHAND =  SlotComponent(name='mainhand',    key='q')
    OFFHAND =   SlotComponent(name='offhand',     key='a')
    FEET =      SlotComponent(name='feet',        key='d')
    ACCESSORY = SlotComponent(name='accessory',   key='e')
    all = {
        'HEAD': HEAD,
        'TORSO': TORSO,
        'MAINHAND': MAINHAND,
        'OFFHAND': OFFHAND,
        'FEET': FEET,
        'ACCESSORY': ACCESSORY

    }
    _key_to_slots = {
        'w': HEAD,
        's': TORSO,
        'q': MAINHAND,
        'a': OFFHAND,
        'd': FEET,
        'e': ACCESSORY
    }
WEARABLE = WearableComponent

_item_components = {'CONSUMABLE': CONSUMABLE, 'ITEM': ITEM, 'JOB_REQ': JOB_REQ, 'SKILL_POOL': SKILL_POOL, 'SLOTS': SLOTS, 'WEARABLE': WEARABLE}

# Other Components
FURNITURE = FurnitureComponent
NAME = NameComponent
PERSIST = PersistComponent
POSITION = PositionComponent
class RARITIES:
    AWFUL =     RarityComponent(name='awful',    rank=0)
    POOR =      RarityComponent(name='poor',     rank=1)
    COMMON =    RarityComponent(name='common',   rank=2)
    UNCOMMON =  RarityComponent(name='uncommon', rank=3)
    EPIC =      RarityComponent(name='epic',     rank=4)
    RARE =      RarityComponent(name='rare',     rank=5)
    MYTHIC =    RarityComponent(name='mythic',   rank=6)
RENDER = RenderComponent
SOUL = SoulComponent
STAIRS = StairsComponent
STATS = StatsComponent
class TILES:
    FLOOR = TileComponent(blocks_path=False,    blocks_sight=False)
    WALL =  TileComponent(blocks_path=True,     blocks_sight=True)

_other_components = {'FURNITURE': FURNITURE, 'NAME': NAME, 'PERSIST': PERSIST, 'POSITION': POSITION, 'RARITIES': RARITIES, 'RENDER': RENDER, 'SOUL': SOUL, 'STAIRS': STAIRS, 'STATS': STATS, 'TILES': TILES}

all = {**_actor_components, **_item_components, **_other_components}

# Entities should have their own instance of these components.
_fluid_components = {'BRAIN': BRAIN, 'DIARY': DIARY, 'ENERGY': ENERGY, 'EQUIPMENT': EQUIPMENT, 'INVENTORY': INVENTORY, 'JOB_REQ': JOB_REQ, 'NAME': NAME, 'POSITION': POSITION, 'RENDER': RENDER, 'SKILL_POOL': SKILL_POOL, 'SOUL': SOUL, 'STATS': STATS}