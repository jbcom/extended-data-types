import base64

from extended_data_types.base64_utils import base64_encode
from extended_data_types.export_utils import wrap_raw_data_for_export


def test_base64_encode_string():
    raw_data = "test data"
    expected_encoded_data = base64.b64encode(raw_data.encode("utf-8")).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=False)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."


def test_base64_encode_bytes():
    raw_data = b"test data"
    expected_encoded_data = base64.b64encode(raw_data).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=False)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."


def test_base64_encode_with_wrap():
    raw_data = "test data"
    wrapped_data = wrap_raw_data_for_export(raw_data).encode("utf-8")
    expected_encoded_data = base64.b64encode(wrapped_data).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=True)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."


def test_base64_encode_with_bytes_and_wrap():
    raw_data = b"test data"
    wrapped_data = wrap_raw_data_for_export(raw_data.decode("utf-8")).encode("utf-8")
    expected_encoded_data = base64.b64encode(wrapped_data).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=True)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."


def test_base64_encode_empty_string():
    raw_data = ""
    expected_encoded_data = base64.b64encode(raw_data.encode("utf-8")).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=False)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."


def test_base64_encode_empty_bytes():
    raw_data = b""
    expected_encoded_data = base64.b64encode(raw_data).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=False)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."


def test_base64_encode_empty_string_with_wrap():
    raw_data = ""
    wrapped_data = wrap_raw_data_for_export(raw_data).encode("utf-8")
    expected_encoded_data = base64.b64encode(wrapped_data).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=True)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."


def test_base64_encode_empty_bytes_with_wrap():
    raw_data = b""
    wrapped_data = wrap_raw_data_for_export(raw_data.decode("utf-8")).encode("utf-8")
    expected_encoded_data = base64.b64encode(wrapped_data).decode("utf-8")
    result = base64_encode(raw_data, wrap_raw_data=True)
    assert (
        result == expected_encoded_data
    ), f"Expected {expected_encoded_data}, but got {result}."
