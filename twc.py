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


def GetTwoWayConfigs(path, parser='pretty-json'):
    loads = PARSERS[parser]['loads']
    dumps = PARSERS[parser]['dumps']

    def onchanged(twc):
        write(path, dumps(twc))

    twc = TwoWayDict(loads(read(path)), onchanged=onchanged)

    return twc


def TwoWaylize(value, onchanged):
    if isinstance(value, dict) and not isinstance(value, TwoWayDict):
        return TwoWayDict(value, onchanged)
    elif isinstance(value, list) and not isinstance(value, TwoWayList):
        return TwoWayList(value, onchanged)
    return value


class TwoWayDict(dict):

    def __init__(self, _dict, onchanged):
        self._onchanged = onchanged
        super().__init__()
        if _dict:
            for k, v in _dict.items():
                self[k] = TwoWaylize(v, onchanged)

    def __delitem__(self, key):
        super().__delitem__(self, key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = TwoWaylize(value, lambda x: self._onchanged(self))
        super().__setitem__(key, value)
        self._onchanged(self)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'TwoWayDict' object has no attribute '%s'" % key)


class TwoWayList(list):

    def __init__(self, _list, onchanged):
        self._onchanged = onchanged
        super().__init__()
        for v in _list:
            super().append(TwoWaylize(v, onchanged))

    def __delitem__(self, key):
        super().__delitem__(self, key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = TwoWaylize(value, lambda x: self._onchanged(self))
        super().__setitem__(key, value)
        self._onchanged(self)

    def append(self, value):
        value = TwoWaylize(value, lambda x: self._onchanged(self))
        super().append(value)
        self._onchanged(self)

    def insert(self, i, value):
        value = TwoWaylize(value, lambda x: self._onchanged(self))
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
