from biconfigs import parser_cson
from biconfigs import Biconfigs

def test_cson():
    configs = Biconfigs('tests/.test.demo.cson', parser='cson', debug=True)
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
