# AI Agent Guidelines for extended-data-types

This document provides critical context for AI coding assistants (Cursor, Codex, Copilot, Gemini, etc.) working on this repository.

## 🚨 CRITICAL: CI/CD Workflow Design Philosophy

### Our Simple Automated Release Workflow

**This repository uses CALENDAR VERSIONING with automatic PyPI releases**. Every push to main that passes tests gets released automatically.

### Key Design Decisions (DO NOT SUGGEST CHANGING THESE)

#### 1. **Calendar Versioning (CalVer) - No Manual Version Management**

✅ **How It Works:**
- Version format: `YYYY.MM.BUILD_NUMBER` (with zero-padded month)
- Example: `2025.01.42` for January, `2025.11.42` for November
- Version is auto-generated using GitHub run number
- Script: `.github/scripts/set_version.py`

❌ **INCORRECT Agent Suggestion:**
> "You should manually manage versions in __init__.py"
> "Add semantic-release for version management"
> "Use git tags for versioning"

✅ **CORRECT Understanding:**
- Version is AUTOMATICALLY updated on every main branch push
- No git tags needed or used
- No semantic analysis of commits needed
- No manual version bumps required

#### 2. **Every Push to Main = PyPI Release**

✅ **How It Works:**
```
Push to main branch
  ↓
All tests pass
  ↓
Auto-generate version (YYYY.MM.BUILD)
  ↓
Build signed package
  ↓
Publish to PyPI
  ↓
DONE
```

❌ **INCORRECT Agent Suggestion:**
> "Only release when version changes"
> "Check if release is needed before publishing"
> "Use conditional logic to skip releases"

✅ **CORRECT Understanding:**
- Every main branch push = new release
- No conditionals, no skipping
- Simple, predictable, automatic

#### 3. **No Git Tags, No GitHub Releases**

✅ **What We Do:**
- Publish directly to PyPI
- Version in package metadata only

❌ **What We Don't Do:**
- ❌ Create git tags
- ❌ Create GitHub releases
- ❌ Manage changelog files automatically
- ❌ Commit version changes back to repo

#### 4. **Why This Approach?**

**Problems with semantic-release and tag-based versioning:**
- Complex setup and configuration
- Depends on commit message conventions
- Requires git tags and history analysis
- Can fail or skip releases unexpectedly
- Adds unnecessary complexity

**Benefits of CalVer + Auto-increment:**
- ✅ Dead simple - no configuration needed
- ✅ Always works - no analysis, no skipping
- ✅ Predictable - every push = new version
- ✅ No git pollution - no tags, no bot commits
- ✅ Build number always increments

### The Complete Workflow

```yaml
On Push to main:
  ↓
1. Build & verify package ✓
  ↓
2. Run tests across all Python versions ✓
  ↓
3. Type checking with pyright ✓
  ↓
4. Linting with pre-commit ✓
  ↓
5. Generate coverage report ✓
  ↓
6. Auto-increment version (YYYY.MM.BUILD) ✓
  ↓
7. Build signed attestation ✓
  ↓
8. Publish to PyPI ✓
```

### What This Workflow DOES NOT Do

❌ Analyze commit messages
❌ Create git tags
❌ Create GitHub releases
❌ Skip releases based on conditions
❌ Require manual version management
❌ Depend on git history or tags

## 📝 Making Code Changes

### When Reviewing PRs

**DO:**
- ✅ Review code quality and correctness
- ✅ Check test coverage
- ✅ Verify type hints
- ✅ Suggest API improvements
- ✅ Check for security issues

**DO NOT:**
- ❌ Suggest adding semantic-release
- ❌ Recommend manual version management
- ❌ Suggest git tag-based versioning
- ❌ Recommend complex release workflows
- ❌ Flag the simple auto-versioning as "incorrect"

### Understanding Version Management

```
GitHub Action Starts
   ↓
Run Number: 42 (GitHub auto-increments)
   ↓
Script generates: 2025.01.42 (for January)
   ↓
Updates __init__.py: __version__ = "2025.01.42"
   ↓
Package built with that version
   ↓
Published to PyPI
```

**Version is:**
- ✅ Generated automatically
- ✅ Based on date + GitHub run number
- ✅ Always incrementing
- ✅ Written to __init__.py during build
- ❌ NOT committed back to git
- ❌ NOT based on git tags

### Commit Message Format

**You can use any commit format you want.** We don't analyze commits for versioning.

Recommendations:
- Write clear, descriptive commits
- Explain what and why
- No specific format required

## 🔧 Development Workflow

### Local Development

```bash
# Install dependencies
pip install -e ".[tests,typing,docs]"

# Run tests
pytest

# Run type checking
mypy src/

# Run linting
pre-commit run --all-files
```

### Creating PRs

1. Create a feature branch
2. Make your changes
3. Run tests locally
4. Create PR against `main`
5. CI will run automatically
6. Merge to main when approved

### Releases (Fully Automated)

When PR is merged to main:
1. CI runs all checks
2. Auto-generates version: `YYYY.MM.BUILD`
3. Builds signed package
4. Publishes to PyPI
5. **DONE - that's it**

No manual steps, no tags, no conditionals, no complexity.

## 🎯 Common Agent Misconceptions

### Misconception #1: "Missing version management"

**Agent says:** "You need to manually update __version__ before releases"

**Reality:** Version is auto-generated on every main branch push. Manual management not needed.

### Misconception #2: "Should use semantic versioning"

**Agent says:** "Consider using semantic-release or conventional commits"

**Reality:** We intentionally use CalVer for simplicity. Every push gets a new version.

### Misconception #3: "Need git tags"

**Agent says:** "Add git tags for release tracking"

**Reality:** PyPI version history is our source of truth. No git tags needed.

### Misconception #4: "CalVer is wrong for libraries"

**Agent says:** "Libraries should use SemVer"

**Reality:** CalVer works fine. Users pin versions anyway. Simplicity > convention.

### Misconception #5: "Missing release conditions"

**Agent says:** "You should only release when changes are made"

**Reality:** Every main push is intentional. If it's merged, it should be released.

## 📚 Design Rationale

This workflow was created to solve real problems:

**Problems We Solved:**
- ✅ No more failed releases due to missing tags
- ✅ No more version conflicts
- ✅ No more "why didn't it release?" debugging
- ✅ No more complex semantic-release configuration
- ✅ No more dependency on git history analysis

**Benefits We Gained:**
- ✅ Predictable: every main push = release
- ✅ Simple: ~70 lines of Python for versioning
- ✅ Reliable: no conditional logic to fail
- ✅ Fast: no git history analysis
- ✅ Clean: no bot commits or tags

## 🤝 Getting Help

If you're an AI agent uncertain about a suggestion:
1. Check this document first
2. If it involves versioning or releases, DON'T suggest changes
3. Focus on code quality, tests, and documentation
4. Trust that the release workflow is intentionally simple

---

**Last Updated:** 2025-11-24
**Versioning:** CalVer (YYYY.MM.BUILD) via GitHub run number
