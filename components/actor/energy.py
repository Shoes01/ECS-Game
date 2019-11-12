import attr

@attr.s(slots=True, auto_attribs=True)
class EnergyComponent:
    ' Component that provides entities with energy used for taking turns. '
    energy : int = 1
    