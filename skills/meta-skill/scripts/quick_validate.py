#!/usr/bin/env python3
"""
Quick validation script for skills
"""

import sys
import re
import yaml
from pathlib import Path

def count_lines(content):
    """Count non-empty lines in content (excluding code blocks and frontmatter)"""
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---', '', content, flags=re.DOTALL)
    # Count non-empty lines
    lines = [line for line in content.split('\n') if line.strip()]
    return len(lines)

def check_progressive_disclosure(content, line_count):
    """Return warning message when >= 250 lines"""
    if line_count < 250:
        return False, ""
    return True, "≥250 行建议使用渐进式披露（链接到独立文件，如 [详情](xxx.md)）"

def check_mermaid(content):
    """Check for ASCII flowcharts"""
    # Remove markdown tables first (they use | legitimately)
    content_no_tables = re.sub(r'^\|.*\|$', '', content, flags=re.MULTILINE)
    
    # Check for ASCII art patterns (multi-line box diagrams)
    ascii_patterns = [
        r'┌[─┐└┘├┤┬┴┼]+\n.*├.*┤',  # Multi-line box drawing
        r'\n\+\s*[-=]+\s*\+\n.*\|.*\|',  # +---+ followed by |
        r'┌.*┐\n│.*│\n└.*┘',  # Complete ASCII box
    ]
    for pattern in ascii_patterns:
        if re.search(pattern, content, re.DOTALL):
            return False, "禁止使用 ASCII 流程图，请使用 Mermaid"
    return True, ""

def check_lists_and_tables(content):
    """
    Heuristic check for plain-text 3+ item enumerations.

    We only flag obvious inline enumerations in non-list, non-table lines.
    """
    for line in content.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(('#', '-', '*', '|', '```')):
            continue
        # Only flag obvious one-line numeric enumerations like
        # "1) ... 2) ... 3) ..." that should be broken into list/table.
        if re.search(r'1[.)、].*2[.)、].*3[.)、]', stripped):
            return False, "检测到疑似 3+ 项并列文本，请改为列表或表格"
    return True, ""

def validate_skill(skill_path, strict=False):
    """Validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text(encoding="utf-8")
    # Normalize for cross-platform line endings and UTF-8 BOM.
    content = content.lstrip('\ufeff').replace('\r\n', '\n')
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if not name:
        return False, "Name cannot be empty or whitespace-only"
    # Check naming convention (kebab-case: lowercase with hyphens)
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    # Check name length (max 64 characters per spec)
    if len(name) > 64:
        return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    # Additional validations
    line_count = count_lines(content)
    
    # Line count check - ≥500 lines fails
    if line_count >= 500:
        return False, f"行数 {line_count} 超过 500 限制"
    
    # Line count check - ≥250 lines warning
    has_warning, msg = check_progressive_disclosure(content, line_count)
    if has_warning:
        if strict:
            return False, msg
        print(f"WARNING: {msg}")

    valid, msg = check_mermaid(content)
    if not valid:
        return False, msg

    valid, msg = check_lists_and_tables(content)
    if not valid:
        return False, msg

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print("Usage: python quick_validate.py <skill_directory> [--strict]")
        sys.exit(1)

    strict_mode = len(sys.argv) == 3 and sys.argv[2] == "--strict"
    if len(sys.argv) == 3 and not strict_mode:
        print("Unknown option. Supported option: --strict")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1], strict=strict_mode)
    print(message)
    sys.exit(0 if valid else 1)