"""This module contains test functions for verifying the functionality of wrapping raw YAML data for export using the
`extended_data_types` package. It includes fixtures for simple and complex YAML data and tests for ensuring the proper
encoding and wrapping of this data.

Fixtures:
    - simple_yaml_fixture: Provides a simple YAML string for testing.
    - complex_yaml_fixture: Provides a complex YAML string representing an AWS CloudFormation template for testing.

Functions:
    - test_wrap_raw_data_for_export_yaml: Tests wrapping and encoding of simple YAML data.
    - test_wrap_raw_data_for_export_yaml_complex: Tests wrapping and encoding of complex YAML data.
"""

from __future__ import annotations

import pytest

from extended_data_types.export_utils import wrap_raw_data_for_export
from extended_data_types.yaml_utils import decode_yaml


@pytest.fixture()
def simple_yaml_fixture() -> str:
    """Provides a simple YAML string for testing.

    Returns:
        str: A simple YAML string.
    """
    return "test_key: test_value\nnested:\n  key1: value1\n  key2: value2\nlist:\n  - item1\n  - item2\n"


@pytest.fixture()
def complex_yaml_fixture() -> str:
    """Provides a complex YAML string representing an AWS CloudFormation template for testing.

    Returns:
        str: A complex YAML string.
    """
    return """
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyBucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: !Sub '${AWS::StackName}-bucket'
      Tags:
        - Key: Name
          Value: !Ref 'AWS::StackName'
Outputs:
  BucketName:
    Value: !Ref MyBucket
    Description: Name of the bucket
"""


def test_wrap_raw_data_for_export_yaml(simple_yaml_fixture: str) -> None:
    """Tests wrapping and encoding of simple YAML data.

    Args:
        simple_yaml_fixture (str): A simple YAML string provided by the fixture.

    Asserts:
        The result of wrap_raw_data_for_export contains key parts of the original YAML string.
    """
    result = wrap_raw_data_for_export(
        decode_yaml(simple_yaml_fixture),
        allow_encoding="yaml",
    )
    assert "test_key: test_value" in result
    assert "key1: value1" in result


def test_wrap_raw_data_for_export_yaml_complex(complex_yaml_fixture: str) -> None:
    """Tests wrapping and encoding of complex YAML data.

    Args:
        complex_yaml_fixture (str): A complex YAML string provided by the fixture.

    Asserts:
        The result of wrap_raw_data_for_export contains key parts of the original YAML string.
    """
    result = wrap_raw_data_for_export(
        decode_yaml(complex_yaml_fixture),
        allow_encoding="yaml",
    )
    assert 'AWSTemplateFormatVersion: "2010-09-09"' in result
    assert 'Type: "AWS::S3::Bucket"' in result
