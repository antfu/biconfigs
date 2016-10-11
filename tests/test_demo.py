from biconfigs import Biconfigs

def test_demo():
    # This is a simple example for Biconfigs
    # The only purpose of this test is to make sure there is no exception occurs
    configs = Biconfigs('tests/.test.demo.json')
    configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

    configs.options.list.append('example')
