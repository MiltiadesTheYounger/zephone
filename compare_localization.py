#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import sys

def extract_entries(filepath):
    """Extract all entry names from an XML file"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        entries = {}
        for entry in root.findall('.//entry'):
            name = entry.get('name')
            value = entry.get('value', '')
            if name:
                entries[name] = value
        return entries
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return {}

def compare_files(russian_file, ukrainian_file, filename):
    """Compare two localization files and find missing entries"""
    rus_entries = extract_entries(russian_file)
    ukr_entries = extract_entries(ukrainian_file)

    rus_keys = set(rus_entries.keys())
    ukr_keys = set(ukr_entries.keys())

    missing = rus_keys - ukr_keys

    return {
        'filename': filename,
        'total_russian': len(rus_keys),
        'total_ukrainian': len(ukr_keys),
        'missing_count': len(missing),
        'missing_entries': sorted(missing),
        'missing_with_values': {k: rus_entries[k] for k in sorted(missing)}
    }

def main():
    base_path = r"c:\Users\kirav\Desktop\Zephon Coding\zephone\ModData\Data\Core\Languages"
    russian_path = os.path.join(base_path, "Russian")
    ukrainian_path = os.path.join(base_path, "Ukrainian")

    files_to_check = [
        'Credits.xml', 'Diplomacy.xml', 'Effects.xml',
        'Factions.xml', 'GUI.xml', 'Items.xml',
        'Modifiers.xml', 'Notifications.xml', 'Objectives.xml',
        'Regions.xml', 'Settings.xml', 'Tips.xml',
        'Titles.xml', 'Traits.xml', 'Units.xml',
        'Upgrades.xml', 'Weapons.xml', 'WorldParameters.xml'
    ]

    results = []
    total_missing = 0

    for filename in files_to_check:
        rus_file = os.path.join(russian_path, filename)
        ukr_file = os.path.join(ukrainian_path, filename)

        if os.path.exists(rus_file) and os.path.exists(ukr_file):
            result = compare_files(rus_file, ukr_file, filename)
            results.append(result)
            total_missing += result['missing_count']

    # Print summary
    print("=" * 80)
    print("UKRAINIAN LOCALIZATION - MISSING ENTRIES REPORT")
    print("=" * 80)
    print()
    print(f"Total files checked: {len(results)}")
    print(f"Total missing entries across all files: {total_missing}")
    print()
    print("=" * 80)
    print("SUMMARY BY FILE")
    print("=" * 80)
    print()

    files_with_missing = []
    files_complete = []

    for result in results:
        if result['missing_count'] > 0:
            files_with_missing.append(result)
            print(f"FILE: {result['filename']}")
            print(f"  Russian entries: {result['total_russian']}")
            print(f"  Ukrainian entries: {result['total_ukrainian']}")
            print(f"  Missing: {result['missing_count']}")
            print()
        else:
            files_complete.append(result['filename'])

    if files_complete:
        print("Files with NO missing entries:")
        for fname in files_complete:
            print(f"  ✓ {fname}")
        print()

    print("=" * 80)
    print("DETAILED MISSING ENTRIES")
    print("=" * 80)
    print()

    for result in files_with_missing:
        print(f"\n{'=' * 80}")
        print(f"FILE: {result['filename']} ({result['missing_count']} missing entries)")
        print('=' * 80)

        if result['missing_count'] < 20:
            # Show all missing entries with Russian values
            for entry_name in result['missing_entries']:
                rus_value = result['missing_with_values'][entry_name]
                print(f"\nEntry: {entry_name}")
                print(f"Russian value: {rus_value}")
        else:
            # Just show entry names for files with 20+ missing
            print(f"\n(Too many to list individually - showing first 10)")
            for entry_name in result['missing_entries'][:10]:
                rus_value = result['missing_with_values'][entry_name]
                print(f"\nEntry: {entry_name}")
                print(f"Russian value: {rus_value}")
            print(f"\n... and {result['missing_count'] - 10} more entries")

if __name__ == '__main__':
    main()
