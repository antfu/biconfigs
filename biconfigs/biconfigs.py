from __future__ import print_function
import os
import json
import random
import string
from threading import Thread
from codecs import open
from .exceptions import *


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
    if isinstance(value, dict) and not isinstance(value, Bidict):
        return Bidict(value, onchanged)
    elif isinstance(value, list) and not isinstance(value, Bilist):
        return Bilist(value, onchanged)
    return value

class Bidict(dict):

    def __init__(self, _dict, onchanged=None):
        self._onchanged = onchanged or (lambda x: None)
        self._onsubchanged = lambda x: self._onchanged(self)
        self.default_value = {}
        super(Bidict, self).__init__()
        for k, v in _dict.items():
            super(Bidict, self).__setitem__(k, Bilateralize(v, self._onsubchanged))

    def __getitem__(self, key):
        try:
            return super(Bidict, self).__getitem__(key)
        except KeyError:
            if key in self.default_value.keys():
                return self.default_value[key]
            else:
                raise

    def get(self, key, default):
        return super(Bidict, self).get(key, self.default_value.get(key, default))

    def __delitem__(self, key):
        super(Bidict, self).__delitem__(key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = Bilateralize(value, self._onsubchanged)
        old_value = None
        old_value = super(Bidict, self).get(key, None)
        if old_value == None or not old_value == value:
            super(Bidict, self).__setitem__(key, value)
            self._onchanged(self)

    def __enter__(self):
        self._onchanged_back = self._onchanged
        self._onchanged = lambda x: None
        return self

    def __exit__(self, *args):
        self._onchanged = self._onchanged_back
        del(self._onchanged_back)
        self._onchanged(self)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'Bidict' object has no attribute '%s'" % key)

    def clear(self):
        self.default_value = {}
        super(Bidict, self).clear()
        self._onchanged(self)

    def get_set(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            if isinstance(default, dict) or isinstance(default, list):
                def _onchanged(x):
                    self[key] = x
                    x._onchanged = self._onsubchanged
                value = Bilateralize(default, _onchanged)
                self.default_value[key] = value
                return value
            else:
                self[key] = default
                return self[key]


class Bilist(list):

    def __init__(self, _list, onchanged=None):
        self._onchanged = onchanged or (lambda x: None)
        self._onsubchanged = lambda x: self._onchanged(self)
        super(Bilist, self).__init__()
        for v in _list:
            super(Bilist, self).append(Bilateralize(v, self._onsubchanged))

    def __delitem__(self, key):
        super(Bilist, self).__delitem__(key)
        self._onchanged(self)

    def __setitem__(self, key, value):
        value = Bilateralize(value, self._onsubchanged)
        try:
            old_value = self[key]
        except IndexError:
            old_value = None
        if old_value == None or not old_value == value:
            super(Bilist, self).__setitem__(key, value)
            self._onchanged(self)

    def __enter__(self):
        self._onchanged_back = self._onchanged
        self._onchanged = lambda x: None
        return self

    def __exit__(self, *args):
        self._onchanged = self._onchanged_back
        del(self._onchanged_back)
        self._onchanged(self)

    def append(self, value):
        value = Bilateralize(value, self._onsubchanged)
        super(Bilist, self).append(value)
        self._onchanged(self)

    def insert(self, i, value):
        value = Bilateralize(value, self._onsubchanged)
        super(Bilist, self).insert(i, value)
        self._onchanged(self)

    def clear(self):
        super(Bilist, self).__delitem__(slice(None, None, None))
        self._onchanged(self)

    def remove(self, i):
        super(Bilist, self).remove(i)
        self._onchanged(self)

    def pop(self):
        super(Bilist, self).pop()
        self._onchanged(self)

    def reverse(self):
        super(Bilist, self).reverse()
        self._onchanged(self)


class Biconfigs(Bidict):
    def __init__(self,
                path=None,
                default_value={},
                parser=None,
                storage=None,
                async_write=True,
                onchanged=None,
                before_save=None):
        '''Constructs a <Biconfigs> instance

        :param path: The path to linked file
        :param parser: The parser name in 'PARSERS' to dumps/loads data with file
        :param default_value: Default value
        :type default_value: dict
        :param storage: The storage name in 'STORAGES' to decide the method
            read/write. Default set as 'memory'.
        :param before_save: A function pass by user. Being fired before saving
            the file. Retrun False will abort the saving.
        :param onchanged: A function pass by user. Being fired once the
            config changed.
        '''

        self.path = path
        self.onchanged = onchanged or (lambda x: None)
        self.before_save = before_save or (lambda x: None)
        self.__pending_changes = False
        self.__binded = True
        self.__writing = False
        self.__use_async_writing = async_write
        self.__async_writing_thread = None

        if path:
            parser = parser or 'pretty-json'
            storage = storage or 'file'
        else:
            path = randstr(20)

        self.__storage = storage or 'memory'
        self.__parser = parser or 'none'

        if not self.__parser in PARSERS.keys():
            raise InvalidPaserError
        if not self.__storage in STORAGES.keys():
            raise InvalidStorageError

        self.__loads = PARSERS[self.__parser]['loads']
        self.__dumps = PARSERS[self.__parser]['dumps']
        self.__read = STORAGES[self.__storage]['read']
        self.__write = STORAGES[self.__storage]['write']

        if self.__storage == 'file' and not os.path.exists(self.path):
            self.__write(self.path, self.__dumps(default_value))

        if self.__storage == 'memory':
            self.__write(self.path, self.__dumps(default_value))

        super(Biconfigs,self).__init__(self.__loads(self.__read(self.path)),
                                       onchanged=self.__biconfig_onchanged)

    def __async_write(self):
        if self.__writing:
            return
        if not self.__use_async_writing:
            self.__sync_write()
        else:
            if not self.__async_writing_thread \
            or not self.__async_writing_thread.is_alive():
                self.__async_writing_thread = Thread(target=self.__sync_write)
                self.__async_writing_thread.start()

    def __sync_write(self):
        self.__writing = True
        self.__pending_changes = False
        self.__write(self.path, self.__dumps(self))
        self.__writing = False

        # If there are new changes made during writing
        # Write again
        if self.__pending_changes:
            self.__sync_write()

    def __biconfig_onchanged(self, obj):
        if not self.__binded:
            return
        self.__pending_changes = True
        self.onchanged(self)
        if self.before_save(self) == False:
            return
        self.__async_write()

    def _unbind(self):
        self.__binded = False

    def _rebind(self):
        self.__binded = True
        self.__biconfig_onchanged(self)

    def release(self):
        self._unbind()
        del(self)
