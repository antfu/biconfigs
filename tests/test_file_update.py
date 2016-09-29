from __future__ import print_function

import pytest
import biconfigs
import json
import os
import codecs

FILENAME = '.test_file_update.json'

def readfile():
    with codecs.open(FILENAME,'r','utf-8') as f:
        return f.read()

def writefile(data):
    with codecs.open(FILENAME,'w','utf-8') as f:
        return f.write(data)

class TestFileUpdate(object):

    def setup_class(self):
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        # Create a Biconfigs instance,
        self.config = biconfigs.Biconfigs(path=FILENAME,
                                        default_value={'default':'value'},
                                        # set parser='json' to disable json beautify
                                        parser='json',
                                        # use sync writing
                                        async_write=False)
        assert self.config._Biconfigs__storage == 'file'
        assert self.config.storage == '<file:'+FILENAME+'>'
        assert os.path.exists(FILENAME)
        assert readfile() == '{"default": "value"}'

    def teardown_class(self):
        self.config.release()
        if os.path.exists(FILENAME):
            os.remove(FILENAME)

    def test_basic_update(self):
        self.config.clear()
        assert readfile() == '{}'

        self.config['item1'] = 'value'
        assert readfile() == '{"item1": "value"}'

        del(self.config['item1'])
        assert readfile() == '{}'

    def test_nested_update(self):
        pass

    def test_setdefault(self):
        self.config.clear()

        # setdefault a value should update to file instantly
        assert self.config.setdefault('item', 'value') == 'value'
        # should return the previous value when setdefault at the 2nd time
        assert self.config.setdefault('item', 'wrong-value') == 'value'
        assert readfile() == '{"item": "value"}'

        self.config.clear()

        # setdefault a dict/list should not update the file
        # until the nested dict/list changed
        sd_dict = self.config.setdefault('gs_dict', {})
        sd_list = self.config.setdefault('gs_list', [])
        # should return the previous value when setdefault at the 2nd time
        assert self.config.setdefault('gs_dict', None) == sd_dict
        assert isinstance(sd_dict, biconfigs.Bidict)
        assert isinstance(sd_list, biconfigs.Bilist)

        del(self.config['gs_list'])

        sd_dict['nested'] = 1
        assert readfile() == '{"gs_dict": {"nested": 1}}'

    def test_reload(self):
        self.config.clear()
        assert readfile() == '{}'

        self.config['item1'] = 'value'
        assert readfile() == '{"item1": "value"}'

        writefile(json.dumps(dict(a=123,b='value')))
        assert self.config['item1'] == 'value'
        self.config.reload()

        assert self.config.a == 123
        assert self.config.b == 'value'
        assert len(self.config) == 2
        with pytest.raises(AttributeError):
            _ = self.config.item1
