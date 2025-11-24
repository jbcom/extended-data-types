Compatibility Strategy
======================

Extended Data Types maintains a **dual-layer architecture** so that existing users can continue to import the legacy `bob` helpers while new consumers build on the modernized modules.

Legacy modules live under `extended_data_types.compat.*`; they are thin wrappers that delegate directly to the canonical implementations in `map_data_type`, `transformations`, `serialization`, and related packages. This keeps the behavior identical while removing duplication and drift between versions.

Key points:

- **Single source of truth**: Most compatibility helpers simply import the modern implementation (`unhump_map`, `flatten_map`, `deduplicate_map`, etc.) and forward arguments without mutating the data.
- **Explicit version awareness**: Consumers can call `extended_data_types.compat.version.check_compatibility(minor)` to gate behavior based on the runtime version, while `extended_data_types.__version__` and the git tags remain authoritative for releases.
- **No hidden dependencies**: The compatibility layer reuses the same dependencies as the rest of the library, so we avoid introducing specialized packages just for backwards compatibility.

API Versioning
--------------

Releases are governed by git tags (`v6.0.0`, etc.) and `hatch` reads the version from `src/extended_data_types/__init__.py`. `semantic-release` runs on the `main` branch to publish packages after CI succeeds. The compatibility layer itself remains stable: wrappers can gain new translation logic without requiring consumers to change their imports.

Upgrade guidance:

1. Prefer the modern API (`extended_data_types.transformations`, `extended_data_types.serialization`, `extended_data_types.core.*`) for all new development.
2. Use the compatibility helpers only when migrating legacy code; they will continue to work because they reuse the modern implementations.
3. If you need to branch logic by version, call `extended_data_types.compat.version.check_compatibility` at runtime instead of hard-coding version strings.

Preparing for v7
-----------------

When we eventually move to v7, the compat layer will remain the bridge: we can keep `extended_data_types.compat` stable while routing its wrappers to the new V7 internals. That means tests focus on the modern modules, migrations stay simple, and users can adopt V7 incrementally without being forced to refactor overnight.
