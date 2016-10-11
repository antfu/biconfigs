from biconfigs import cson_support, Biconfigs

def test_cson():
    configs = Biconfigs('configs.cson', parser='cson')
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
