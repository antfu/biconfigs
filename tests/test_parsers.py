import biconfigs
from biconfigs import Biconfigs
import pytest

@pytest.mark.first
def test_parser_before_import():
    with pytest.raises(biconfigs.InvalidPaserError) as excinfo:
        Biconfigs(parser='cson')
    assert 'parser_cson' in str(excinfo.value)

    with pytest.raises(biconfigs.InvalidPaserError) as excinfo:
        Biconfigs(parser='yaml')
    assert 'parser_yaml' in str(excinfo.value)


def test_cson():
    from biconfigs import parser_cson

    configs = Biconfigs('tests/.test.demo.cson')
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
    configs.options.list.append({'nested': 3.1415})


def test_yaml():
    from biconfigs import parser_yaml

    configs = Biconfigs('tests/.test.demo.yml')
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
    configs.options.list.append({'nested': 3.1415})
