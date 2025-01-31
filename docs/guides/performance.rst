Performance Optimization Guide
===========================

This guide covers performance optimization strategies for the Extended Data Types package.

Memory Optimization
----------------

Efficient memory usage patterns:

.. code-block:: python

    from extended_data_types import yaml_utils, json_utils
    from typing import Iterator, Any

    # Stream processing for large files
    def process_large_yaml(
        file_path: str,
        chunk_size: int = 1000
    ) -> Iterator[Any]:
        for document in yaml_utils.decode_yaml_stream(file_path):
            yield document

    # Memory-efficient data transformation
    def transform_large_dataset(
        input_path: str,
        output_path: str,
        transform_func
    ):
        with open(output_path, 'w') as out:
            for chunk in process_large_yaml(input_path):
                result = transform_func(chunk)
                json_utils.encode_json(result, out)
                out.write('\n')

Caching Strategies
----------------

Implementing effective caching:

.. code-block:: python

    from functools import lru_cache
    from typing import Any, Dict

    # Cache expensive operations
    @lru_cache(maxsize=1000)
    def expensive_transform(data: str) -> Dict[str, Any]:
        # Complex transformation logic
        return processed_data

    # Custom cache with size limits
    class SizeAwareCache:
        def __init__(self, max_size_bytes: int = 1024 * 1024):
            self.max_size = max_size_bytes
            self.current_size = 0
            self.cache: Dict[str, Any] = {}

        def add(self, key: str, value: Any):
            size = len(str(value).encode())
            if size + self.current_size <= self.max_size:
                self.cache[key] = value
                self.current_size += size

        def get(self, key: str) -> Any:
            return self.cache.get(key)

Parallel Processing
----------------

Utilizing parallel processing:

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    from typing import List, Any

    # Thread pool for I/O-bound operations
    def process_files_parallel(
        files: List[str],
        max_workers: int = 4
    ) -> List[Any]:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(executor.map(process_file, files))

    # Process pool for CPU-bound operations
    def transform_data_parallel(
        items: List[Any],
        max_workers: int = None
    ) -> List[Any]:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            return list(executor.map(transform_item, items))

Profiling and Monitoring
---------------------

Performance monitoring tools:

.. code-block:: python

    import cProfile
    import pstats
    from contextlib import contextmanager
    import time

    @contextmanager
    def profile_section(name: str):
        profiler = cProfile.Profile()
        profiler.enable()
        start_time = time.time()

        try:
            yield
        finally:
            end_time = time.time()
            profiler.disable()
            stats = pstats.Stats(profiler)
            print(f"\nProfile for {name}:")
            print(f"Total time: {end_time - start_time:.2f}s")
            stats.sort_stats('cumulative').print_stats(20)

Best Practices
------------

1. **Memory Management**:

   - Use generators for large datasets
   - Implement streaming where possible
   - Monitor memory usage

2. **Caching**:

   - Cache expensive operations
   - Use appropriate cache sizes
   - Implement cache eviction

3. **Parallel Processing**:

   - Choose appropriate concurrency model
   - Handle errors in parallel code
   - Monitor resource usage

4. **Optimization Strategy**:

   - Profile before optimizing
   - Measure improvements
   - Document performance characteristics
