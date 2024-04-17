from __future__ import annotations, division, print_function, unicode_literals

import pytest
from sortedcontainers import SortedDict

from extended_data_types.map_data_type import (
    all_values_from_map,
    deduplicate_map,
    filter_map,
    first_non_empty_value_from_map,
    flatten_map,
    get_default_dict,
    unhump_map,
    zipmap,
)


@pytest.fixture
def test_map():
    return {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "list": [1, 2, 3, {"key": "value"}],
        "nested": {"nested_key1": "nested_value1", "nested_key2": "nested_value2"},
    }


@pytest.fixture
def duplicated_map():
    return {
        "key1": ["value1", "value1", "value2"],
        "key2": {"subkey1": "value1", "subkey2": "value2", "subkey2": "value2"},
        "key3": "value3",
    }


@pytest.fixture
def test_keys():
    return ["key2", "key4", "key1"]


@pytest.fixture
def flattened_map():
    return {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "list.0": 1,
        "list.1": 2,
        "list.2": 3,
        "list.3.key": "value",
        "nested.nested_key1": "nested_value1",
        "nested.nested_key2": "nested_value2",
    }


@pytest.fixture
def a_list():
    return ["a", "b", "c"]


@pytest.fixture
def b_list():
    return ["1", "2", "3"]


@pytest.fixture
def zipmap_result():
    return {"a": "1", "b": "2", "c": "3"}


@pytest.fixture
def camel_case_map():
    return {
        "camelCaseKey": "value1",
        "anotherCamelCase": {"nestedCamelCaseKey": "nested_value1"},
        "withoutPrefix": "value2",
    }


@pytest.fixture
def snake_case_map():
    return {
        "camel_case_key": "value1",
        "another_camel_case": {"nested_camel_case_key": "nested_value1"},
    }


@pytest.fixture
def filter_map_data():
    return {
        "allowed1": "value1",
        "allowed2": "value2",
        "denied1": "value3",
        "denied2": "value4",
    }


@pytest.fixture
def allowlist():
    return ["allowed1", "allowed2"]


@pytest.fixture
def denylist():
    return ["denied1", "denied2"]


def test_first_non_empty_value_from_map(test_map, test_keys):
    result = first_non_empty_value_from_map(test_map, *test_keys)
    assert result == "value2"


def test_deduplicate_map(duplicated_map):
    result = deduplicate_map(duplicated_map)
    assert result == {
        "key1": ["value1", "value2"],
        "key2": {"subkey1": "value1", "subkey2": "value2"},
        "key3": "value3",
    }


def test_all_values_from_map(test_map):
    result = all_values_from_map(test_map)
    assert result == [
        "value1",
        "value2",
        "value3",
        1,
        2,
        3,
        "value",
        "nested_value1",
        "nested_value2",
    ]


def test_flatten_map(test_map, flattened_map):
    result = flatten_map(test_map)
    assert result == flattened_map


def test_zipmap(a_list, b_list, zipmap_result):
    result = zipmap(a_list, b_list)
    assert result == zipmap_result


def test_get_default_dict():
    result = get_default_dict()
    result["key"]["subkey"] = "value"
    assert result["key"]["subkey"] == "value"


def test_get_default_dict_sorted():
    result = get_default_dict(sorted=True)
    result["key"]["subkey"] = "value"
    assert result["key"]["subkey"] == "value"
    assert isinstance(result["key"], SortedDict)


def test_unhump_map(camel_case_map, snake_case_map):
    result = unhump_map(camel_case_map, drop_without_prefix=None)
    assert result == {
        "camel_case_key": "value1",
        "another_camel_case": {"nested_camel_case_key": "nested_value1"},
        "without_prefix": "value2",
    }


def test_filter_map(filter_map_data, allowlist, denylist):
    filtered, remaining = filter_map(
        filter_map_data, allowlist=allowlist, denylist=denylist
    )
    assert filtered == {"allowed1": "value1", "allowed2": "value2"}
    assert remaining == {"denied1": "value3", "denied2": "value4"}
