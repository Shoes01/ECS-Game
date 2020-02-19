import attr

@attr.s(auto_attribs=True, slots=True)
class NameComponent:
    ' Component that holds the name of the entity. '
    name: str
    original_name: str = ""

    def __attrs_post_init__(self):
        # Hold the private variable for later access.
        self.original_name = self.name