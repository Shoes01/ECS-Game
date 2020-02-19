import attr

@attr.s(auto_attribs=True, slots=True)
class SkillPoolComponent:
    ' Component that holds a list of skills this item entity may bestow. '
    skill_pool: list = attr.Factory(list)