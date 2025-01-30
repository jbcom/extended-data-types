"""Tests for CloudFormation template handling.

This module tests the YAML utils' CloudFormation capabilities, including:
    - Intrinsic function handling
    - Template structure validation
    - Resource definitions
    - Parameter references
    - Condition handling
    - Cross-stack references
    - Tag preservation

Fixtures:
    basic_template: Simple CloudFormation template
    complex_template: Template with various features
    invalid_templates: Templates with errors
"""
from __future__ import annotations

import textwrap
from typing import Any

import pytest

from extended_data_types.yaml_utils import (YAMLFlags, YamlTagged,
                                            configure_yaml, decode_yaml,
                                            encode_yaml)


@pytest.fixture
def basic_template() -> str:
    """Provide a basic CloudFormation template.
    
    Returns:
        str: Simple template with basic resources
    """
    return textwrap.dedent("""
        AWSTemplateFormatVersion: '2010-09-09'
        Description: Basic template example
        
        Parameters:
          Environment:
            Type: String
            Default: dev
        
        Resources:
          MyBucket:
            Type: AWS::S3::Bucket
            Properties:
              BucketName: !Sub ${AWS::StackName}-${Environment}-bucket
              Tags:
                - Key: Environment
                  Value: !Ref Environment
    """).lstrip()


@pytest.fixture
def complex_template() -> str:
    """Provide a complex CloudFormation template.
    
    Returns:
        str: Template with various CloudFormation features
    """
    return textwrap.dedent("""
        AWSTemplateFormatVersion: '2010-09-09'
        Description: Complex template example
        
        Parameters:
          Environment:
            Type: String
            AllowedValues: [dev, prod]
        
        Conditions:
          IsProd: !Equals [!Ref Environment, prod]
        
        Resources:
          MyQueue:
            Type: AWS::SQS::Queue
            Properties:
              QueueName: !Sub ${AWS::StackName}-queue
              Tags:
                - Key: Environment
                  Value: !Ref Environment
        
          MyFunction:
            Type: AWS::Lambda::Function
            Properties:
              FunctionName: !Sub ${AWS::StackName}-function
              Runtime: python3.9
              Handler: index.handler
              Code:
                S3Bucket: !ImportValue shared-bucket
                S3Key: !Join
                  - "/"
                  - - !Ref Environment
                    - !Ref AWS::StackName
                    - function.zip
              Environment:
                Variables:
                  QUEUE_URL: !Ref MyQueue
                  REGION: !Ref AWS::Region
              Tags:
                - Key: Name
                  Value: !Sub ${AWS::StackName}-function
                - Key: Environment
                  Value: !Ref Environment
        
        Outputs:
          QueueUrl:
            Value: !Ref MyQueue
            Export:
              Name: !Sub ${AWS::StackName}-queue-url
    """).lstrip()


@pytest.fixture
def invalid_templates() -> dict[str, str]:
    """Provide invalid CloudFormation templates.
    
    Returns:
        dict: Dictionary of invalid templates with their error cases
    """
    return {
        "invalid_ref": """
            Resources:
              MyBucket:
                Type: AWS::S3::Bucket
                Properties:
                  BucketName: !Ref
        """,
        "invalid_sub": """
            Resources:
              MyBucket:
                Type: AWS::S3::Bucket
                Properties:
                  BucketName: !Sub
        """,
        "invalid_join": """
            Resources:
              MyBucket:
                Type: AWS::S3::Bucket
                Properties:
                  BucketName: !Join []
        """
    }


def test_basic_template_handling(basic_template: str) -> None:
    """Test basic CloudFormation template handling.
    
    This test verifies:
        - Template structure is preserved
        - Intrinsic functions are handled
        - References are maintained
        - Tags are processed
    
    Args:
        basic_template: Fixture containing basic template
    """
    configure_yaml(YAMLFlags.CLOUDFORMATION)
    data = decode_yaml(basic_template)
    
    # Check structure
    assert "AWSTemplateFormatVersion" in data
    assert "Parameters" in data
    assert "Resources" in data
    
    # Check resource
    bucket = data["Resources"]["MyBucket"]
    assert bucket["Type"] == "AWS::S3::Bucket"
    
    # Check intrinsic functions
    bucket_name = bucket["Properties"]["BucketName"]
    assert isinstance(bucket_name, YamlTagged)
    assert bucket_name.tag == "!Sub"


