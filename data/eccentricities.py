import attr

@attr.s(auto_attribs=True, slots=True)
class Eccentricity:
    ' The eccentricity of an entity determines the variation of its base stats. '
    eccentricity: int
    name: str

DECAYED =       Eccentricity(eccentricity=-2, name="decayed")
HYPOBOLIC =     Eccentricity(eccentricity=-1, name="hypobolic")
CIRCULAR =      Eccentricity(eccentricity= 0, name="circular")
ELLIPTIC =      Eccentricity(eccentricity= 1, name="elliptic")
PARABOLIC =     Eccentricity(eccentricity= 3, name="parabolic")
SUPERBOLIC =    Eccentricity(eccentricity= 5, name="superbolic")
HYPERBOLIC =    Eccentricity(eccentricity= 9, name="hyperbolic")

all = {
    'DECAYED': DECAYED,
    'HYPOBOLIC': HYPOBOLIC,
    'CIRCULAR': CIRCULAR,
    'ELLIPTIC': ELLIPTIC,
    'PARABOLIC': PARABOLIC,
    'SUPERBOLIC': SUPERBOLIC,
    'HYPERBOLIC': HYPERBOLIC
}