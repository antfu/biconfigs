import pytest
import biconfigs

changed_count = 0
def test_list():
    global changed_count
    changed_count = 0

    def onchanged(obj):
        global changed_count
        changed_count += 1

    orginal_dict = {'a': 1, 'b': 2}
    d = biconfigs.Bidict(orginal_dict, onchanged=onchanged)

    assert changed_count == 0
    assert d.pop('a') == 1
    assert d.popitem() == ('b', 2)
    assert changed_count == 2

    d.update({'c': 123, 'd': 456})
    assert changed_count == 3
    assert d['c'] == 123

def test_dict():
    d = biconfigs.Bidict({'orginal_key': 'orginal_value'})

    assert d['orginal_key'] == 'orginal_value'
    assert d.orginal_key == 'orginal_value'

    d['setitem1'] = 'value1'
    assert d['setitem1'] == 'value1'

    d['setitem2'] = 2.1
    assert d['setitem2'] == 2.1

    with pytest.raises(KeyError):
        _ = d['item_not_exists']

    with pytest.raises(AttributeError):
        _ = d.item_not_exists

    d['itemtodel'] = 'value'
    assert d['itemtodel'] == 'value'
    del(d['itemtodel'])
    with pytest.raises(KeyError):
        _ = d['itemtodel']

def test_with():
    global changed_count
    changed_count = 0

    def onchanged(obj):
        global changed_count
        changed_count += 1

    d = biconfigs.Bidict({'orginal_key': 'orginal_value'}, onchanged=onchanged)

    assert changed_count == 0

    d['key1'] = 'value1'
    d['key2'] = 'value2'
    assert changed_count == 2

    # New value is just as same as the old one, should not fire changed
    d['key1'] = 'value1'
    d['key2'] = 'value2'
    assert changed_count == 2

    with d:
        for i in range(100):
            d['key'] = i

    assert changed_count == 3

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
