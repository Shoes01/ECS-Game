import attr

@attr.s(slots=True)
class EnergyComponent:
    ' Component that provides entities with energy used for taking turns. '
    energy : int = attr.ib(default=1)
    