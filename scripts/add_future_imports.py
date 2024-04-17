import os
from pathlib import Path

# Define the future imports to be added
FUTURE_IMPORTS = [
    "from __future__ import annotations, division, print_function, unicode_literals"
]


def add_future_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    imports_added = False
    for future_import in FUTURE_IMPORTS:
        if not any(future_import in line for line in lines):
            lines.insert(0, future_import + '\n')
            imports_added = True

    if imports_added:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        print(f"Added future imports to {file_path}")


def main():
    # Find all Python files in extended_data_types and tests directories
    directories = ['extended_data_types', 'tests']
    for directory in directories:
        for py_file in Path(directory).rglob('*.py'):
            add_future_imports(py_file)

    print("Future imports added successfully.")


if __name__ == "__main__":
    main()
