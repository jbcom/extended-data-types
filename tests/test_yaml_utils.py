import pytest

from extended_data_types.yaml_utils import (
    YamlPairs,
    YamlTagged,
    decode_yaml,
    encode_yaml,
)


CUSTOM_TAG_VALUE = 12345


@pytest.fixture()
def simple_yaml_fixture() -> str:
    return "test_key: test_value\nnested:\n  key1: value1\n  key2: value2\nlist:\n  - item1\n  - item2\n"


@pytest.fixture()
def complex_yaml_fixture() -> str:
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


def test_encode_yaml(simple_yaml_fixture: str) -> None:
    data = decode_yaml(simple_yaml_fixture)
    result = encode_yaml(data)
    expected_data = decode_yaml(simple_yaml_fixture)
    result_data = decode_yaml(result)
    assert result_data == expected_data


def test_yaml_construct_undefined() -> None:
    custom_tag_yaml_fixture = "!CustomTag\nname: custom\nvalue: 12345\n"
    data = decode_yaml(custom_tag_yaml_fixture)
    assert isinstance(data, YamlTagged)
    assert data.tag == "!CustomTag"
    assert data["name"] == "custom"
    assert data["value"] == CUSTOM_TAG_VALUE


def test_yaml_represent_tagged() -> None:
    data = YamlTagged("!CustomTag", {"name": "custom", "value": CUSTOM_TAG_VALUE})
    encoded_data = encode_yaml(data)
    assert "!CustomTag" in encoded_data
    assert "name: custom" in encoded_data
    assert f"value: {CUSTOM_TAG_VALUE}" in encoded_data


def test_yaml_pairs_representation() -> None:
    data = YamlPairs([("key1", "value1"), ("key2", "value2")])
    encoded_data = encode_yaml(data)
    assert "key1: value1" in encoded_data
    assert "key2: value2" in encoded_data


def test_decode_and_encode_complex_yaml(complex_yaml_fixture: str) -> None:
    data = decode_yaml(complex_yaml_fixture)
    assert isinstance(data, dict), f"Expected dict, but got {type(data)}"
    encoded_data = encode_yaml(data)
    assert "AWSTemplateFormatVersion" in encoded_data
    assert "Resources" in encoded_data
    assert "Outputs" in encoded_data
