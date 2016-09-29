import pytest
import biconfigs

change_count = 0
def test_list():
    global change_count

    def onchanged(list):
        global change_count
        change_count += 1

    orginal_list = ['orginal_vale', 2]
    l = biconfigs.Bilist(orginal_list, onchanged=onchanged)

    assert len(orginal_list) == len(l)

    for i in range(len(orginal_list)):
        assert l[i] == orginal_list[i]

    # Should not fire changed till now
    assert change_count == 0

    l.clear()
    assert len(l) == 0
    # []
    l.append(123)
    # [123]
    l.insert(0, 'inserted')
    # ['inserted', 123]
    l.reverse()
    # [123, 'inserted']
    l[1] = 'reversed'
    # [123, 'reversed']
    l.remove(123)
    # ['reversed']
    assert l.pop() == 'reversed'
    # []
    l.append('value')
    # ['value']
    l.extend([4,3,1])
    # ['value', 4, 3, 1]
    del(l[0])
    # [4, 3, 1]
    l.sort()
    # [1, 3, 4]
    assert l[0] == 1

    assert change_count == 11

    assert len(l) == 3

changed_count = 0
def test_with():
    global changed_count
    changed_count = 0
    def onchanged(obj):
        global changed_count
        changed_count += 1

    l = biconfigs.Bilist([1, 2], onchanged=onchanged)

    assert changed_count == 0

    l.append(3)
    l.append(4)
    assert changed_count == 2

    # New value is just as same as the old one, should not fire changed
    l[0] = 1
    l[2] = 3
    assert changed_count == 2

    with pytest.raises(IndexError):
        l[100] = 1

    with l:
        for i in range(5,10):
            l.append(i)

    assert changed_count == 3

def test_nested():
    nested_dict1 = {'key1':'value1'}
    nested_list1 = ['nested_list', 2, 3]
    orginal_list = [nested_dict1, nested_list1]
    l = biconfigs.Bilist(orginal_list)

    assert isinstance(l[0], biconfigs.Bidict)
    assert isinstance(l[1], biconfigs.Bilist)

    for k in nested_dict1.keys():
        assert l[0][k] == nested_dict1[k]

    for i in range(len(nested_list1)):
        assert l[1][i] == nested_list1[i]

    l.clear()
    l.append([])
    l.append({})
    assert isinstance(l[0], biconfigs.Bilist)
    assert isinstance(l[1], biconfigs.Bidict)
