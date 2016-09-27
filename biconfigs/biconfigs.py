from __future__ import print_function
import os
import json
import random
import string
from codecs import open

__version__ = '0.0.1'
__randstr_chars = string.ascii_letters + string.digits
__memory_storage = {}


def randstr(length=10):
    return ''.join(random.sample(__randstr_chars, length))

def file_read(path):
    with open(path, 'r', 'utf-8') as f:
        return f.read()

def file_write(path, text):
    with open(path, 'w', 'utf-8') as f:
        return f.write(text)

def memory_write(key, data):
     __memory_storage[key] = data

PARSERS = {
    'json': {
        'loads': json.loads,
        'dumps': json.dumps
    },
    'pretty-json': {
        'loads': json.loads,
        'dumps': lambda dict: json.dumps(dict, indent=2, sort_keys=True)
    },
    'none': {
        'loads': lambda x: x,
        'dumps': lambda y: y
    }
}

STORAGES = {
    'file': {
        'read': file_read,
        'write': file_write
    },
    'memory': {
        'read': lambda x: __memory_storage[x],
        'write': memory_write
    }
}

def Bilateralize(value, onchanged):
    if isinstance(value, dict) and not isinstance(value, BiDict):
        return BiDict(value, onchanged)
    elif isinstance(value, list) and not isinstance(value, BiList):
        return BiList(value, onchanged)
    return value


class BiDict(dict):

    def __init__(self, _dict, onchanged=None):
        self._onchanged = onchanged or (lambda x: None)
        self._onsubchanged = lambda x: self._onchanged(self)
        super(BiDict, self).__init__()
        for k, v in _dict.items():
            super(BiDict, self).__setitem__(k, Bilateralize(v, self._onsubchanged))

    def __delitem__(self, key):
        super(BiDict, self).__delitem__(key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = Bilateralize(value, self._onsubchanged)
        super(BiDict, self).__setitem__(key, value)
        self._onchanged(self)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'BiDict' object has no attribute '%s'" % key)

    def clear(self):
        super(BiDict, self).clear()
        self._onchanged(self)

    def get_set(self, key, default=None):
        if key in self.keys():
            return self[key]
        else:
            if isinstance(default, dict) or isinstance(default, list):
                def _onchanged(x):
                    self[key] = x
                    x._onchanged = self._onsubchanged
                value = Bilateralize(default, _onchanged)
                self.setdefault(key, value)
                return value
            else:
                self[key] = default
                return self[key]


class BiList(list):

    def __init__(self, _list, onchanged=None):
        self._onchanged = onchanged or (lambda x: None)
        self._onsubchanged = lambda x: self._onchanged(self)
        super(BiList, self).__init__()
        for v in _list:
            super(BiList, self).append(Bilateralize(v, self._onsubchanged))

    def __delitem__(self, key):
        super(BiList, self).__delitem__(key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = Bilateralize(value, self._onsubchanged)
        super(BiList, self).__setitem__(key, value)
        self._onchanged(self)

    def append(self, value):
        value = Bilateralize(value, self._onsubchanged)
        super(BiList, self).append(value)
        self._onchanged(self)

    def insert(self, i, value):
        value = Bilateralize(value, self._onsubchanged)
        super(BiList, self).insert(i, value)
        self._onchanged(self)

    def clear(self):
        del(self[:])

    def remove(self, i):
        super(BiList, self).remove(i)
        self._onchanged(self)

    def pop(self):
        super(BiList, self).pop()
        self._onchanged(self)

    def reverse(self):
        super(BiList, self).reverse()
        self._onchanged(self)


class BiConfigs(BiDict):
    def __init__(self, path=None, parser=None, default_value={}, storage=None, onchanged=None, debug=False):
        self.storage = storage or 'file'
        self.parser = parser or 'pretty-json'
        self.path = path
        self.onchanged = onchanged or (lambda x: None)

        if not path or path == '::memory::':
            self.parser = 'none'
            self.storage = 'memory'
            self.path = randstr(20)

        self.loads = PARSERS[self.parser]['loads']
        self.dumps = PARSERS[self.parser]['dumps']
        self.read = STORAGES[self.storage]['read']
        self.write = STORAGES[self.storage]['write']

        if self.storage == 'file' and not os.path.exists(self.path):
            self.write(self.path, self.dumps(default_value))

        if self.storage == 'memory':
            self.write(self.path, default_value)

        super(BiConfigs,self).__init__(self.loads(self.read(self.path)),
                                       onchanged=self._biconfig_onchanged)

    def _biconfig_onchanged(self, obj):
        if self.onchanged:
            self.onchanged(obj)
        self.write(self.path, self.dumps(obj))
