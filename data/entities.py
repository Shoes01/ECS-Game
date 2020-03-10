import attr
import data.components_master as Components
import data.jobs as Jobs
import data.rarities as Rarities
import data.render as Render
import data.skills as Skills
import data.slots as Slots
import data.souls as Souls
import data.stats as Stats

# ITEMS #######################################################################

' Base components that are the same to all Items. '
ITEM = {
    Components.ITEM: True,
    Components.POSITION: True,
    Components.WEARABLE: True,
}

HAMMER = {**ITEM,
    Components.JOB_REQ: [Jobs.SOLDIER, Jobs.WARRIOR],
    Components.NAME: 'Hammer',
    Components.RARITY: Rarities.AWFUL,
    Components.RENDER: Render.HAMMER,
    Components.SLOT: Slots.MAINHAND,
    Components.STATS: {Stats.ATK: 7},
    Components.SKILL_POOL: [Skills.HEADBUTT, Skills.SPRINT]
}

SWORD = {**ITEM,
    Components.JOB_REQ: [Jobs.SOLDIER, Jobs.WARRIOR],
    Components.NAME: 'Sword',
    Components.RARITY: Rarities.AWFUL,
    Components.RENDER: Render.SWORD,
    Components.SLOT: Slots.MAINHAND,
    Components.STATS: {Stats.ATK: 5},
    Components.SKILL_POOL: [Skills.LUNGE, Skills.CLEAVE]
}

_all_items = {'HAMMER': HAMMER, 'SWORD': SWORD}

' The items will now bestow their slot onto their skills. '
for _, item in _all_items.items():
    for skill in item[Components.SKILL_POOL]:
        skill.slot = item[Components.SLOT]

# ACTORS ######################################################################

' Base components that are the same to all Actors. '
ACTOR = {
    Components.ACTOR: True,
    Components.ENERGY: True,
    Components.EQUIPMENT: True,
    Components.INVENTORY: True,
    Components.JOB: True,
    Components.POSITION: True,
}

PLAYER = {**ACTOR,
    Components.JOB: Jobs.SOLDIER,
    Components.NAME: 'Player',
    Components.PLAYER: True,
    Components.RENDER: Render.PLAYER,
    Components.SOUL: Souls.PLAYER,
    Components.STATS: Stats.PLAYER
}

ZOMBIE = {**ACTOR,
    Components.NAME: 'Zombie',
    Components.RENDER: Render.ZOMBIE,
    Components.SOUL: Souls.ZOMBIE,
    Components.STATS: Stats.ZOMBIE
}

_all_actors = {'PLAYER': PLAYER, 'ZOMBIE': ZOMBIE}

all = {**_all_items, **_all_actors}
