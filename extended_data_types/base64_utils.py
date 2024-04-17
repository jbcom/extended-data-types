from __future__ import annotations, division, print_function, unicode_literals

from base64 import b64encode
from typing import Union

from extended_data_types.export_utils import wrap_raw_data_for_export


def base64_encode(raw_data: Union[str, bytes], wrap_raw_data: bool = True) -> str:
    """Encodes data to base64 format.

    Args:
        raw_data (Union[str, bytes]): The data to encode.
        wrap_raw_data (bool): Whether to wrap the raw data for export.

    Returns:
        str: The base64 encoded string.
    """
    if wrap_raw_data:
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode("utf-8")
        raw_data = wrap_raw_data_for_export(raw_data).encode("utf-8")
    elif isinstance(raw_data, str):
        raw_data = raw_data.encode("utf-8")

    return b64encode(raw_data).decode("utf-8")
