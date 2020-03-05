import attr

from data.skills import Skill
from typing import List

@attr.s(auto_attribs=True, slots=True)
class CooldownEntry:
    remaining: int
    skill: Skill

@attr.s(auto_attribs=True, slots=True)
class MasteryEntry:
    skill: Skill
    ap: int = 0

@attr.s(auto_attribs=True, slots=True)
class DiaryComponent:
    ' Component that holds information about the relationship between this entity and its skills. '
    cooldown: List[CooldownEntry] = attr.Factory(list)
    mastery: List[MasteryEntry] = attr.Factory(list)
    active: List[Skill] = attr.Factory(list)