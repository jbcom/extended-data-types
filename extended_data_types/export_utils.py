from __future__ import annotations, division, print_function, unicode_literals

import datetime
import pathlib
from typing import Any, Mapping, Union

from extended_data_types.json_utils import encode_json
from extended_data_types.string_data_type import strtobool
from extended_data_types.yaml_utils import (
    YamlPairs,
    YamlTagged,
    encode_yaml,
    is_yaml_data,
)


def make_raw_data_export_safe(raw_data: Any, export_to_yaml: bool = False) -> Any:
    """Makes raw data export safe by converting certain types to strings.

    Args:
        raw_data (Any): The raw data to process.
        export_to_yaml (bool): Flag to indicate if the data is for YAML export.

    Returns:
        Any: The processed data.
    """
    if isinstance(raw_data, Mapping):
        return {
            k: make_raw_data_export_safe(v, export_to_yaml=export_to_yaml)
            for k, v in raw_data.items()
        }
    elif isinstance(raw_data, (set, list)):
        return [
            make_raw_data_export_safe(v, export_to_yaml=export_to_yaml)
            for v in raw_data
        ]

    if isinstance(raw_data, YamlTagged):
        raw_data = raw_data.__wrapped__
    elif isinstance(raw_data, YamlPairs):
        raw_data = list(raw_data)

    if isinstance(raw_data, (datetime.date, datetime.datetime)):
        return raw_data.isoformat()
    elif isinstance(raw_data, pathlib.Path):
        return str(raw_data)
    elif isinstance(raw_data, (int, float, str, bool, type(None))):
        return raw_data

    # For all other types, convert to string representation
    return str(raw_data)


def wrap_raw_data_for_export(
    raw_data: Union[Mapping, Any],
    allow_encoding: Union[bool, str] = True,
    **format_opts: Any,
) -> str:
    """Wraps raw data for export, optionally encoding it.

    Args:
        raw_data (Any): The raw data to wrap.
        allow_encoding (str): The encoding format (default is 'yaml').

    Returns:
        str: The wrapped and encoded data.
    """
    raw_data = make_raw_data_export_safe(raw_data)

    if isinstance(allow_encoding, str):
        allow_encoding_lower = allow_encoding.casefold()
        if allow_encoding_lower == "yaml":
            return encode_yaml(raw_data)
        elif allow_encoding_lower == "json":
            return encode_json(raw_data, **format_opts)
        elif allow_encoding_lower == "raw":
            return raw_data

        try:
            allow_encoding_bool = strtobool(allow_encoding, raise_on_error=True)
            allow_encoding = (
                allow_encoding_bool
                if isinstance(allow_encoding_bool, bool)
                else allow_encoding
            )
        except ValueError:
            raise ValueError(f"Invalid allow_encoding value: {allow_encoding}")

    if allow_encoding:
        if is_yaml_data(raw_data):
            return encode_yaml(raw_data)
        return encode_json(raw_data, **format_opts)

    return raw_data
