from __future__ import annotations, division, print_function, unicode_literals

import pytest

from extended_data_types.json_utils import decode_json, encode_json


@pytest.fixture
def simple_json():
    return """{
  "key1": "value1",
  "key2": {
    "subkey1": "subvalue1",
    "subkey2": "subvalue2"
  },
  "key3": [
    1,
    2,
    3
  ]
}"""


@pytest.fixture
def simple_dict():
    return {
        "key1": "value1",
        "key2": {"subkey1": "subvalue1", "subkey2": "subvalue2"},
        "key3": [1, 2, 3],
    }


def test_decode_json(simple_json, simple_dict):
    result = decode_json(simple_json)
    assert result == simple_dict


def test_encode_json(simple_dict, simple_json):
    result = encode_json(simple_dict)
    assert result == simple_json
