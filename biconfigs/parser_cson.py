
from .exceptions import DependenciesMissingError
from .parsers import PARSERS

try:
    import cson
except ImportError: # pragma: no cover
    raise DependenciesMissingError('Can not import dependency "cson", did you install it?')
else:
    if 'cson' not in PARSERS:
        PARSERS['cson'] = {
            'loads': cson.loads,
            'dumps': lambda x: cson.dumps(x, indent=2)
        }
