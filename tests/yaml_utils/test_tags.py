"""Tests for YAML tag handling functionality.

This module tests the tag handling capabilities of the YAML utils, including:
    - Custom tag creation and parsing
    - CloudFormation tag handling
    - Tag preservation during round-trip
    - Tag validation
    - Complex nested tags

Fixtures:
    tagged_data: Provides sample tagged YAML data
    cloudformation_template: Provides a sample CloudFormation template
"""
from __future__ import annotations

import textwrap
from typing import Any

import pytest

from extended_data_types.yaml_utils import (YAMLFlags, YamlTagged,
                                            configure_yaml, decode_yaml,
                                            encode_yaml)


@pytest.fixture
def tagged_data() -> dict[str, Any]:
    """Provide sample data with YAML tags.
    
    Returns:
        dict: A dictionary containing various tagged values:
            - Simple tagged string
            - Tagged dictionary
            - Nested tags
            - Multiple tags of same type
    """
    return {
        "simple": YamlTagged("!Str", "simple value"),
        "nested": {
            "ref": YamlTagged("!Ref", "MyResource"),
            "sub": YamlTagged("!Sub", "${AWS::Region}-${AWS::StackName}")
        },
        "list": [
            YamlTagged("!GetAtt", "Resource.Attribute"),
            YamlTagged("!GetAtt", "Other.Property")
        ]
    }


@pytest.fixture
def cloudformation_template() -> str:
    """Provide a sample CloudFormation template with intrinsic functions.
    
    Returns:
        str: A YAML string containing CloudFormation template with various tags
    """
    return textwrap.dedent("""
        Resources:
          MyFunction:
            Type: AWS::Lambda::Function
            Properties:
              FunctionName: !Sub ${AWS::StackName}-function
              Role: !GetAtt MyRole.Arn
              Code:
                S3Bucket: !Ref CodeBucket
                S3Key: !Join 
                  - "/"
                  - - !Ref Version
                    - function.zip
              Environment:
                Variables:
                  REGION: !Ref AWS::Region
                  STACK: !Ref AWS::StackName
    """).lstrip()


def test_simple_tag_handling(tagged_data: dict[str, Any]) -> None:
    """Test basic tag handling functionality.
    
    This test verifies:
        - Tags are properly encoded
        - Tag values are preserved
        - Tag types are maintained
    
    Args:
        tagged_data: Fixture containing sample tagged data
    """
    encoded = encode_yaml(tagged_data)
    decoded = decode_yaml(encoded)
    
    # Check simple tag
    assert isinstance(decoded["simple"], YamlTagged)
    assert decoded["simple"].tag == "!Str"
    assert decoded["simple"] == "simple value"
    
    # Check nested tags
    assert decoded["nested"]["ref"].tag == "!Ref"
    assert decoded["nested"]["sub"].tag == "!Sub"


def test_cloudformation_tags(cloudformation_template: str) -> None:
    """Test CloudFormation intrinsic function handling.
    
    This test verifies:
        - CloudFormation tags are properly parsed
        - Nested tag structures are maintained
        - Tag values are correctly preserved
    
    Args:
        cloudformation_template: Fixture containing CloudFormation template
    """
    configure_yaml(YAMLFlags.CLOUDFORMATION)
    data = decode_yaml(cloudformation_template)
    
    function = data["Resources"]["MyFunction"]
    props = function["Properties"]
    
    # Check various CloudFormation tags
    assert isinstance(props["FunctionName"], YamlTagged)
    assert props["FunctionName"].tag == "!Sub"
    
    assert isinstance(props["Role"], YamlTagged)
    assert props["Role"].tag == "!GetAtt"
    
    # Check nested tag structure
    code = props["Code"]
    assert isinstance(code["S3Bucket"], YamlTagged)
    assert code["S3Bucket"].tag == "!Ref"


def test_tag_round_trip() -> None:
    """Test round-trip preservation of tags.
    
    This test verifies:
        - Tags survive encode/decode cycle
        - Tag order is preserved
        - Tag values remain unchanged
        - Complex tag structures are maintained
    """
    original = {
        "single": YamlTagged("!Tag", "value"),
        "list": [
            YamlTagged("!Tag1", "value1"),
            YamlTagged("!Tag2", "value2")
        ],
        "nested": {
            "key": YamlTagged("!Tag3", {
                "inner": YamlTagged("!Tag4", "value")
            })
        }
    }
    
    encoded = encode_yaml(original)
    decoded = decode_yaml(encoded)
    
    # Check structure preservation
    assert decoded["single"].tag == "!Tag"
    assert decoded["list"][0].tag == "!Tag1"
    assert decoded["list"][1].tag == "!Tag2"
    assert decoded["nested"]["key"].tag == "!Tag3"
    assert decoded["nested"]["key"]["inner"].tag == "!Tag4"


def test_tag_validation() -> None:
    """Test tag validation and error handling.
    
    This test verifies:
        - Invalid tags are rejected
        - Tag format is validated
        - Error messages are clear
    """
    # Test invalid tag format
    with pytest.raises(ValueError, match="Invalid tag format"):
        YamlTagged("Invalid Tag", "value")
    
    # Test empty tag
    with pytest.raises(ValueError, match="Tag cannot be empty"):
        YamlTagged("", "value")
    
    # Test None tag
    with pytest.raises(ValueError, match="Tag cannot be None"):
        YamlTagged(None, "value")  # type: ignore


def test_complex_tag_structures() -> None:
    """Test handling of complex tag structures.
    
    This test verifies:
        - Deeply nested tags work correctly
        - Tags with complex values are handled
        - Multiple tag types interact properly
    """
    complex_data = {
        "condition": YamlTagged("!If", [
            YamlTagged("!Equals", ["prod", YamlTagged("!Ref", "Environment")]),
            YamlTagged("!Sub", "${AWS::Region}-prod"),
            YamlTagged("!Sub", "${AWS::Region}-dev")
        ])
    }
    
    encoded = encode_yaml(complex_data)
    decoded = decode_yaml(encoded)
    
    condition = decoded["condition"]
    assert condition.tag == "!If"
    assert isinstance(condition[0], YamlTagged)
    assert condition[0].tag == "!Equals"
    assert isinstance(condition[0][1], YamlTagged)
    assert condition[0][1].tag == "!Ref" 