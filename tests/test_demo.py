from biconfigs import Biconfigs

def test_demo():
    configs = Biconfigs('configs.json')
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
