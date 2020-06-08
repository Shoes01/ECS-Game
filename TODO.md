## PROGRESSION -- Implement a sense of progression
First floor should have monsters that drop rarity 1 loot, and have souls that total +1
Second floor: rarity 2, souls +2
etc.

## MISC -- Improve monster pathing
Monsters should avoid pathing into a tile that already contains a monster (and thus attacking it)
Monsters should favor approaching the player orthogonally

## MISC -- Improve input processor
Move each input scheme into its own def
Eventually move it into its own class, and have the FSM assign the proper class, via queue
> I could perhaps add the event to the queue in the GameStateAMachine() class by itself

## MISC -- Dev Environment
Look into GitLens, Flake8, mypy, isort, black

## SOULS -- Player class determines the order of stats in the soul
Have the "titles" dict be stored in the SoulComponent, or the PlayerComponent, or the StatComponent or something.
One class might have the soul [[HP, ATK, MAG], whereas another might have the soul [[HP, SPD, RES],
                              [SPD, DEF, RES]]                                     [ATK, DEF, MAG]]
Some classes might have hybrid stats??? 

## OPTIONS -- Have a dict with options that can be set in the main menu
First options could be font, and sprite size.

## COMBAT
[x] Bump Attack: Always physical.
[ ] "Use" weapon: Wands zap (magical), bows fire (ranged), etc
[ ] "Skill" weapon: Dependent on the skill.
[ ] Add melee item that deals magic damage
> [ ] Will probably need to inform the player somehow of the damage type of a monster.
[ ] FE:H Color triangle of enemy power
> [ ] R > G > B > R, like in FE:H. Monsters don't get assigned this randomly. 
[ ] Enemy UI Dichotomies :: The player could toggle the UI display... swap between the three... 
> [ ] Magic/Physical -- not necessary
> [ ] High SPD, medium SPD, low SPD -- would be nice to have ^ and ˇ
> [ ] Color addinity: RGB
DEPRECATED: Enemies no longer have a random stat allocation, so the above UI considerations may be obsolete.
[?] Create item that is just a jar containing an HP-soul named Faerie

## JOBS -- v0.11.x
[x] Implement Races, Jobs, and Skills
    [-] Races
        - Orc
        - Goblin
        - Human
        - Vermin
        - Demon
    [-] Jobs (: items)
        - Zombie: Torn Cloth
        - Rat: 
        - berserker: Axe
        - Thief: Dagger
        - Soldier: Sword, Shield
    [-] Skills
        - Axe: Hack
        - Sword: Slash
        - Shield: Block
[x] Implement Ability Points
    [x] Skills have a max AP
    [x] Using a skill grants it AP, say 10
    [x] Getting kills grants AP, say 2
    [x] When a skill has max AP, it is Mastered
[ ] Implement Skill Selection
    [ ] Pressing ctrl+Q will bring up the weapon skill, the mastered skills, and skills that have at least one AP
    [x] Display AP/maxAP
[x] Job selection is based on Race
[x] Item equip is based on Job
[x] Need a way for the player to pick a race/job at the beginning of the game.
[x] Player may switch between jobs
[x] At the moment, items may only have _one_ job_req. I would like some items to fit in many jobs, but have different skills.
[ ] Need a way to "inspect" items, to know what skills they have, and the jobs those need. This could be an extension of the inventory, an added (i) where consume/drop/etc are located.
[ ] Create a process/function that closes out the game. This process/function is what will set "world.running" to False.
ISSUE: What is in branch "job"? Is it all redundant code? \\I've archived it just in case...

#### Bugfixes -- v0.11.(x-1)
[ ] Look into fixing debug mode, or imporiving it
[ ] Improve message log process

BUG: I sometimes don't die when at negative HP (does this happen to others as well, triggering the "corpse being killed" message thing?)
BUG: Shield seems to not be a valid item, yet Long Sword is and has no skill
>>> Only true when both of these items are equipped. Saved game shows this.
>>>>>> Perhaps using the new data will fix this problem
BUG: Sprint skill doesn't teleport the player -- or it does, but it still takes "too long". The player moves two tiles, but so do the monsters ...
BUG: The message log doesn't clear when starting a new game after death.
BUG: "There are two items here" triggers when trying to move to a square, even if moving there failed.

