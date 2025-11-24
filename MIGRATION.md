# Migration Guide: v5.x → v6.0

This guide helps you migrate from Extended Data Types v5.x to v6.0.

## Breaking Changes

### Python Version Requirement
- **v5.x**: Python >=3.9
- **v6.0**: Python >=3.10

**Action Required**: Upgrade to Python 3.10 or later.

### YAML Library Change
- **v5.x**: PyYAML
- **v6.0**: ruamel.yaml

**Impact**: 
- YAML output formatting may differ slightly
- Comments and formatting are now preserved in round-trip operations
- Custom YAML tags need migration (see below)

**Action Required**: Test your YAML serialization to ensure output compatibility.

### Architecture Changes

#### New Modular Structure
v6.0 introduces a new modular architecture while maintaining backward compatibility:

```
extended_data_types/
├── core/              # Enhanced collection types
├── serialization/     # Format handling (JSON, YAML, TOML, HCL2, etc.)
├── transformations/   # Data transformation pipelines  
├── inspection/        # Type introspection
├── matching/          # Pattern matching
├── io/                # File operations
└── compat/            # v5 compatibility layer
```

#### Dual API Design
v6.0 maintains **full backward compatibility** through a dual API:

**Legacy API (v5)** - Still works!
```python
from extended_data_types import decode_json, encode_yaml, flatten_map
```

**Modern API (v6)** - Recommended for new code
```python
from extended_data_types import ExtendedDict, get_serializer
from extended_data_types.serialization import serialize, deserialize
```

## Migration Paths

### Option 1: No Changes Required (Recommended)
The v5 API is fully supported via the compatibility layer. Your existing code should work without modifications:

```python
# v5 code - still works in v6!
from extended_data_types import decode_json, encode_json, flatten_map

data = decode_json('{"key": "value"}')
result = flatten_map({"a": {"b": 1}})
```

### Option 2: Gradual Migration
Migrate to the new API incrementally:

**Before (v5)**:
```python
from extended_data_types import decode_json, encode_yaml

data = decode_json(json_string)
yaml_string = encode_yaml(data)
```

**After (v6)**:
```python
from extended_data_types.serialization import deserialize, serialize

data = deserialize(json_string, 'json')
yaml_string = serialize(data, 'yaml')
```

### Option 3: Full Migration
Use the new object-oriented API for maximum features:

```python
from extended_data_types import ExtendedDict
from extended_data_types.serialization import serialize

# Enhanced collections with transformation methods
data = ExtendedDict({"user": {"name": "John", "age": 30}})
data = data.flatten()

# Unified serialization
output = serialize(data, 'yaml')
```

## Specific Migration Cases

### 1. Type Conversion

**Before (v5)**:
```python
from extended_data_types import convert_special_type, strtoint

result = convert_special_type(value, int)
num = strtoint("42")
```

**After (v6)** - Still works, or use new API:
```python
from extended_data_types.core.types import TypeSystem

system = TypeSystem()
result = system.convert_value(value, int)
```

### 2. File Operations

**Before (v5)**:
```python
from extended_data_types import get_parent_repository

repo = get_parent_repository("/path/to/file")
```

**After (v6)** - Still works, or use new module:
```python
from extended_data_types.io.git import get_parent_repository

repo = get_parent_repository("/path/to/file")
```

### 3. HCL2 Support (NEW in v6)

v6.0 adds full HCL2 (Terraform) support:

```python
from extended_data_types.serialization import serialize, deserialize

# Parse HCL2
terraform_config = deserialize(hcl2_string, 'hcl2')

# Generate HCL2
hcl2_output = serialize(config_dict, 'hcl2')
```

### 4. CLI Tool (NEW in v6)

v6.0 includes a command-line tool:

```bash
# Convert between formats
edt convert input.json --to yaml

# Validate data files
edt validate data.yaml

# Format HCL2 files
edt hcl2 format terraform.tf
```

## Dependency Changes

### Removed
- None (all v5 dependencies retained for compatibility)

### Added
- `ruamel.yaml` (replaces PyYAML for better round-trip support)
- `python-hcl2` (for Terraform configuration support)
- `babel`, `num2words`, `roman` (for transformation features)
- `pydantic`, `attrs`, `cattrs` (for type validation)

### Changed
- `pyyaml` → Still included for compatibility, but `ruamel.yaml` is preferred

## Testing Your Migration

### 1. Run Your Test Suite
```bash
pytest tests/
```

### 2. Check for Deprecation Warnings
```python
import warnings
warnings.simplefilter('always', DeprecationWarning)

# Run your code
```

### 3. Verify Serialization Output
Compare serialization output before and after upgrade:

```python
import extended_data_types as edt

data = {"test": "data"}
result_v5 = edt.encode_yaml(data)  # v5 way
result_v6 = edt.encode_yaml(data)  # Still works!

assert result_v5 == result_v6  # Should match
```

## Troubleshooting

### Issue: Import Errors
**Problem**: `ImportError: cannot import name 'X'`

**Solution**: Check if you're importing from the correct module:
```python
# Old location (may have moved)
from extended_data_types import some_function

# Try new location
from extended_data_types.compat import some_function
```

### Issue: YAML Formatting Differences
**Problem**: YAML output format changed

**Solution**: This is expected due to ruamel.yaml. The YAML is still valid but may have different formatting (spacing, quotes, etc.). If you need exact formatting, use serialization options:

```python
from extended_data_types import encode_yaml

result = encode_yaml(data, default_flow_style=False)
```

### Issue: Type Errors
**Problem**: mypy or type checkers report new errors

**Solution**: v6.0 has stricter type annotations. Update your type hints:
```python
# Before
def process(data: dict) -> dict:
    pass

# After  
def process(data: dict[str, Any]) -> dict[str, Any]:
    pass
```

## Getting Help

- **Documentation**: https://jbcom.github.io/extended-data-types/
- **Issues**: https://github.com/jbcom/extended-data-types/issues
- **Changelog**: See CHANGELOG.md for detailed changes

## Timeline

- **v5.x**: Supported, receives bug fixes
- **v6.0**: Current release, fully backward compatible
- **v7.0**: Future release (v5 API may be deprecated)

**Recommendation**: Migrate gradually. Test thoroughly. The v5 API will be supported for the foreseeable future.
