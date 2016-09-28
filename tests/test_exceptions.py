import pytest
import biconfigs

def test_invalid_parser_storages():
    with pytest.raises(biconfigs.InvalidPaserError):
        biconfigs.BiConfigs(parser='invalid_parser')

    with pytest.raises(biconfigs.InvalidStorageError):
        biconfigs.BiConfigs(storage='invalid_storage')
