import biconfigs
import time
import pytest

write_count = 0
def test_callbacks_sync():
    global write_count
    write_count = 0

    def before_save(config):
        if config.get('abort_save', False):
            return False

    config = biconfigs.Biconfigs(
        before_save=before_save,
        parser='json',
        async_write=False
    )

    # Hack to check write times
    old_write = config._Biconfigs__write
    def alter_write(*args):
        global write_count
        old_write(*args)
        write_count += 1
    config._Biconfigs__write = alter_write

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

class TestBlocking():
    def setup_class(self):
        self.sleeptime = 0.05
        self.writing = False
        self.blocking_config = biconfigs.Biconfigs(async_write=False)
        self.non_blocking_config = biconfigs.Biconfigs(async_write=True)

        def fake_write(*args):
            self.writing = True
            time.sleep(self.sleeptime)
            self.writing = False

        self.blocking_config._Biconfigs__write = fake_write
        self.non_blocking_config._Biconfigs__write = fake_write

    def test_blocking(self):
        self.blocking_config['item'] = 'value'
        assert self.writing == False

    def test_non_blocking(self):
        assert self.writing == False
        self.non_blocking_config['item'] = 'value'
        assert self.writing == True
        time.sleep(self.sleeptime*2)
        assert self.writing == False


def test_invalid_parser_storages():
    with pytest.raises(biconfigs.InvalidPaserError):
        biconfigs.Biconfigs(parser='invalid_parser')

    with pytest.raises(biconfigs.InvalidStorageError):
        biconfigs.Biconfigs(storage='invalid_storage')

    with pytest.raises(biconfigs.AlreadyCreatedError):
        biconfigs.Biconfigs(path='.test.json')
        biconfigs.Biconfigs(path='.test.json')

def test_io_expections():
    with pytest.raises(biconfigs.InvaildFilePathError):
        biconfigs.Biconfigs('/')

    with pytest.raises(biconfigs.InvaildFilePathError):
        biconfigs.Biconfigs('..')

    with pytest.raises(biconfigs.FailedOpeningFileError):
        biconfigs.Biconfigs(path='not_exits/file')