#### Undecided -- v0.11.4
[ ] Go through and properly document my stuff via pythonic convention, with a Title and a Body.
```py
class DoNothing:
    """Do nothing.

    This class does nothing."""
```

#### Mastered Skilled -- v0.11.3 -- "mastered-skills"
[ ] Revisit using typing.NamedTuples and subclassing it. I could use this to make "hashable dicts". (using `._asdict()`)
[ ] Make a "meta"processor for Skills, much like I have done for Render. \\Maybe formalize this more too...
[ ] Commit one last diff updating the change log. This commit will be tagged v0.11.3
[?] Jobs and Races could be pulled out into JSONs. \\This doesn't actually affect the game ... there is no point in doing this yet.
ISSUE: Commit c3e51d5 reads "not" instead of "now", totally changing what happens there \\Possible, but I need to know how to use vim or something
ISSUE: New classes were added for Slots, AI, etc. Ensure that there are no bugs regarding this. 
ISSUE: Job selection menu: If a condition is suddenly no longer valid, then the text goes back to ???.
ISSUE: I should make choices about input now. For example, movement and other player-map interactions have no modifiers. user-player interactions should all have the same modifier. SHIFT or CTRL or ALT. Intercations types are player-map, user-player, user-map, user-game, ???.
[?] There are issues with attrs and my linter ... can I figure this out?
[x] Spawn a sword in the first room the player starts.
[ ] Skills should be equippable, inedpedantly of item
`Expectation` 
Player may press CTRL+Q to open a menu of their Q-skills. 
    The menu displays Bestowed Skills, Mastered Skills and Unmastered Skills.
        While all skills begin unmastered, only those that have been seen by the player are displayed on this list.
        The rest could be ???s.
Player may then choose to equip a mastered Q-skill, or to equip a bestowed Q-skill.
Player may also choose to unequip the Q-skill.
Player is prompted to equip the skill of the first item they pick up. \\Maybe
If the player attemps to equip an unmastered skill, prompt the player to swap items.
`Implementation details`
The Q-skill Menu is a menu with the following options:
    Equip
     Bestowed Skills
     Mastered Skills
     Unmastered Skills \\Greyed out, and unable to be picked: prompt the player to switch items.
     Unknown Skills \\Listed as ???s, and unable to be picked.
    Unequip
    Cancel

__Current Commit Batch__
[x] Make skills equippable. \\I think this technically works... but I am inbetween changing a lot of things related to skills and items... so...
 [x] When choosing something from the skill menu, activate the skill. And deactivate the currently active skill.
  [x] Skills need to be de/activated when wearing, removing items and when switching jobs.
  [x] Remove all mention of items when using skills. Except for error messages? That will be interesting. But I think I have a table for that.
[x] Replace `SkillComponent` by `class Skills` that contains an entry for each skill, allowing code to be written as `Skills.LUNGE`.
 [x] The class `Skills` needs to import its slot-property from the items in `equipment.json`.
  [x] Each time an item-entity is created, it will assign a slot to the skills found in its skill_pool. \\This can lead to difficult bugs
[x] Replace `SkillComponentDirectory` by `DiaryComponent`
 [x] Check that cooldowns, masteries and activations are done via `DiaryComponent`
  [x] Time to actually make skill_menu work ... \\Skill-menu is crashing, now that I've messed around with the jsons.
   [x] Remove json.equipement, and get the game going again. \\`create_entity` is built with JSONs on mind. Hmm. This will be changed ... almost entirely...
   [x] Pulled a bunch of stuff out of _data.py into its own data/file.py
 [x] Figure out how to give the player a mastered skill from the get-go \\the heal skill
 [x] Replace references to `SkillComponentDirectory`
 [x] Update various processors (`SkillMenuProcessor`, `CooldownProcessor`, `SkillProcessor`, etc) to use the new component.
 [x] Remove the SkillComponent ...
 [x] Character Sheet needs to dispaly Skills, because items have been decoupled.
