import biconfigs
import json

class TestMemoryStorage(object):

    def setup_class(cls):
        cls.change_count = 0
        def onchanged(config):
            cls.change_count += 1

        cls.config = biconfigs.BiConfigs(
            default_value={'default':'value'},
            onchanged=onchanged
        )
        assert cls.config.storage == 'memory'
        assert cls.change_count == 0
        assert json.dumps(cls.config) == '{"default": "value"}'

    def test_basic_update(self):
        self.config.clear()
        assert json.dumps(self.config) == '{}'

        self.config['item1'] = 'value'
        assert json.dumps(self.config) == '{"item1": "value"}'

        del(self.config['item1'])
        assert json.dumps(self.config) == '{}'
