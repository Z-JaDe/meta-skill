#!/usr/bin/env python3
"""
Validate plugin metadata consistency across extension manifests.
"""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def manifest_entries():
    claude_plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    cursor_plugin_path = ROOT / ".cursor-plugin" / "plugin.json"
    qwen_extension_path = ROOT / "qwen-extension.json"
    claude_marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"

    claude_plugin = load_json(claude_plugin_path)
    cursor_plugin = load_json(cursor_plugin_path)
    qwen_extension = load_json(qwen_extension_path)
    claude_marketplace = load_json(claude_marketplace_path)
    marketplace_plugin = (claude_marketplace.get("plugins") or [{}])[0]

    return {
        "claude-plugin/plugin.json": claude_plugin,
        "cursor-plugin/plugin.json": cursor_plugin,
        "qwen-extension.json": qwen_extension,
        "claude-plugin/marketplace.json.plugins[0]": marketplace_plugin,
    }


def check_marketplace_shape(marketplace: dict, errors: list):
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("`.claude-plugin/marketplace.json` must contain a non-empty `plugins` array.")
        return

    plugin = plugins[0]
    if marketplace.get("description") != plugin.get("description"):
        errors.append(
            "Description mismatch: `.claude-plugin/marketplace.json.description` "
            "!= `.claude-plugin/marketplace.json.plugins[0].description`."
        )


def check_consistency(entries: dict):
    errors = []
    warnings = []

    required_keys = ("name", "version", "description")
    optional_keys = ("homepage", "repository", "license")

    for key in required_keys:
        baseline = None
        for entry_name, data in entries.items():
            value = data.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"`{entry_name}` is missing required key `{key}`.")
                continue
            value = value.strip()
            if baseline is None:
                baseline = value
            elif value != baseline:
                errors.append(
                    f"Mismatch on `{key}`: `{entry_name}` = {value!r}, expected {baseline!r}."
                )

    for key in optional_keys:
        seen = []
        for name, data in entries.items():
            value = data.get(key)
            if value is None or value == "":
                continue
            if not isinstance(value, str):
                errors.append(f"`{name}` has non-string optional key `{key}`: {type(value).__name__}")
                continue
            seen.append((name, value.strip()))
        if not seen:
            warnings.append(f"No manifest defines optional key `{key}`.")
            continue
        baseline = seen[0][1]
        for entry_name, value in seen[1:]:
            if value != baseline:
                errors.append(
                    f"Mismatch on optional `{key}`: `{entry_name}` = {value!r}, expected {baseline!r}."
                )
        missing = [name for name, data in entries.items() if not data.get(key)]
        if missing:
            warnings.append(
                f"Optional key `{key}` missing in: {', '.join(missing)}."
            )

    return errors, warnings


def main():
    strict_optional = "--strict-optional" in sys.argv[1:]
    entries = manifest_entries()
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")

    errors, warnings = check_consistency(entries)
    check_marketplace_shape(marketplace, errors)

    if errors:
        print("❌ Metadata consistency check failed:")
        for item in errors:
            print(f"  - {item}")
        if warnings:
            print("\n⚠️  Warnings:")
            for item in warnings:
                print(f"  - {item}")
        return 1

    if strict_optional and warnings:
        print("❌ Metadata consistency check failed in strict optional mode:")
        for item in warnings:
            print(f"  - {item}")
        return 1

    print("✅ Metadata consistency check passed.")
    if warnings:
        print("⚠️  Warnings:")
        for item in warnings:
            print(f"  - {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
