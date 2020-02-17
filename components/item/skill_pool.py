import attr

@attr.s(slots=True, auto_attribs=True)
class SkillPoolComponent:
    ' Component that holds a list of skills this item entity may bestow. '
    skill_pool: list = attr.Factory(list)