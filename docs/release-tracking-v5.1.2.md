# Release Tracking: v5.1.2

## Release Status Overview

| Item | Status | Details |
|------|--------|---------|
| GitHub Release | ✅ Published | [v5.1.2](https://github.com/jbcom/extended-data-types/releases/tag/v5.1.2) |
| Release Date | ✅ Complete | 2025-11-23 09:44:06 UTC |
| Release Workflow | ✅ Success | [Run #82](https://github.com/jbcom/extended-data-types/actions/runs/19609291398) |
| PyPI Publication | ❌ **Not Published** | Latest on PyPI: v5.1.0 |
| Package Build | ✅ Available | Release assets on GitHub |

## Issue Analysis

### What Happened

The v5.1.2 release was created manually on GitHub using a direct tag and commit, rather than being generated through the automated semantic-release workflow. This caused the following sequence:

1. **Manual Release Creation**: A tag `v5.1.2` was created and pushed to GitHub manually
2. **GitHub Release Created**: Release notes and assets were uploaded to GitHub
3. **Workflow Triggered**: The release workflow was triggered by the CI completion
4. **Semantic Release Skipped**: The semantic-release action detected the existing v5.1.2 tag and determined "No release will be made, 5.1.2 has already been released!"
5. **PyPI Publication Skipped**: Because `released == 'false'`, the PyPI publish job was skipped

### Root Cause

The automated release workflow (`.github/workflows/release.yml`) only publishes to PyPI when:
```yaml
if: needs.release.outputs.released == 'true'
```

Since the semantic-release detected an existing tag, it set `released=false`, which prevented the PyPI publication step from running.

## Release Contents

### Changes in v5.1.2

- ✅ Added missing `ruamel.yaml>=0.18.0` dependency to `pyproject.toml`
- ✅ Updated Python version to 3.12 in configuration
- ✅ Fixed ModuleNotFoundError in export_utils
- ✅ Resolves compatibility issues with downstream packages (lifecyclelogging)

### Release Assets

Available on GitHub:
- `extended_data_types-5.1.2-py3-none-any.whl` (34,205 bytes)
- `extended_data_types-5.1.2.tar.gz` (382,575 bytes)

Both files include cryptographic attestations and SHA256 digests.

## Verification Steps

### ✅ Completed Verifications

1. **GitHub Release Exists**
   ```bash
   curl -s https://api.github.com/repos/jbcom/extended-data-types/releases/tags/v5.1.2 | jq '.name'
   # Output: "v5.1.2"
   ```

2. **Release Workflow Succeeded**
   ```bash
   # Workflow run ID: 19609291398
   # Status: completed
   # Conclusion: success
   ```

3. **Package Version Updated**
   ```bash
   # src/extended_data_types/__init__.py
   __version__ = "5.1.2"
   ```

4. **Dependencies Updated**
   ```bash
   # pyproject.toml includes:
   ruamel.yaml>=0.18.0
   ```

### ❌ Failed Verification

1. **PyPI Publication**
   ```bash
   pip install extended-data-types==5.1.2
   # ERROR: Could not find a version that satisfies the requirement extended-data-types==5.1.2
   
   # Latest available on PyPI:
   pip index versions extended-data-types
   # extended-data-types (5.1.0)
   ```

## Remediation Options

### Option 1: Manual PyPI Publication (Recommended)

Manually publish the v5.1.2 package to PyPI using the release assets:

1. Download the wheel and source distribution from the GitHub release
2. Verify the package integrity using the provided SHA256 digests
3. Use `twine` to upload to PyPI:
   ```bash
   pip install twine
   twine upload extended_data_types-5.1.2*
   ```

### Option 2: Create v5.1.3 Release

Create a new patch release (v5.1.3) through the normal automated workflow:

1. Make a trivial documentation or version bump commit
2. Push to main branch
3. Let CI complete successfully
4. Automated semantic-release will create v5.1.3 and publish to PyPI

### Option 3: Document and Skip

Accept that v5.1.2 is a GitHub-only release:

1. Update CHANGELOG to note PyPI publication status (completed)
2. Create this tracking document (completed)
3. Direct users to install from GitHub if they need v5.1.2 specifically:
   ```bash
   pip install git+https://github.com/jbcom/extended-data-types.git@v5.1.2
   ```

## Current Recommendation

**Option 1 (Manual PyPI Publication)** is recommended because:
- The package has already been built and tested
- The changes fix important dependency issues
- Users expect version parity between GitHub and PyPI
- Avoids creating unnecessary version numbers

## Next Steps for Users

Until v5.1.2 is published to PyPI, users have these options:

1. **Use v5.1.0 from PyPI** (if they don't need the ruamel.yaml fix):
   ```bash
   pip install extended-data-types==5.1.0
   ```

2. **Install v5.1.2 from GitHub**:
   ```bash
   pip install git+https://github.com/jbcom/extended-data-types.git@v5.1.2
   ```

3. **Install directly from the wheel asset**:
   ```bash
   pip install https://github.com/jbcom/extended-data-types/releases/download/v5.1.2/extended_data_types-5.1.2-py3-none-any.whl
   ```

## Documentation Updates

**Completed:**
- Update CHANGELOG.md with v5.1.2 entry
- Create this tracking document

**Not Required:**
- Update README.md installation instructions (no version-specific instructions exist)
- Add note to release notes about PyPI status (already noted in CHANGELOG)

## References

- GitHub Release: https://github.com/jbcom/extended-data-types/releases/tag/v5.1.2
- PyPI Project: https://pypi.org/project/extended-data-types/
- Workflow Run: https://github.com/jbcom/extended-data-types/actions/runs/19609291398
- Release Commit: [`36d88d5`](https://github.com/jbcom/extended-data-types/commit/36d88d5ae260434e2c7feb71fe2a24829244296f)
