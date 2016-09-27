from __future__ import print_function

import pytest
import biconfigs

class TestFileUpdate(object):

    def setup_class(cls):
        cls.config = biconfigs.BiConfigs(path='test_file_update.json')
        cls.config.clear()

    def test_clear(self):
        self.config.clear()
        assert str(self.config) == '{}'
