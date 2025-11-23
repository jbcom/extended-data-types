# Release Architecture Documentation

## Overview
This document explains the release process architecture for `extended-data-types` and the rationale behind key design decisions.

## Current Architecture (As of 2025-11-23)

### Single-Workflow, Tag-Only Releases

**File**: `.github/workflows/ci.yml`

**Flow**:
```
1. Developer creates PR
2. PR merged to main
3. CI workflow triggers:
   ├─ build-package (creates "Packages" artifact)
   ├─ tests (all Python versions in parallel)
   ├─ typechecking
   ├─ linting
   ├─ coverage
   └─ [ALL PASS] → release job (main branch only)
       ├─ semantic-release: Calculate version, create tag
       ├─ Create GitHub Release
       └─ Build signed packages ("Packages-signed" artifact)
   └─ publish job (if release occurred)
       └─ Upload to PyPI
```

### Key Configuration

**semantic-release settings** (`.github/workflows/ci.yml`):
```yaml
commit: false      # Don't create version bump commits
tag: true          # Create Git tags
push: false        # Don't push to repository
changelog: false   # Don't create changelog commits
vcs_release: true  # Create GitHub releases
build: false       # Don't build (we use hynek's action)
```

**Build artifacts**:
- `Packages`: Unsigned builds for CI testing
- `Packages-signed`: Signed builds with attestations for PyPI

## Design Decisions

### Decision 1: No Version Bump Commits

**Rationale**:
1. **Branch Protection Conflict**: Main branch has protection rules requiring status checks
   - Version bump commits haven't passed checks yet
   - Attempting to push them gets rejected
   - Creates a catch-22 situation

2. **Double CI Runs**: Version bump commits would trigger CI again
   - Wastes resources
   - Increases release time
   - Creates duplicate test runs

3. **Git Tags as Source of Truth**:
   - Build tools can extract version from git tags
   - PyPI packages are tagged correctly
   - No need to persist version in source files

**Trade-offs**:
- ✅ No branch protection conflicts
- ✅ Single CI run per release
- ✅ Simpler workflow
- ⚠️ Version in `__init__.py` may lag behind latest release
- ⚠️ Local source builds show older version (acceptable)

### Decision 2: Consolidated Workflow

**Before**:
- `ci.yml`: Build, test, lint
- `release.yml`: Triggered by `workflow_run` after CI completes

**After**:
- Single `ci.yml` with conditional release job

**Rationale**:
1. **Simpler**: One workflow to maintain
2. **Faster**: No workflow_run delay
3. **Clearer**: Release happens as part of CI, not separate
4. **Consistent**: All jobs use same checkout SHA

### Decision 3: Separate Signed Artifacts

**Implementation**:
```yaml
- uses: hynek/build-and-inspect-python-package@v2
  with:
    upload-name-suffix: "-signed"
```

**Rationale**:
- CI creates unsigned "Packages" for testing
- Release creates signed "Packages-signed" for PyPI
- Avoids artifact name conflicts
- Clear separation of test vs. production builds

## Version Management

### How Versions Work

1. **Git Tags**: Authoritative version source
   - Created by semantic-release based on commit messages
   - Example: `v5.1.3`

2. **PyPI Packages**: Built from tagged commits
   - Package metadata uses git tag version
   - Correct version appears on PyPI

3. **Source Files**: May lag behind
   - `src/extended_data_types/__init__.py`: `__version__ = "5.1.2"`
   - Latest PyPI: `5.1.3`
   - This is acceptable

### Why Version Lag Is Acceptable

1. **Primary Distribution**: PyPI (has correct version)
2. **Source Builds**: Rare, users typically install from PyPI
3. **Documentation**: Can reference git tags for latest version
4. **Developer Clarity**: git tags always show true version

### If Version Sync Is Required

If in the future we need source file versions to match releases:
1. Could use setuptools_scm to derive version from git at build time
2. Could use a bot with admin privileges to push version bumps
3. Could disable branch protection for bot (not recommended)

## Common Misunderstandings

### "Version bump commits are required"
**False**. Many projects (e.g., Go modules) use tag-only versioning successfully.

### "Changelog should be generated"
**Optional**. GitHub Releases provide changelog functionality. Committing CHANGELOG.md would require pushing to main.

### "Version in source files must match latest release"
**Not necessary**. PyPI packages are versioned correctly from git tags.

### "Need to create PR for version bumps"
**Counterproductive**. Would cause:
- Branch protection issues (original problem)
- Double CI runs (inefficient)
- Additional complexity (unnecessary)

## Troubleshooting

### Release doesn't trigger
- Check commit messages follow conventional commits format
- Ensure push is to `main` branch
- Verify all tests/lint/coverage pass

### Artifact conflicts
- Ensure `upload-name-suffix: "-signed"` is set in release job
- Check both artifacts appear in workflow run

### Wrong version on PyPI
- Verify git tag was created correctly
- Check semantic-release output for version calculation
- Ensure tag follows semver format

## Future Considerations

### If Branch Protection Changes
If branch protection is relaxed or we get bot admin privileges:
- Could re-enable `commit: true` and `push: true`
- Would persist version bumps to repository
- Would eliminate version lag

### If Version Lag Becomes Issue
- Implement setuptools_scm for dynamic versioning
- Use git tags as sole version source at build time
- Eliminates need for version in source files entirely

## References
- Original issue: https://github.com/jbcom/extended-data-types/actions/runs/19615176677
- PR: https://github.com/jbcom/extended-data-types/pull/41
- Semantic Release docs: https://python-semantic-release.readthedocs.io/
- Conventional Commits: https://www.conventionalcommits.org/
