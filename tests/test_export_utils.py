import pytest

from extended_data_types.export_utils import wrap_raw_data_for_export
from extended_data_types.yaml_utils import decode_yaml


@pytest.fixture()
def simple_yaml_fixture():
    return "test_key: test_value\nnested:\n  key1: value1\n  key2: value2\nlist:\n  - item1\n  - item2\n"


@pytest.fixture()
def complex_yaml_fixture():
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


def test_wrap_raw_data_for_export_yaml(simple_yaml_fixture):
    result = wrap_raw_data_for_export(
        decode_yaml(simple_yaml_fixture), allow_encoding="yaml",
    )
    assert "test_key: test_value" in result
    assert "key1: value1" in result


def test_wrap_raw_data_for_export_yaml_complex(complex_yaml_fixture):
    result = wrap_raw_data_for_export(
        decode_yaml(complex_yaml_fixture), allow_encoding="yaml",
    )
    assert 'AWSTemplateFormatVersion: "2010-09-09"' in result
    assert 'Type: "AWS::S3::Bucket"' in result
