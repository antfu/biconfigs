import json

PARSERS = {
    'json': {
        'loads': json.loads,
        'dumps': json.dumps
    },
    'pretty-json': {
        'loads': json.loads,
        'dumps': lambda d: json.dumps(d, indent=2, sort_keys=True)
    },
    'none': {
        'loads': lambda x: x,
        'dumps': lambda y: y
    }
}

EXTENSION_TO_PARSER = {
    'json': 'pretty-json',
}
