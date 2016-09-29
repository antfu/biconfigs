import biconfigs
import json

class TestMemoryStorage(object):

    def setup_class(self):
        self.change_count = 0
        def onchanged(config):
            self.change_count += 1

        self.config = biconfigs.Biconfigs(
            default_value={'default':'value'},
            onchanged=onchanged
        )
        assert self.config._Biconfigs__storage == 'memory'
        assert self.change_count == 0
        assert json.dumps(self.config) == '{"default": "value"}'

    def test_basic_update(self):
        self.config.clear()
        assert json.dumps(self.config) == '{}'

        self.config['item1'] = 'value'
        assert json.dumps(self.config) == '{"item1": "value"}'

        del(self.config['item1'])
        assert json.dumps(self.config) == '{}'
