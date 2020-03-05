import attr
import data.jobs as Jobs
import data.rarities as Rarities
import data.skills as Skills
import data.slots as Slots
import data.stats as Stats

from data.rarities import Rarity
from data.render import Render, SPRITES

@attr.s(auto_attrib=True, slots=True)
class Item:
    job_requirement: list
    name: str
    rarity: Rarity
    render: dict
    slot: str
    stats: dict
    wearable: bool
    skill: list
    archtype: 'item'
    # The 'item' archtype bestows a lot of blank components: Item, Position.

################
### MAINHAND ###
################

HAMMER = Item(
    job_requirement=[Jobs.SOLDIER, Jobs.WARRIOR]
    name='Hammer'
    rarity=Rarities.AWFUL
    render=Render(
        char=')',
        codepoint=SPRITES['eqp_sword'],
        color_fg='weapon'
    )
    slot=Slots.MAINHAND
    stats={Stats.ATK: 5}
    wearable=True
    skill=[Skills.HEADBUTT, Skills.SPRINT]
)

SWORD = Item(
    job_requirement=[Jobs.SOLDIER, Jobs.WARRIOR]
    name='Sword'
    rarity=Rarities.AWFUL
    render=Render(
        char=')',
        codepoint=SPRITES['eqp_sword'],
        color_fg='weapon'
    )
    slot=Slots.MAINHAND
    stats={Stats.ATK: 5}
    wearable=True
    skill=[Skills.LUNGE, Skills.CLEAVE]
)

_mainhands = {'HAMMER': HAMMER, 'SWORD': SWORD}

###############
### OFFHAND ###
###############

_offhands = {}

all = {**_mainhands, **_offhands}