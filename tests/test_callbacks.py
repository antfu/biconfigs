import biconfigs
import json

write_count = 0
def test_callbacks():
    global write_count
    write_count = 0

    def before_save(config):
        if config.get('abort_save', False):
            return False

    config = biconfigs.Biconfigs(
        before_save=before_save,
        parser='json'
    )

    # Hack to check write times
    old_write = config.write
    def alter_write(*args):
        global write_count
        old_write(*args)
        write_count += 1
    config.write = alter_write

    assert write_count == 0
    config['123'] = '123'
    assert write_count == 1
    config['abort_save'] = True
    assert write_count == 1
    config['321'] = '321'
    assert write_count == 1
    del(config['abort_save'])
    assert write_count == 2

    write_count = 0
    config['123'] = '1234'
    assert write_count == 1
    config._unbind()
    config['123'] = '12345'
    assert write_count == 1
    config._rebind()
    assert write_count == 2
