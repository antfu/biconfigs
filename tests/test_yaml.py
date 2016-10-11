from biconfigs import parser_yaml
from biconfigs import Biconfigs

def test_yaml():
    configs = Biconfigs('tests/.test.demo.yml', parser='yaml', debug=True)
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
