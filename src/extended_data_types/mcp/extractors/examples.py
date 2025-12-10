"""Extract usage examples from test files.

This module provides functionality to parse test files and extract
clean, minimal usage examples for functions and classes.
"""

from __future__ import annotations

import ast
import logging

from pathlib import Path
from typing import NamedTuple


logger = logging.getLogger(__name__)

# Constants
MIN_MODULE_PARTS = 2
MAX_EXAMPLES_BUFFER = 10

# Mapping from module names to test file names
TEST_FILE_MAP = {
    "string_transformations": "test_string_transformations.py",
    "type_utils": "test_type_utils.py",
    "file_data_type": "test_file_data_type.py",
    "yaml_utils": "test_yaml_utils.py",
    "json_utils": "test_json_utils.py",
    "map_data_type": "test_map_data_type.py",
    "list_data_type": "test_list_data_type.py",
    "state_utils": "test_state_utils.py",
    "base64_utils": "test_base64_utils.py",
    "toml_utils": "test_toml_utils.py",
    "export_utils": "test_export_utils.py",
    "hcl2_utils": "test_hcl2_utils.py",
    "import_utils": "test_import_utils.py",
    "matcher_utils": "test_matcher_utils.py",
    "splitter_utils": "test_splitter_utils.py",
    "stack_utils": "test_stack_utils.py",
    "string_data_type": "test_string_data_type.py",
    "number_transformations": "test_number_transformations.py",
}


class Example(NamedTuple):
    """A single usage example."""

    code: str
    description: str


class ExampleExtractor:
    """Extracts usage examples from test files."""

    def __init__(self, tests_dir: Path | None = None) -> None:
        """Initialize with tests directory path.

        Args:
            tests_dir: Path to tests directory. If None, defaults to
                       finding tests relative to package.
        """
        if tests_dir is None:
            # Default to finding tests relative to package
            tests_dir = Path(__file__).parents[4] / "tests"
        self.tests_dir = tests_dir

    def extract_examples(
        self, function_name: str, module_name: str, max_examples: int = 5
    ) -> list[Example]:
        """Extract examples for a function from test files.

        Args:
            function_name: Name of the function to find examples for.
            module_name: Module where the function is defined.
            max_examples: Maximum number of examples to return.

        Returns:
            List of Example objects containing code and description.
        """
        # Find the test file for this module
        test_file = self._find_test_file(module_name)
        if not test_file:
            logger.debug("No test file found for module %s", module_name)
            return []

        if not test_file.exists():
            logger.debug("Test file does not exist: %s", test_file)
            return []

        # Parse the test file
        try:
            with test_file.open(encoding="utf-8") as f:
                source_code = f.read()
            tree = ast.parse(source_code)
        except Exception as e:  # noqa: BLE001
            # Broad exception is appropriate for file parsing
            logger.debug("Failed to parse test file %s: %s", test_file, e)
            return []

        # Extract examples from the AST
        examples = self._extract_from_ast(tree, function_name, source_code)

        # Limit number of examples
        return examples[:max_examples]

    def _find_test_file(self, module_name: str) -> Path | None:
        """Find test file for a module.

        Args:
            module_name: Module name (e.g., "string_transformations").

        Returns:
            Path to test file or None if not found.
        """
        # Extract base module name from full module path
        # e.g., "extended_data_types.yaml_utils.utils" -> "yaml_utils"
        if "." in module_name:
            parts = module_name.split(".")
            # Find the last part that's in our map
            for part in reversed(parts):
                if part in TEST_FILE_MAP:
                    module_name = part
                    break
            else:
                # Use the second-to-last part (package name)
                module_name = parts[-2] if len(parts) >= MIN_MODULE_PARTS else parts[-1]

        # Look up test file
        test_filename = TEST_FILE_MAP.get(module_name)
        if not test_filename:
            return None

        return self.tests_dir / test_filename

    def _extract_from_ast(
        self, tree: ast.AST, function_name: str, source_code: str
    ) -> list[Example]:
        """Extract examples from AST.

        Args:
            tree: Parsed AST of test file.
            function_name: Function to find examples for.
            source_code: Original source code for line extraction.

        Returns:
            List of Example objects.
        """
        examples = []
        source_lines = source_code.split("\n")

        # Find all test functions
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            # Only look at test functions
            if not node.name.startswith("test_"):
                continue

            # Check if this test uses our target function
            if not self._uses_function(node, function_name):
                continue

            # Extract simple examples from this test
            test_examples = self._extract_examples_from_test(
                node, function_name, source_lines
            )
            examples.extend(test_examples)

            # Stop if we have enough examples
            if len(examples) >= MAX_EXAMPLES_BUFFER:  # Get extra, we'll filter later
                break

        return examples

    def _uses_function(self, node: ast.FunctionDef, function_name: str) -> bool:
        """Check if a test function uses the target function.

        Args:
            node: Test function AST node.
            function_name: Function to check for.

        Returns:
            True if the test uses the target function.
        """
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                # Check if this is a direct call to our function
                if isinstance(child.func, ast.Name) and child.func.id == function_name:
                    return True
                # Check if this is a method call (e.g., obj.method())
                if (
                    isinstance(child.func, ast.Attribute)
                    and child.func.attr == function_name
                ):
                    return True
        return False

    def _extract_examples_from_test(
        self, node: ast.FunctionDef, function_name: str, source_lines: list[str]
    ) -> list[Example]:
        """Extract examples from a single test function.

        Args:
            node: Test function AST node.
            function_name: Function to extract examples for.
            source_lines: Source code lines for extraction.

        Returns:
            List of Example objects from this test.
        """
        examples = []

        # Get the test function's docstring as description
        docstring = ast.get_docstring(node) or ""
        test_description = docstring.split("\n")[0] if docstring else node.name

        # Look for simple assert statements with direct function calls
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Assert):
                example_code = self._extract_assert_example(
                    stmt, function_name, source_lines
                )
                if example_code:
                    examples.append(
                        Example(code=example_code, description=test_description)
                    )

        return examples

    def _extract_assert_example(
        self, assert_node: ast.Assert, function_name: str, source_lines: list[str]
    ) -> str | None:
        """Extract example code from an assert statement.

        Args:
            assert_node: Assert statement AST node.
            function_name: Function to extract example for.
            source_lines: Source code lines.

        Returns:
            Extracted example code or None.
        """
        # Look for patterns like: assert function(input) == expected
        test = assert_node.test

        # Handle: assert func(args) == value
        if (
            isinstance(test, ast.Compare)
            and len(test.ops) > 0
            and isinstance(test.left, ast.Call)
            and isinstance(test.left.func, ast.Name)
            and test.left.func.id == function_name
            and hasattr(assert_node, "lineno")
        ):
            line_num = assert_node.lineno - 1
            if 0 <= line_num < len(source_lines):
                line = source_lines[line_num].strip()
                # Clean up the assert statement
                return line.removeprefix("assert ")

        # Handle: assert func(args) - for boolean returns
        if (
            isinstance(test, ast.Call)
            and isinstance(test.func, ast.Name)
            and test.func.id == function_name
            and hasattr(assert_node, "lineno")
        ):
            line_num = assert_node.lineno - 1
            if 0 <= line_num < len(source_lines):
                line = source_lines[line_num].strip()
                return line.removeprefix("assert ")

        return None
