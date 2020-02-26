import attr

from _data import Skill
from typing import List

@attr.s(auto_attribs=True, slots=True)
class CooldownEntry:
    remaining: int
    skill: Skill

@attr.s(auto_attribs=True, slots=True)
class MasteryEntry:
    ap: int = 0
    skill: Skill

@attr.s(auto_attribs=True, slots=True)
class DiaryComponent:
    ' Component that holds information about the relationship between this entity and its skills. '
    cooldown: List[CooldownEntry]
    mastery: List[MasteryEntry]
    active: List[Skill]