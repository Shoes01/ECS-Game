# MONSTER OUTLINE
Monsters will have a race.
Monsters will have a soul.
Monsters will have a class.

## MECHANIC ONE -- RACE
The race of a monster determines its baseline stats.

`Examples`
Rat: 1
Kobold: 5
Goblin: 9
Orc: 15

## MECHANIC TWO -- SOUL ECCENTRICITY
The race of a monstter determines the eccentricity of a soul.
A "circular" soul has eccentricity 0; all value are the same.
A "hyperbolic" soul is very eccentric; values may be wildly different.

`Examples`
Rat: 0 (boring)
Kobold: 10 (quite eccentric)
Goblin: 2
Orc: 4

## MECHANIC THREE -- SOUL RARITY
The soul of a monster determines its net additional stats above baseline.
> Eccentric souls may have negative values for certain stats, but the sum total of the changes will be the same for souls of equal rarity.

`Examples`
Zombie: -2
Husk: -1
(no name): 0
Initiate: +1
Adventurer: +3
Hero: +5
Champion: +9

Thus a Goblin Zombie will have base stats +9, with a net -2 of additional stats, spread based on eccentricity.

## MECHANIC FOUR -- CLASS
Given the stats of a monster, a class can be inferred and items can be given based on that.
Classes are determined by the stats. Classes can have tiers, based on the total stats. (stat totals are just race + soul rarity)
Item layout is determined by class.
Item quality is based on stat total

`Example` -- simplified
__Physical Melee__ Has highest ATK and HP
Grunt: 0 - 20 (total stat points)
Soldier: 21 - 50
Crusader: 51 - 100
Kingslayer: 101 - 200
Godslayer: 201 - 500

Mainhand: Sword
Offhand: Shield
Torso: Chainmail
Head: Great Helm
Feet: Greaves
Accessory: Ring of Resistance

### RESULT 
Monsters are simply constructed. 
> Pick `Race`.
> Generate `Soul`, with `Eccentricity`.
> `Stats` have now been determined.
>> `Class` is based on the stats.
>>> `Items` is based on class.
>>> `Name` is based on class and race.

### MONSTER GEN
A map could have a difficulty number, the total set of stats
Each room gets some stat points
Then the stat points are used to gen monsters until it's all used up?