# Meta Skill Context

This file provides lightweight runtime context for Qwen extension loading.

## Canonical Process Source

The single authoritative workflow definition is:

- `skills/meta-skill/SKILL.md`

When README snippets and `SKILL.md` differ, always follow `skills/meta-skill/SKILL.md`.

## Scope

- Project purpose: create and improve AI skills with strict quality gates.
- Built-in skills live under `skills/`.
- Packaging script: `skills/meta-skill/scripts/package_skill.py`.

## Required Quality Gates

1. Intent discovery
2. Type decision (main type + enforcement tag)
3. TDD loop (`test-first` + `skill-format`, with anti-rationalization enhancement when needed)
4. Blind comparison (candidate vs baseline)
5. AI doc optimization
6. Packaging

## Validation

After modifying any `SKILL.md`, run:

```bash
python3 skills/meta-skill/scripts/quick_validate.py skills/<skill-name>
```
