import pytest
import biconfigs

def test_invalid_parser_storages():
    with pytest.raises(biconfigs.InvalidPaserError):
        biconfigs.Biconfigs(parser='invalid_parser')

    with pytest.raises(biconfigs.InvalidStorageError):
        biconfigs.Biconfigs(storage='invalid_storage')

    with pytest.raises(biconfigs.AlreadyCreatedError):
        biconfigs.Biconfigs(path='.test.json')
        biconfigs.Biconfigs(path='.test.json')
