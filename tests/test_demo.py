from biconfigs import BiConfigs

def test_demo():
    configs = BiConfigs('configs.json')
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
