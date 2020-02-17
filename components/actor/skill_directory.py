import attr

@attr.s(slots=True, auto_attribs=True)
class SkillDirectoryComponent:
    ' Component that holds a list of skills the entity has touched. '
    skills: list = attr.Factory(list)