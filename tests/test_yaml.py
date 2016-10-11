from biconfigs import support_yaml, Biconfigs

def test_yaml():
    configs = Biconfigs('.test.demo.yml', parser='yaml', debug=True)
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
