#!/usr/bin/env python3
"""
Kiểm tra inline schema trong paths/
Inline schema = có 'type: object' hoặc 'type: array' mà không có '$ref'
"""

import sys
import yaml
from pathlib import Path

def check_schema(schema, path=""):
    """
    Kiểm tra xem schema có phải inline không
    Returns: (is_inline, error_message)
    """
    if not isinstance(schema, dict):
        return False, None

    # Nếu có $ref → OK
    if '$ref' in schema:
        return False, None

    # Nếu có type: object hoặc type: array → INLINE SCHEMA
    schema_type = schema.get('type')
    if schema_type in ['object', 'array']:
        return True, f"Found inline schema with type: {schema_type} at {path}"

    return False, None

def check_file(file_path):
    """
    Kiểm tra 1 file YAML
    Returns: list of errors
    """
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            return errors

        # Check tất cả operations (get, post, put, patch, delete, etc.)
        for method, operation in data.items():
            if not isinstance(operation, dict):
                continue

            # Check requestBody
            if 'requestBody' in operation:
                content = operation['requestBody'].get('content', {})
                for media_type, media_data in content.items():
                    if 'schema' in media_data:
                        is_inline, msg = check_schema(
                            media_data['schema'],
                            f"{method}.requestBody.content.{media_type}.schema"
                        )
                        if is_inline:
                            errors.append(msg)

            # Check responses
            if 'responses' in operation:
                for status_code, response in operation['responses'].items():
                    if not isinstance(response, dict):
                        continue
                    content = response.get('content', {})
                    for media_type, media_data in content.items():
                        if 'schema' in media_data:
                            is_inline, msg = check_schema(
                                media_data['schema'],
                                f"{method}.responses.{status_code}.content.{media_type}.schema"
                            )
                            if is_inline:
                                errors.append(msg)

    except Exception as e:
        errors.append(f"Error parsing file: {e}")

    return errors

def main():
    """Main function"""
    paths_dir = Path('paths')

    if not paths_dir.exists():
        print("❌ paths/ directory not found")
        sys.exit(1)

    print("🔍 Checking for inline schemas in paths/...")
    print()

    all_errors = []

    # Tìm tất cả file yaml trong paths/
    for yaml_file in paths_dir.rglob('*.yaml'):
        print(f"Checking {yaml_file}...")
        errors = check_file(yaml_file)

        if errors:
            print(f"  ❌ INLINE SCHEMA FOUND:")
            for error in errors:
                print(f"     - {error}")
                all_errors.append(f"{yaml_file}: {error}")
        else:
            print(f"  ✅ OK")

    print()

    if all_errors:
        print("❌ Found inline schemas in paths/")
        print()
        print("Errors:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ No inline schemas in paths/")
        sys.exit(0)

if __name__ == '__main__':
    main()