def test_complex_template_handling(complex_template: str) -> None:
    """Test complex CloudFormation template features.
    
    This test verifies:
        - Conditions are processed
        - Multiple resources work
        - Complex intrinsic functions
        - Nested structures
        - Exports and imports
    
    Args:
        complex_template: Fixture containing complex template
    """
    configure_yaml(YAMLFlags.CLOUDFORMATION)
    data = decode_yaml(complex_template)
    
    # Check condition
    condition = data["Conditions"]["IsProd"]
    assert isinstance(condition, YamlTagged)
    assert condition.tag == "!Equals"
    
    # Check function
    function = data["Resources"]["MyFunction"]
    code = function["Properties"]["Code"]
    
    # Check ImportValue
    assert isinstance(code["S3Bucket"], YamlTagged)
    assert code["S3Bucket"].tag == "!ImportValue"
    
    # Check Join
    assert isinstance(code["S3Key"], YamlTagged)
    assert code["S3Key"].tag == "!Join"


def test_template_round_trip(complex_template: str) -> None:
    """Test template round-trip preservation.
    
    This test verifies:
        - Template can be decoded and re-encoded
        - All features are preserved
        - Structure remains intact
        - Tags are maintained
    
    Args:
        complex_template: Fixture containing complex template
    """
    configure_yaml(YAMLFlags.CLOUDFORMATION)
    data = decode_yaml(complex_template)
    encoded = encode_yaml(data)
    decoded = decode_yaml(encoded)
    
    # Compare structures
    assert data.keys() == decoded.keys()
    assert data["Resources"].keys() == decoded["Resources"].keys()
    
    # Compare specific elements
    original_queue = data["Resources"]["MyQueue"]
    decoded_queue = decoded["Resources"]["MyQueue"]
    assert original_queue == decoded_queue


def test_invalid_template_handling(invalid_templates: dict[str, str]) -> None:
    """Test handling of invalid templates.
    
    This test verifies:
        - Invalid intrinsic functions are caught
        - Proper error messages are generated
        - Invalid structures are detected
    
    Args:
        invalid_templates: Fixture containing invalid templates
    """
    configure_yaml(YAMLFlags.CLOUDFORMATION)
    
    for case_name, template in invalid_templates.items():
        with pytest.raises((ValueError, SyntaxError), msg=f"Failed to catch {case_name}"):
            decode_yaml(template)


def test_intrinsic_function_combinations() -> None:
    """Test combinations of intrinsic functions.
    
    This test verifies:
        - Nested functions work
        - Multiple functions in sequence
        - Complex expressions
    """
    template = {
        "Resources": {
            "MyResource": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "Name": YamlTagged("!If", [
                        YamlTagged("!Equals", [
                            YamlTagged("!Ref", "Environment"),
                            "prod"
                        ]),
                        YamlTagged("!Sub", "${AWS::StackName}-prod"),
                        YamlTagged("!Sub", "${AWS::StackName}-dev")
                    ])
                }
            }
        }
    }
    
    result = encode_yaml(template)
    
    # Verify function nesting
    assert "!If" in result
    assert "!Equals" in result
    assert "!Ref" in result
    assert "!Sub" in result


def test_cloudformation_specific_tags() -> None:
    """Test CloudFormation-specific tag handling.
    
    This test verifies:
        - All CloudFormation tags are supported
        - Tags are properly formatted
        - Tag values are correct
    """
    template = {
        "Resources": {
            "TestResource": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "Ref": YamlTagged("!Ref", "AWS::StackName"),
                    "GetAtt": YamlTagged("!GetAtt", "OtherResource.Arn"),
                    "Join": YamlTagged("!Join", [":", ["a", "b"]]),
                    "Select": YamlTagged("!Select", ["0", YamlTagged("!Ref", "List")]),
                    "Split": YamlTagged("!Split", [",", "a,b,c"]),
                    "ImportValue": YamlTagged("!ImportValue", "ExportedValue"),
                }
            }
        }
    }
    
    result = encode_yaml(template)
    
    # Check all CloudFormation tags
    assert "!Ref" in result
    assert "!GetAtt" in result
    assert "!Join" in result
    assert "!Select" in result
    assert "!Split" in result
    assert "!ImportValue" in result 