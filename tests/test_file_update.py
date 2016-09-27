from __future__ import print_function

import pytest
import biconfigs
import json
import os
from codecs import open

FILENAME = '.test_file_update.json'

def readfile():
    with open(FILENAME,'r','utf-8') as f:
        return f.read()

class TestFileUpdate(object):

    def setup_class(cls):
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        # Create a BiConfigs instance,
        # set parser='json' to disable json beautify
        cls.config = biconfigs.BiConfigs(path=FILENAME, default_value={'default':'value'}, parser='json')
        assert cls.config.storage == 'file'
        assert os.path.exists(FILENAME)
        assert readfile() == '{"default": "value"}'

    def test_basic_update(self):
        self.config.clear()
        assert readfile() == '{}'

        self.config['item1'] = 'value'
        assert readfile() == '{"item1": "value"}'

        del(self.config['item1'])
        assert readfile() == '{}'

    def test_nested_update(self):
        pass

    def test_get_set(self):
        self.config.clear()

        # get_set a value should update to file instantly
        assert self.config.get_set('item', 'value') == 'value'
        # should return the previous value when get_set at the 2nd time
        assert self.config.get_set('item', 'wrong-value') == 'value'
        assert readfile() == '{"item": "value"}'

        self.config.clear()

        # get_set a dict/list should not update the file
        # until the nested dict/list changed
        get_set_dict = self.config.get_set('item', {})
        # should return the previous value when get_set at the 2nd time
        assert self.config.get_set('item', None) == get_set_dict
        assert readfile() == '{}'
        assert isinstance(get_set_dict, biconfigs.BiDict)

        # nested dict changed, update the file
        get_set_dict['nested'] = 1
        assert readfile() == '{"item": {"nested": 1}}'
