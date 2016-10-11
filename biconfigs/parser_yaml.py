
from .exceptions import DependenciesMissingError
from .parsers import PARSERS
import json

try:
    import yaml
except ImportError: # pragma: no cover
    raise DependenciesMissingError('Can not import dependency "PyYAML", did you install it?')
else:
    if 'yaml' not in PARSERS:
        PARSERS['yaml'] = {
            'loads': yaml.load,
            'dumps': lambda x: yaml.dump(x.represent())
        }
