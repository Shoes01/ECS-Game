import attr

@attr.s(auto_attribs=True, slots=True)
class EnergyComponent:
    ' Component that provides entities with energy used for taking turns. '
    energy : int = 1
    