import pytest
import sys

from extended_data_types.json_utils import decode_json, encode_json


@pytest.fixture
def with_orjson(monkeypatch):
    """Mock the import to simulate `orjson` being available."""
    original_import = __import__

    def import_mock(name, *args):
        if name == "orjson":
            return original_import(name, *args)
        raise ImportError(f"No module named '{name}'")

    monkeypatch.setattr("builtins.__import__", import_mock)
    monkeypatch.setitem(sys.modules, "orjson", sys.modules[original_import("orjson").__name__])
    yield


@pytest.fixture
def without_orjson(monkeypatch):
    """Mock the import to simulate `orjson` being unavailable."""
    original_import = __import__

    def import_mock(name, *args):
        if name == "orjson":
            raise ImportError(f"No module named '{name}'")
        return original_import(name, *args)

    monkeypatch.setattr("builtins.__import__", import_mock)
    monkeypatch.delitem(sys.modules, "orjson", None)
    yield


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


@pytest.mark.usefixtures("with_orjson")
def test_decode_json_with_orjson(simple_json, simple_dict):
    result = decode_json(simple_json)
    assert result == simple_dict


@pytest.mark.usefixtures("without_orjson")
def test_decode_json_without_orjson(simple_json, simple_dict):
    result = decode_json(simple_json)
    assert result == simple_dict


@pytest.mark.usefixtures("with_orjson")
def test_encode_json_with_orjson(simple_dict, simple_json):
    result = encode_json(simple_dict, indent=2)
    assert result == simple_json


@pytest.mark.usefixtures("without_orjson")
def test_encode_json_without_orjson(simple_dict, simple_json):
    result = encode_json(simple_dict, indent=2)
    assert result == simple_json
