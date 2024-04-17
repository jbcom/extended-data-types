from __future__ import annotations, division, print_function, unicode_literals

from io import StringIO
from typing import Any

import hcl2
from lark.exceptions import UnexpectedToken


def decode_hcl2(hcl2_data: str) -> Any:
    """Decodes HCL2 data into a Python object.

    Args:
        hcl2_data (str): The HCL2 data to decode.

    Returns:
        Any: The decoded Python object.

    Raises:
        ValueError: If the HCL2 data cannot be parsed.
    """
    hcl2_data_stream = StringIO(hcl2_data)
    try:
        return hcl2.load(hcl2_data_stream)
    except UnexpectedToken as e:
        raise ValueError(f"Invalid HCL2 data: {e}")
