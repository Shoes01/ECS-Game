import attr
import data.archtypes as Archtypes
import data.components_master as Components
import data.jobs as Jobs
import data.rarities as Rarities
import data.skills as Skills
import data.slots as Slots
import data.stats as Stats

from data.render import ENTITY_COLORS, SPRITES # TODO: Change these too :3

# ITEMS #######################################################################

' Base components that are the same to all Items. '
ITEM = {
    Components.ITEM: True,
    Components.POSITION: True,
    Components.WEARABLE: True,
}

## MAINHAND ITEMS #############################################################

HAMMER = {**ITEM,
    Components.JOB_REQ: [Jobs.SOLDIER, Jobs.WARRIOR],
    Components.NAME: 'Hammer',
    Components.RARITY: Rarities.AWFUL,
    Components.RENDER: (')', SPRITES['eqp_sword'], ENTITY_COLORS['weapon']),
    Components.SLOT: Slots.MAINHAND,
    Components.STATS: {Stats.ATK: 7},
    Components.SKILL_POOL: [Skills.HEADBUTT, Skills.SPRINT]
}

SWORD = {**ITEM,
    Components.JOB_REQ: [Jobs.SOLDIER, Jobs.WARRIOR],
    Components.NAME: 'Sword',
    Components.RARITY: Rarities.AWFUL,
    Components.RENDER: (')', SPRITES['eqp_sword'], ENTITY_COLORS['weapon']),
    Components.SLOT: Slots.MAINHAND,
    Components.STATS: {Stats.ATK: 5},
    Components.SKILL_POOL: [Skills.LUNGE, Skills.CLEAVE]
}

_mainhands = {'HAMMER': HAMMER, 'SWORD': SWORD}

_all_items = {**_mainhands}

' The items will now bestow their slot onto their skills. '
for _, item in _all_items.items():
    for skill in item[Components.SKILL_POOL]:
        skill.slot = item[Components.SLOT]

# ACTORS ######################################################################

ACTOR = {
    Components.ACTOR: True,
    Components.ENERGY: True,
    Components.EQUIPMENT: True,
    Components.INVENTORY: True,
    Components.JOB: True,
    Components.POSITION: True,
    Components.SOUL: True
}

PLAYER = {**ACTOR,
    Components.NAME: 'Player',
    Components.PLAYER: True,
    Components.RENDER: ('@', SPRITES['player'], ENTITY_COLORS['player']),
    Components.STATS: {
        Stats.ATK: 5,
        Stats.DEF: 5,
        Stats.HP: 10,
        Stats.MAG: 5,
        Stats.RES: 5,
        Stats.SPD: 5
    }
}

ZOMBIE = {**ACTOR,
    Components.NAME: 'Zombie',
    Components.RENDER: ('Z', SPRITES['mon_zombie'], ENTITY_COLORS['mon_zombie']),
    Components.STATS: {
        Stats.ATK: 3,
        Stats.DEF: 1,
        Stats.HP:  0,
        Stats.MAG: 0,
        Stats.RES: 0,
        Stats.SPD: 0
    }
}

all = {**_all_items}