[x] Update error messages to no longer mention items when thinking about skills.
[x] Implement damage types
[x] Some data_tables in game.py may now be obsolete. \\Skill or item related ones
[x] Removed all tables from game.py. Hopefully this don't break anything lol.
[x] Check that the player healing skill works.
[x] Shift+W opens the skill menu, and the wearable menu. This is a conflict
[ ] Add corpse info to the entity's render component? (this may be cool, or it may be useless boilerplate.)
[ ] Take a look at how jobs work, and compare to how skills and items work \\Why? I forget.
[-] Move all use of pseudo decimals to the display
[ ] Pressing 'esc' at the race/job picker menus should send back to main menu
[ ] Now that I have all components in one handy file, I should move that file into /components, and invoke only this when I work
[ ] Skill processor uses a variable called "number" which represetns the integer used in the skill definition. Replace this with a more descriptive variable name to improve legibility.
[!!!] Give skills a unique targeting sprite that can be used when casting a spell
 [ ] Use the same sprite (but smaller?) on the QWEASD menu
[ ] Backup json items need to have their slot changed.


__Current Commit__
Make a small sprite sheet ... can this be used concurrently with text?
 > I have some code to allow the skill sprite to appear in the QWEASD menu
 ISSUE: error message needs to be fixed
 ISSUE: cooldown colors arent right. i dont think the skill clears



__Changelog__
## [0.11.3] - 2020-MM-DD - "Mastered Skills Update"
### Project
#### Added
- Added a changelog.
- Rudimentary skill menu, for equipping skills. \\Doesn't work yet.
### Gameplay
#### Added
- A sword spawns with the player.
- Player starts with a healing skill.
#### Changed
- Improved error messages in SkillProcessor.
- The skill used in combat gains double the ability points.
### UI
#### Removed
- The letter-box skill menu on the bottom left no longer displays the item granting the skill (items and skills have been decoupled)
### Internal
#### Added
- Add a check to ensure items are created with skills that exist.
- Add a check to ensure skills don't share a first letter (prevents a conflict in the Skill Menu).
- Add a helper function to create skills. This will allow the player to be given skills without using an item.
#### Changed
- Main Menu logic code has been moved from input processor to event processor.
- Improved readability of InputProcessor.
- Introduce DiaryComponent that tracks cooldown, mastery and active-state of skills.
- Skills inherit their slot information from their parent item.
- Skills and Items have largely been decoupled.
#### Fixed
- A few bugs related to switching from a dict of Jobs to a class of Jobs.



################# Q for the discord

```py
# components.py ###############################################################
from components.position import PositionComponent
from components.render import RenderComponent
from components.wearable import WearableComponent

POSITION = PositionComponent
RENDER = RenderComponent
WEARABLE = WearableComponent

all = {'POSITION': POSITION, 'RENDER': RENDER, 'WEARABLE': WEARABLE}

# entities.py #################################################################
import components as Components

ITEM = {
    Components.POSITION: True,
    Components.WEARABLE: True
}

MONSTER = {
    Components.POSITION: True,
}

all = {'ITEM': ITEM, 'MONSTER': MONSTER}

# equipment.py ################################################################
import colors as Colors
import components as Components
import entities as Entities

HAMMER = {**Entities.ITEM,
    Components.RENDER: (')', Colors.BLUE)
}

SWORD = {**Entities.ITEM,
    Components.RENDER: (')', Colors.RED)
}

# somefile.py #################################################################
import equipment as Equipment
from game import create_entity

hammer_entity = create_entity(Equipment.HAMMER)

# game.py #####################################################################
def create_entity(data):
    ent = new_entity()
    for key, value in data.items():
        component = key(value) # For example, key could be PositionComponent and value would be True, so key(value) would be PositionComponent(True)
        attach_compinent(ent, component)
    
    return ent

### QUESTIONS #################################################################
# I am faily certain this fails, because using a function is not hashable, and thus not usable as the key of a dict. What is the work around here?
# Does the create_entity entity line 3 "component = key(value)" work the way I expect? 
```