import attr

@attr.s(auto_attribs=True, slots=True)
class SkillDirectoryComponent:
    ' Component that holds a list of skills the entity has touched. '
    skill_directory: list = attr.Factory(list)