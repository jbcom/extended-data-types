"""Transformation helpers for numbers and strings.

This namespace groups high-level utility APIs that operate on top of the
primitive data-type helpers that ship with the project (for example the
`number_transformations` and `string_data_type` modules).  Tests import
symbols from sub-packages such as
`extended_data_types.transformations.numbers` and
`extended_data_types.transformations.strings`, so providing an explicit
package makes those imports possible.
"""

__all__ = [
    "numbers",
    "strings",
]
