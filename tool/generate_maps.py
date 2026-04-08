#!/usr/bin/env python3
"""
Generate Dart scheme data from TOML files.
This script reads the common_maps TOML files and generates Dart code.
"""

import os
import toml
import json
from pathlib import Path

COMMON_MAPS_DIR = Path(__file__).parent.parent
OUTPUT_DIR = Path(__file__).parent.parent / "lib" / "src" / "maps"


def load_toml_file(filepath):
    """Load a TOML file and return its contents."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return toml.load(f)


def get_devanagari_vowel_to_mark_map():
    """Load the devanagari vowel to marks map."""
    filepath = COMMON_MAPS_DIR / "_devanagari_vowel_to_marks.toml"
    return load_toml_file(filepath)


def get_all_schemes():
    """Load all scheme TOML files."""
    schemes = {}
    
    # Load Roman schemes
    roman_dir = COMMON_MAPS_DIR / "roman"
    if roman_dir.exists():
        for f in roman_dir.glob("*.toml"):
            name = f.stem
            schemes[name] = {'data': load_toml_file(f), 'type': 'roman'}
    
    # Load Brahmic schemes
    brahmic_dir = COMMON_MAPS_DIR / "brahmic"
    if brahmic_dir.exists():
        for f in brahmic_dir.glob("*.toml"):
            name = f.stem
            schemes[name] = {'data': load_toml_file(f), 'type': 'brahmic'}
    
    return schemes


def to_dart_map(data, indent=2, depth=0):
    """Convert a Python dict to Dart map syntax."""
    spaces = ' ' * (indent * depth)
    if not data:
        return '{}'
    
    lines = ['{']
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f'{spaces}  "{escape_dart_string(key)}": {to_dart_map(value, indent, depth + 1)},')
        elif isinstance(value, list):
            list_str = '[' + ', '.join([f'"{escape_dart_string(v)}"' for v in value]) + ']'
            lines.append(f'{spaces}  "{escape_dart_string(key)}": {list_str},')
        else:
            lines.append(f'{spaces}  "{escape_dart_string(key)}": "{escape_dart_string(value)}",')
    lines.append(spaces + '}')
    return '\n'.join(lines)


def escape_dart_string(s):
    """Escape special characters for Dart strings."""
    if s is None:
        return ''
    return str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t').replace('$', r'\$')


def generate_dart_schemes():
    """Generate the Dart schemes file."""
    dev_vowel_map = get_devanagari_vowel_to_mark_map()
    schemes = get_all_schemes()
    
    output = '''// Auto-generated file. Do not edit manually.
// Generated from common_maps TOML files.

library;

final devVowelToMarkMap = ''' + to_dart_map(dev_vowel_map) + ''';

final schemesData = <String, Map<String, dynamic>>{};
final schemeTypes = <String, bool>{};

void initSchemesData() {
'''    
    for name, scheme_info in schemes.items():
        data = scheme_info['data']
        scheme_type = scheme_info['type']
        
        output += f'  schemesData["{name}"] = {to_dart_map(data)};\n'
        output += f'  schemeTypes["{name}"] = {str(scheme_type == "roman").lower()};\n'
    
    output += '}\n'
    output += '\nvoid initializeAll() {\n  initSchemesData();\n}\n'
    
    return output


def main():
    """Main entry point."""
    print("Generating Dart schemes data...")
    
    output = generate_dart_schemes()
    
    output_file = OUTPUT_DIR / "schemes.dart"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"Generated {output_file}")


if __name__ == '__main__':
    main()