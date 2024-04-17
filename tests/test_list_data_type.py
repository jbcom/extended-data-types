import pytest

from extended_data_types.list_data_type import filter_list, flatten_list


@pytest.fixture
def nested_list():
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


@pytest.fixture
def flat_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


@pytest.fixture
def test_list():
    return ["apple", "banana", "cherry", "date"]


@pytest.fixture
def allowlist():
    return ["apple", "cherry"]


@pytest.fixture
def denylist():
    return ["banana", "date"]


@pytest.fixture
def allowlist_and_denylist():
    return {"allowlist": ["apple", "cherry", "date"], "denylist": ["date"]}


def test_flatten_list(nested_list, flat_list):
    result = flatten_list(nested_list)
    assert result == flat_list


def test_filter_list_allowlist(test_list, allowlist):
    result = filter_list(test_list, allowlist=allowlist)
    assert result == ["apple", "cherry"]


def test_filter_list_denylist(test_list, denylist):
    result = filter_list(test_list, denylist=denylist)
    assert result == ["apple", "cherry"]


def test_filter_list_allowlist_and_denylist(test_list, allowlist_and_denylist):
    result = filter_list(
        test_list,
        allowlist=allowlist_and_denylist["allowlist"],
        denylist=allowlist_and_denylist["denylist"],
    )
    assert result == ["apple", "cherry"]


def test_filter_list_none_input():
    result = filter_list(None)
    assert result == []
