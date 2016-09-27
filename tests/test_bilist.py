import pytest
import biconfigs

change_count = 0
def test_list():
    global change_count

    def onchanged(list):
        global change_count
        change_count += 1

    orginal_list = ['orginal_vale', 2]
    l = biconfigs.BiList(orginal_list, onchanged=onchanged)

    assert len(orginal_list) == len(l)

    for i in range(len(orginal_list)):
        assert l[i] == orginal_list[i]

    # Should not fire changed till now
    assert change_count == 0

    l.clear()
    assert change_count == 1

    l.append(123)
    assert change_count == 2

    l.insert(0, 'insert-0')
    assert change_count == 3

    l.reverse()
    assert change_count == 4

    l[1] = 'reversed'
    assert change_count == 5

    l.remove(123)
    assert change_count == 6

    l.pop()
    assert change_count == 7

    l.append('value')
    assert change_count == 8
    del(l[0])

    assert change_count == 9

    assert len(l) == 0

def test_nested():
    nested_dict1 = {'key1':'value1'}
    nested_list1 = ['nested_list', 2, 3]
    orginal_list = [nested_dict1, nested_list1]
    l = biconfigs.BiList(orginal_list)

    assert isinstance(l[0], biconfigs.BiDict)
    assert isinstance(l[1], biconfigs.BiList)

    for k in nested_dict1.keys():
        assert l[0][k] == nested_dict1[k]

    for i in range(len(nested_list1)):
        assert l[1][i] == nested_list1[i]

    l.clear()
    l.append([])
    l.append({})
    assert isinstance(l[0], biconfigs.BiList)
    assert isinstance(l[1], biconfigs.BiDict)
