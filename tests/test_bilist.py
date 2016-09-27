import pytest
import biconfigs

def test_list():
    orginal_list = ['orginal_vale', 2]
    l = biconfigs.BiList(orginal_list)

    assert len(orginal_list) == len(l)

    for i in range(len(orginal_list)):
        assert l[i] == orginal_list[i]

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
