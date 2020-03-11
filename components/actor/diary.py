import attr

from typing import List

@attr.s(auto_attribs=True, slots=True)
class CooldownEntry:
    remaining: int
    skill: dict

@attr.s(auto_attribs=True, slots=True)
class MasteryEntry:
    skill: dict
    ap: int = 0

@attr.s(auto_attribs=True, slots=True)
class DiaryComponent:
    ' Component that holds information about the relationship between this entity and its skills. '
    cooldown: List[CooldownEntry] = attr.Factory(list)
    mastery: List[MasteryEntry] = attr.Factory(list)
    active: List[dict] = attr.Factory(list)