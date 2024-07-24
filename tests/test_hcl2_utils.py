import pytest

from extended_data_types.hcl2_utils import decode_hcl2, encode_hcl2


@pytest.fixture()
def hcl2_data():
    return """
    resource "aws_s3_bucket" "b" {
      bucket = "my-tf-test-bucket"
      acl    = "private"

      tags = {
        Name        = "My bucket"
        Environment = "Dev"
      }
    }
    """


@pytest.fixture()
def expected_output():
    return {
        "resource": [
            {
                "aws_s3_bucket": {
                    "b": {
                        "bucket": "my-tf-test-bucket",
                        "acl": "private",
                        "tags": {"Name": "My bucket", "Environment": "Dev"},
                    },
                },
            },
        ],
    }


def test_decode_hcl2_valid(hcl2_data, expected_output):
    result = decode_hcl2(hcl2_data)
    assert result == expected_output


def test_decode_hcl2_empty():
    hcl2_data = ""
    expected_output = {}
    result = decode_hcl2(hcl2_data)
    assert result == expected_output


def test_decode_hcl2_invalid():
    hcl2_data = "invalid hcl2 data"
    with pytest.raises(ValueError, match="Invalid HCL2 data:"):
        decode_hcl2(hcl2_data)


def test_encode_hcl2():
    data = {
        "resource": [
            {
                "aws_s3_bucket": {
                    "b": {
                        "bucket": "my-tf-test-bucket",
                        "acl": "private",
                        "tags": {"Name": "My bucket", "Environment": "Dev"},
                    },
                },
            },
        ],
    }
    expected_hcl2 = """{
  "resource" = [
    {
      "aws_s3_bucket" = {
        "b" = {
          "bucket" = "my-tf-test-bucket",
          "acl" = "private",
          "tags" = {
            "Name" = "My bucket",
            "Environment" = "Dev"
          }
        }
      }
    }
  ]
}"""
    result = encode_hcl2(data)
    assert result == expected_hcl2
