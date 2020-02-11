# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [0.11.2] - 2020-02-09
### Gameplay
#### Added
- Player race and job can be selected before starting a game.
- Jobs that the player cannot switch to are shown as ???s. However, the ???s don't remain revealed...
#### Changed
- The player's soul is now based on their race and job selections, not RNG.
#### Fixed
- Fix crash related to attempting to wear an item with no slot component or no job requirement component.
### Engine
#### Added
- Menus may now pop to a state other than Game.
- Menu choices can affect multiple processors.
#### Changed
- All game states are stored as States rather than strings.
- Moved logic out of fsm.py
- Most components and other classes have been converted to using attrs or slots.
- Item Slots, AI, Races, rarity and Jobs are all defind via Enums.
- Change all enums into classes.
- Updated readme.
#### Fixed
- Fix full message log rendering behind the game map tiles.
## [0.11.0] - 2019-10-12 - "Jobs"
This release isn't quite feature complete, but there is enough of a foundation to release something, finally!

This release introduces playable classes, called Jobs. The player starts as a Soldier, and may switch to Warrior if they have stats, or Rogue if they have the skills. They may not switch to Berserker, as they aren't the correct race. Items are now tied to Jobs, as well.

Skills may also be mastered, which at the moment is only used for Job requirements.
### Gameplay
#### Added
- Jobs have been added to the game.
- Jobs have requirements that must be met before the player may change to them.
    - Jobs may have a stat requirement.
    - Jobs may have a race requirement.
    - Jobs may have a skill requirement.
- Items may only be equipped if the player is of the correct job.
- Skills can be mastered.
    - Killing creatures grants Ability Points.
#### Known Bugs
- Entities may have negative HP and still be alive.
## [0.10.0] - 2019-07-20 - "Tiles"
This release will be a bit awkward, as part way through some combat and skill work I jumped into adding tiles to the game. So this contais a bit of both.
### Gameplay
#### Added
- Using a skill consumes part of a stat
- Implement CooldownProcessor
### Engine
#### Added
- Implement sprites
    - Support sprites being larger than font
    - Limited support for randomized floor and wall sprites
    - Experiment with some overlapping ('look' cursor)
- Implement DiscoveryProcessor
    - This is used to control in what turn a discovery is declared
- Implement camera
- Support HSV colors
- Update HUD with cooldown info
- UI displays numbers to one decimal place
- CombatProcessor now supports physical or magical damage types
#### Fixed
- Fix circular import problem by improving RenderProcessor
#### Changed
- Improve SkillProcessor error reporting
- Improve RenderProcessor readability
- Improve color readability in JSON
- Improve turn log readability by adding a whitespace before most recent turn
#### Known Bugs
- Many features from Debug Mode are broken thanks to the sprites.
## [0.9.0] - 2019-06-11 - "Souls"
This release sees the addition of Souls, and the rest of the player stats. When a monster is killed, they drop their soul (in a handy jar). The player may collect and consume the soul, giving a bonus or a penalty to certain stats. Typically, the net change will be additional stat points, but the player will have some control over where the trade offs happen. Souls are a 2x3 matrix and its values can be rolled left to right or flipped up and down before being consumed.

Because HP is one of the stats touched by the soul, the concept of maximum hp won't exist in this game. Having a huge amount of HP won't be helpful if you can't deal damage to any monsters. The next release should focus on combat and introduce some magic into the game (probably only through melee actions).
#### Added
- StatsComponent now features HP, SPD, ATK, DEF, MAG and RES
- These stats are displayed on the HUD
- Actors now generate with a SoulComponent; a 2x3 matrix giving bonuses and penalties to the aforementioned stats
- There is no max HP, as the player can choose to merge souls in a way that increases HP
- Combat now uses the stats in the following way:
- If the attacker's SPD is 5 more than the defender's, they will hit twice
- ATK is reduced by DEF, MAG is reduced by RES
- Combattans will now counter attack
- More monsters are added to display SoulComponent varieties
- Like-monsters are now all identical; equipment and souls don't affect stats for them
#### Fixed
- Fixed a bug with viewing the log
#### Changed
- Create a CharacterSheet to view stats, accessed by 'c'
- Better organize InputProcessor
- ActionProcessor has been removed; all actions go directly to their processors
- ModifierComponent removed; items will use the StatComponent to the same effect
## [0.8.2] - 2019-05-21 - "Queued Processors"
This release should introduce nothing new, gameplay wise... except maybe bugs.
#### Added
- Most processors use queues instead of looking for entities to process.
## [0.8.1] - 2019-05-01 - "Combat Update"
This update introduces an active skill component for items.
#### Added
- Active skills cost energy based on their JSON definition
- Active skills use colors based on their JSON definition
- Active skills use flags in their JSON definition
- The following flags are supported: unblockable damage, blockable damage (cannot hit walls), movement, and "require space" (if a move skill uses this, the unit may be running; without it, they may be leaping)
- Active skills use the message log to display information about the item and skill
#### Changed
- CombatProcessor now supports hitting many units in one action
- A few more items have been added to test the active skills
## [0.7.0] - 2019-04-21
This update mostly contains improvements to the engine.
#### Added
- Mouse over information is provided
- Movement can be done with the mouse left click (no pathfinding yet)
- Implemented a GameWorld() object to hold what used to be the game entity
- Events are filled and emptied, rather than added and removed
- State is tracked as a stack
- A look function has been added
- Improve CustomWorld(): can now fetch entities containing arbitrary components from a specific location.
#### Fixes
- Entering the debug menu no longer opens the drop menu
#### Changed
- Update Readme
## [0.6.0] - 2019-04-19 - "Equipment Update"
This update adds a rudimentary loot system.
#### Added
- Create item slots
- UI shows what items are equipped
- Chests spawn, containing loot
- Moved entity/component data to JSON
- Give equipment to monsters based on: dungeon floor, item rarity, monster rarity
- New messages: walking on an item, or a stack of items
#### Fixed
- Fixed bug related to dropping items
- Fixed bug related to message log
#### Changed
- Updated readme
## [0.5.0] - 2019-04-15 - "Depth Update"
This update added stairs that lead to additional floors.
#### Added
- Added a "final floor" that also spawns a boss monster. Currently that is floor 2
- Tiles containing more than one item, or an entity and an item, are highlighted
- Pressing 'm' shows the message log, and is scrollable
#### Changed
- Menus are now closed after loading a game
- HP is set to 500... made finding the boss monster a little easier!
## [0.4.0] - 2019-04-13 - "Beauty Update"
This update focused on making things look a little better.
#### Changed
- Borders no longer use place holder glyphs
- Menu popup has an improved front-end and back-end
- Message log should now have a message for every action
- Colors are now managed from one file, and are using a theme
## [0.3.0] - 2019-04-09
Items can now be equipped, consumed, or dropped! There are keys for accessing each action ('w', 'e' and 'd' respectively), or open the inventory ('i') and choose an item to see the action submenu.
## [0.1.0] - 2019-04-06
This is the first release. The game contains only a small number of systems, but the player can run around and slay zombies until they die!