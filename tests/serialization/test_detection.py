"""Tests for serialization format detection."""

from __future__ import annotations

import pytest

from extended_data_types.serialization.detection import (
    guess_format, is_potential_hcl2, is_potential_ini, is_potential_json,
    is_potential_querystring, is_potential_toml, is_potential_xml,
    is_potential_yaml)


def test_is_potential_json():
    """Test JSON format detection."""
    assert is_potential_json('{"key": "value"}')
    assert is_potential_json('[1, 2, 3]')
    assert is_potential_json('{}')
    assert is_potential_json('[]')
    
    # Should not detect other formats
    assert not is_potential_json('key: value')
    assert not is_potential_json('[section]\nkey=value')
    assert not is_potential_json('plain text')

def test_is_potential_yaml():
    """Test YAML format detection."""
    assert is_potential_yaml('key: value')
    assert is_potential_yaml('- list item')
    assert is_potential_yaml('---\nkey: value')
    assert is_potential_yaml('&anchor value')
    assert is_potential_yaml('*reference')
    
    # Should not detect other formats
    assert not is_potential_yaml('{"key": "value"}')
    assert not is_potential_yaml('plain text')

def test_is_potential_toml():
    """Test TOML format detection."""
    assert is_potential_toml('[section]\nkey = "value"')
    assert is_potential_toml('key = "value"')
    assert is_potential_toml('"""multiline\nstring"""')
    
    # Should not detect other formats
    assert not is_potential_toml('{"key": "value"}')
    assert not is_potential_toml('key: value')
    assert not is_potential_toml('plain text')

def test_is_potential_xml():
    """Test XML format detection."""
    assert is_potential_xml('<?xml version="1.0"?>')
    assert is_potential_xml('<!DOCTYPE html>')
    assert is_potential_xml('<root><child>value</child></root>')
    assert is_potential_xml('<![CDATA[content]]>')
    
    # Should not detect other formats
    assert not is_potential_xml('{"key": "value"}')
    assert not is_potential_xml('key: value')
    assert not is_potential_xml('plain text')

def test_is_potential_ini():
    """Test INI format detection."""
    assert is_potential_ini('[section]\nkey=value')
    assert is_potential_ini('key=value')
    assert is_potential_ini('[database]\nhost=localhost')
    
    # Should not detect other formats
    assert not is_potential_ini('{"key": "value"}')
    assert not is_potential_ini('key: value')
    assert not is_potential_ini('plain text')

def test_is_potential_querystring():
    """Test query string format detection."""
    assert is_potential_querystring('key1=value1&key2=value2')
    assert is_potential_querystring('key=value')
    assert is_potential_querystring('a=1&b=2&c=3')
    
    # Should not detect other formats
    assert not is_potential_querystring('{"key": "value"}')
    assert not is_potential_querystring('key: value')
    assert not is_potential_querystring('key = value')
    assert not is_potential_querystring('plain text')

def test_is_potential_hcl2():
    """Test HCL2 format detection."""
    # Test block declarations
    assert is_potential_hcl2('resource "aws_instance" "example" {}')
    assert is_potential_hcl2('variable "region" {}')
    assert is_potential_hcl2('provider "aws" {}')
    assert is_potential_hcl2('module "vpc" {}')
    assert is_potential_hcl2('data "aws_ami" "ubuntu" {}')
    assert is_potential_hcl2('locals { count = 1 }')
    assert is_potential_hcl2('terraform { required_version = ">= 1.0" }')
    
    # Test attribute assignments
    assert is_potential_hcl2('''
        resource "aws_instance" "example" {
          ami = "abc123"
          instance_type = "t2.micro"
        }
    ''')
    
    # Test heredoc syntax
    assert is_potential_hcl2('''
        variable "script" {
          default = <<-EOF
            #!/bin/bash
            echo "Hello"
          EOF
        }
    ''')
    
    # Test dynamic blocks
    assert is_potential_hcl2('''
        dynamic "setting" {
          for_each = var.settings
          content {
            name  = setting.key
            value = setting.value
          }
        }
    ''')
    
    # Test for expressions
    assert is_potential_hcl2('''
        locals {
          instance_ids = [for inst in aws_instance.example : inst.id]
        }
    ''')
    
    # Should not detect other formats
    assert not is_potential_hcl2('{"key": "value"}')  # JSON
    assert not is_potential_hcl2('key: value')        # YAML
    assert not is_potential_hcl2('[section]\nkey=value')  # INI
    assert not is_potential_hcl2('plain text')
    
    # Test edge cases
    assert is_potential_hcl2('''
        resource "complex_type" "example" {
          nested_block {
            key = "value"
          }
          list = [
            "item1",
            "item2"
          ]
          map = {
            key1 = "value1"
            key2 = "value2"
          }
        }
    ''')

def test_guess_format():
    """Test format guessing."""
    assert guess_format('{"key": "value"}') == 'json'
    assert guess_format('[1, 2, 3]') == 'json'
    assert guess_format('key: value') == 'yaml'
    assert guess_format('---\nkey: value') == 'yaml'
    assert guess_format('[section]\nkey = "value"') == 'toml'
    assert guess_format('<?xml version="1.0"?>') == 'xml'
    assert guess_format('[section]\nkey=value') == 'ini'
    assert guess_format('key1=value1&key2=value2') == 'querystring'
    assert guess_format('plain text') == 'unknown'

    # Test edge cases
    assert guess_format('') == 'unknown'
    assert guess_format(' ') == 'unknown'

def test_guess_format_with_hcl2():
    """Test format guessing including HCL2."""
    # Test HCL2 detection
    assert guess_format('resource "aws_instance" "example" {}') == 'hcl2'
    assert guess_format('variable "region" {}') == 'hcl2'
    assert guess_format('''
        provider "aws" {
          region = "us-west-2"
        }
    ''') == 'hcl2'
    
    # Test format priority (HCL2 vs other formats)
    assert guess_format('{"type": "json"}') == 'json'  # JSON takes precedence
    assert guess_format('''
        resource "test" "example" {
          key = "value"
        }
    ''') == 'hcl2'  # HCL2 before YAML
    
    # Test complex HCL2 content
    assert guess_format('''
        module "vpc" {
          source = "terraform-aws-modules/vpc/aws"
          version = "3.0.0"
          
          name = "my-vpc"
          cidr = "10.0.0.0/16"
          
          azs             = ["us-west-2a", "us-west-2b", "us-west-2c"]
          private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
          public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
          
          enable_nat_gateway = true
          single_nat_gateway = true
          
          tags = {
            Environment = "dev"
            Project     = "my-project"
          }
        }
    ''') == 'hcl2'

def test_guess_format_comprehensive():
    """Test format guessing for all supported formats."""
    # Test all formats in one test function
    assert guess_format('{"key": "value"}') == 'json'
    assert guess_format('key: value') == 'yaml'
    assert guess_format('[section]\nkey = "value"') == 'toml'
    assert guess_format('<?xml version="1.0"?>') == 'xml'
    assert guess_format('[section]\nkey=value') == 'ini'
    assert guess_format('key1=value1&key2=value2') == 'querystring'
    assert guess_format('resource "test" "example" {}') == 'hcl2'
    assert guess_format('plain text') == 'unknown'
    
    # Test empty or whitespace content
    assert guess_format('') == 'unknown'
    assert guess_format(' ') == 'unknown'
    assert guess_format('\n') == 'unknown' 