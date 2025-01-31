Deployment Guide
==============

This guide covers deployment considerations and configuration management for the Extended Data Types package.

Installation
-----------

Different installation methods:

.. code-block:: bash

    # Basic installation
    pip install extended-data-types

    # Development installation
    pip install -e ".[dev]"

    # Production installation with extras
    pip install extended-data-types[yaml,json,toml]

Configuration Management
---------------------

Managing configurations across environments:

.. code-block:: python

    from extended_data_types import yaml_utils
    from pathlib import Path
    from typing import Dict, Any

    class ConfigManager:
        def __init__(
            self,
            config_dir: Path,
            environment: str = "development"
        ):
            self.config_dir = Path(config_dir)
            self.environment = environment
            self.config: Dict[str, Any] = {}
            
            # Load configurations
            self.load_config()
        
        def load_config(self):
            # Load base config
            base_config = self.load_yaml("base.yaml")
            
            # Load environment config
            env_config = self.load_yaml(f"{self.environment}.yaml")
            
            # Merge configurations
            self.config = {**base_config, **env_config}
        
        def load_yaml(self, filename: str) -> Dict[str, Any]:
            path = self.config_dir / filename
            if path.exists():
                with open(path) as f:
                    return yaml_utils.decode_yaml(f)
            return {}
        
        def get(self, key: str, default: Any = None) -> Any:
            return self.config.get(key, default)

Environment Setup
--------------

Setting up different environments:

.. code-block:: python

    import os
    from enum import Enum
    from typing import Optional

    class Environment(Enum):
        DEVELOPMENT = "development"
        STAGING = "staging"
        PRODUCTION = "production"

    class EnvironmentManager:
        def __init__(
            self,
            env: Optional[str] = None
        ):
            self.env = Environment(
                env or os.getenv("APP_ENV", "development")
            )
            
            # Configure based on environment
            self.configure()
        
        def configure(self):
            if self.env == Environment.PRODUCTION:
                self.configure_production()
            elif self.env == Environment.STAGING:
                self.configure_staging()
            else:
                self.configure_development()
        
        def configure_production(self):
            yaml_utils.configure_yaml(
                yaml_utils.YAMLFlags.SAFE_LOAD |
                yaml_utils.YAMLFlags.NO_ALIASES
            )
            # Additional production settings
        
        def configure_staging(self):
            # Staging configuration
            pass
        
        def configure_development(self):
            # Development configuration
            pass

Monitoring and Logging
-------------------

Setting up monitoring:

.. code-block:: python

    import logging
    from typing import Optional
    from datetime import datetime

    class LogManager:
        def __init__(
            self,
            log_file: Optional[str] = None,
            level: int = logging.INFO
        ):
            self.logger = logging.getLogger("extended_data_types")
            self.logger.setLevel(level)
            
            # Add handlers
            if log_file:
                handler = logging.FileHandler(log_file)
            else:
                handler = logging.StreamHandler()
            
            # Set formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        def log_operation(
            self,
            operation: str,
            data: Any,
            start_time: datetime
        ):
            duration = datetime.now() - start_time
            self.logger.info(
                f"Operation: {operation}, "
                f"Duration: {duration.total_seconds():.2f}s, "
                f"Data size: {len(str(data))}"
            )

Best Practices
------------

1. **Installation**:
   
   - Use virtual environments
   - Pin dependencies
   - Document requirements

2. **Configuration**:
   
   - Use environment variables
   - Separate config by environment
   - Validate configurations

3. **Monitoring**:
   
   - Set up proper logging
   - Monitor performance
   - Track errors

4. **Security**:
   
   - Secure sensitive data
   - Use appropriate permissions
   - Follow security best practices 