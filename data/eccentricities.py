from collections import namedtuple

Eccentricity = namedtuple('Eccentricity', 'name rank')

DECAYED =       Eccentricity(name='decayed',    rank=0)
HYPOBOLIC =     Eccentricity(name='hypobolic',  rank=1)
CIRCULAR =      Eccentricity(name='circular',   rank=2)
ELLIPTIC =      Eccentricity(name='elliptic',   rank=3)
PARABOLIC =     Eccentricity(name='parabolic',  rank=4)
SUPERBOLIC =    Eccentricity(name='superbolic', rank=5)
HYPERBOLIC =    Eccentricity(name='hyperbolic', rank=6)

all = {
    'DECAYED': DECAYED,
    'HYPOBOLIC': HYPOBOLIC,
    'CIRCULAR': CIRCULAR,
    'ELLIPTIC': ELLIPTIC,
    'PARABOLIC': PARABOLIC,
    'SUPERBOLIC': SUPERBOLIC,
    'HYPERBOLIC': HYPERBOLIC
}