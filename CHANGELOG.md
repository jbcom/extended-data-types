Changelog
==========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

<!-- changelog follows -->


Changelog
==========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

<!-- changelog follows -->


## [2.0.0](https://github.com/jbcom/extended-data-types/tree/2.0.0) - 2024-09-05

### BREAKING CHANGE

- Moving forward 3.8 will not be supported as it adds too much complexity maintaining backwards compatibility
      ### Feat

- Adds reconstruction capabilities for converted data and several new type conversions from strings
      - Added TOML support and extended importing and exporting to use it
      - **Scope**: src/extended_data_types/toml_utils.py


## [1.0.3](https://github.com/jbcom/extended-data-types/tree/1.0.3) - 2024-08-28

### Feat

- Added TOML support and extended importing and exporting to use it
      - **Scope**: src/extended_data_types/toml_utils.py

## [1.0.2](https://github.com/jbcom/extended-data-types/tree/1.0.2) - 2024-08-27

### Fix

- base64_decode was not exported in __all__
      - **Scope**: src/extended_data_types/__init__.py

## [1.0.1](https://github.com/jbcom/extended-data-types/tree/1.0.1) - 2024-08-27

### Feat

- Initial commit establishing the extended-data-types project
