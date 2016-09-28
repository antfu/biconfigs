import pytest
import biconfigs

def test_dict():
    d = biconfigs.Bidict({'orginal_key': 'orginal_value'})

    assert d['orginal_key'] == 'orginal_value'
    assert d.orginal_key == 'orginal_value'

    d['setitem1'] = 'value1'
    assert d['setitem1'] == 'value1'

    d['setitem2'] = 2.1
    assert d['setitem2'] == 2.1

    with pytest.raises(KeyError) as exinfo:
        d['item_not_exists']

    with pytest.raises(AttributeError) as exinfo:
        d.item_not_exists

    d['itemtodel'] = 'value'
    assert d['itemtodel'] == 'value'
    del(d['itemtodel'])
    with pytest.raises(KeyError) as exinfo:
        d['itemtodel']

def test_nested():
    d = biconfigs.Bidict({'nested_dict': {
                            'key1': 'value1',
                            'key2': 2
                         },
                         'nested_list': [
                            'item1',
                            2
                         ]})

    assert isinstance(d.nested_dict, biconfigs.Bidict)
    assert isinstance(d.nested_list, biconfigs.Bilist)

    assert d.nested_dict.key1 == 'value1'
    assert d.nested_list[1] == 2

    d['new_nested_dict'] = {}
    d['new_nested_list'] = []

    assert isinstance(d.new_nested_dict, biconfigs.Bidict)
    assert isinstance(d.new_nested_list, biconfigs.Bilist)
