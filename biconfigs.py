import os
import json
from codecs import open

PARSERS = {
    'json': {
        'loads': json.loads,
        'dumps': json.dumps
    },
    'pretty-json': {
        'loads': json.loads,
        'dumps': lambda dict: json.dumps(dict, indent=2, sort_keys=True)
    }
}


def read(path):
    with open(path, 'r', 'utf-8') as f:
        return f.read()


def write(path, text):
    with open(path, 'w', 'utf-8') as f:
        return f.write(text)


def BiConfigs(path, parser='pretty-json', default_value={}, debug=False):
    loads = PARSERS[parser]['loads']
    dumps = PARSERS[parser]['dumps']

    if not os.path.exists(path):
        write(path, dumps(default_value))

    def onchanged(twc):
        if debug: print('Writing')
        write(path, dumps(twc))

    twc = BiDict(loads(read(path)), onchanged=onchanged)

    return twc


def Bilateralize(value, onchanged):
    if isinstance(value, dict) and not isinstance(value, BiDict):
        return BiDict(value, onchanged)
    elif isinstance(value, list) and not isinstance(value, BiList):
        return BiList(value, onchanged)
    return value


class BiDict(dict):

    def __init__(self, _dict, onchanged):
        self._onchanged = onchanged
        self._onsubchanged = lambda x: self._onchanged(self)
        super().__init__()
        for k, v in _dict.items():
            super().__setitem__(k, Bilateralize(v, self._onsubchanged))

    def __delitem__(self, key):
        super().__delitem__(self, key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = Bilateralize(value, self._onsubchanged)
        super().__setitem__(key, value)
        self._onchanged(self)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'BiDict' object has no attribute '%s'" % key)
    def clear(self):
        super().clear()
        self._onchanged(self)

    def get_set(self, key, default=None):
        if key in self.keys():
            return self[key]
        else:
            if isinstance(default, dict) or isinstance(default, list):
                def _onchanged(x):
                    self[key] = x
                    x._onchanged = self._onsubchanged
                return Bilateralize(default, _onchanged)
            else:
                self[key] = default
                return self[key]


class BiList(list):

    def __init__(self, _list, onchanged):
        self._onchanged = onchanged
        self._onsubchanged = lambda x: self._onchanged(self)
        super().__init__()
        for v in _list:
            super().append(Bilateralize(v, self._onsubchanged))

    def __delitem__(self, key):
        super().__delitem__(self, key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = Bilateralize(value, self._onsubchanged)
        super().__setitem__(key, value)
        self._onchanged(self)

    def append(self, value):
        value = Bilateralize(value, self._onsubchanged)
        super().append(value)
        self._onchanged(self)

    def insert(self, i, value):
        value = Bilateralize(value, self._onsubchanged)
        super().insert(i, value)
        self._onchanged(self)

    def clear(self):
        super().clear()
        self._onchanged(self)

    def remove(self, i):
        super().clear(i)
        self._onchanged(self)

    def pop(self):
        super().pop(i)
        self._onchanged(self)

    def reverse(self):
        super().reverse(i)
        self._onchanged(self)