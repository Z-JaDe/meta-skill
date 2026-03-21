# Meta Skill

**Create custom AI skills with guaranteed completeness and optimized retrieval.** Meta-skill uses **TDD + Anti-Rationalization Pressure Testing + Blind Comparison** to ensure skill completeness, and **redundancy removal + ambiguity clarification + progressive disclosure** to maximize AI retrieval efficiency.

[中文文档](README_CN.md)

---

## Quick Start: Create Your First Skill

```bash
# In Qwen Code or Claude Code, simply ask:
"Create a skill for [your requirement]"
```

**Example:**
```
"Create a skill for automatic code review"
"Create a skill for writing unit tests"
"Create a skill for optimizing prompts"
```

Meta-skill will automatically:

**Ensure Completeness:**
1. **TDD** - Write tests first to define expected behavior
2. **Anti-Rationalization Pressure Testing** - Capture and plug loopholes under pressure scenarios
3. **Blind Comparison** - Verify candidate significantly outperforms baseline

**Optimize AI Retrieval:**
4. **Ambiguity Clarification** - Resolve unclear semantics
5. **Redundancy Removal** - Eliminate duplicate content
6. **Progressive Disclosure** - Structure information from simple to complex

7. **Package** as `.skill` file ready to use

---

## Core Philosophy

**Self-Evolution: The meta-skill uses its own pipeline to create and continuously improve skills (including itself) until convergence.**

The `skills/` directory contains the built-in skill library that meta-skill calls during its creation pipeline.

---

## Core Flow

```
Intent Discovery → Type Decision → TDD Loop → Blind Comparison → AI Retrieval Optimization → Package
```

This README only keeps a lightweight flow view.

**Single source of truth for the authoritative stage contract and gating rules:**

- `skills/meta-skill/SKILL.md`

| Stage (Lite View) | Main Components |
|-------------------|-----------------|
| Intent Discovery | `intent-discovery` |
| Type Decision | `meta-skill` stage-2 judgment (main type + enforcement tag) |
| TDD Loop | `test-first` + `skill-format` (+ `anti-rationalization` when enforcement tag is present) |
| Blind Comparison | `agents/{grader,comparator,analyzer}` + `scripts/aggregate_benchmark.py` |
| AI Retrieval Optimization | `ai-doc-optimizer` |
| Package | `scripts/package_skill.py` |

---

## Skill System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  skills/  (Built-in Skill Library)                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  meta-skill/ (Orchestrator)                          │   │
│  │  - SKILL.md                                          │   │
│  │  - agents/ (grader, analyzer, comparator)            │   │
│  │  - scripts/ (package_skill.py, aggregate_benchmark)  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Sub-skills (Called by meta-skill during pipeline)   │   │
│  │  - intent-discovery/  - test-first/                  │   │
│  │  - anti-rationalization/  - skill-format/            │   │
│  │  - ai-doc-optimizer/                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Note**: When creating a NEW skill, output goes to user-specified directory (`~/.qwen/skills/`, `./`, etc.), NOT in `meta-skill/skills/`.

---

## Skill Relationships

```mermaid
flowchart TB
    User[User Request] --> Meta[meta-skill<br/>Orchestrator]

    Meta --> ID[intent-discovery<br/>Requirement Clarification]
    ID --> Meta

    Meta --> TF[test-first<br/>TDD Methodology]
    TF --> AR[anti-rationalization<br/>Pressure Testing]
    AR --> TF
    TF --> SF[skill-format<br/>Format Validation]
    SF --> TF

    Meta --> AO[ai-doc-optimizer<br/>Iterative Optimization]
    AO --> AO

    subgraph Flow[Creation Flow]
        ID
        TF
        AO
    end

    subgraph Support[Support Skills]
        AR
        SF
    end

    Meta --> Flow
    Flow --> Support
```

---

## Skills

### Built-in Skill Library

These skills work together to create new skills:

| Skill | Role in Skill Creation |
|-------|------------------------|
| `meta-skill` | **Orchestrator** — coordinates the entire skill creation pipeline |
| `intent-discovery` | **Requirement Analyst** — clarifies vague requirements through progressive questioning |
| `test-first` | **TDD Engine** — writes tests before implementation to ensure correctness |
| `anti-rationalization` | **Quality Assurance** — pressure-tests rules to prevent loopholes |
| `skill-format` | **Validator** — ensures SKILL.md follows proper format |
| `ai-doc-optimizer` | **Optimizer** — iteratively refines documentation for AI reading efficiency |

### How Skills Work Together

When you ask meta-skill to create a new skill:

```
User Request → intent-discovery → type decision
           → test-first + skill-format (+ anti-rationalization when needed)
           → blind comparison → ai-doc-optimizer → package
```

Each sub-skill handles a specific aspect of the creation process, ensuring the final skill is:
- **Well-defined** (clear requirements)
- **Test-covered** (TDD-driven)
- **Robust** (pressure-tested against rationalization)
- **Well-documented** (optimized for AI reading)
- **Properly formatted** (validated format)

---

## Self-Evolution

All skills in `skills/` are created and maintained by the meta-skill pipeline:

```
v0.1: Single monolithic skill (500+ lines, complex)
    ↓ TDD + Split (via meta-skill)
v0.2: Split into focused sub-skills
    ↓ Refactor (via meta-skill)
v0.3: Remove redundancy, clarify ambiguity
    ↓ Converge (via meta-skill)
v1.0: Final optimized version
```

**Key insight**: meta-skill evolves itself and its sub-skills using the same pipeline it orchestrates.

---

## Directory Structure

```
meta-skill/
├── skills/
│   ├── meta-skill/
│   │   ├── SKILL.md
│   │   ├── agents/              # grader.md, analyzer.md, comparator.md
│   │   └── scripts/             # package_skill.py, aggregate_benchmark.py
│   ├── intent-discovery/
│   │   └── SKILL.md
│   ├── test-first/
│   │   ├── SKILL.md
│   │   └── evals/
│   ├── anti-rationalization/
│   │   └── SKILL.md
│   ├── skill-format/
│   │   └── SKILL.md
│   └── ai-doc-optimizer/
│       └── SKILL.md
├── .qwen/
└── README.md
```

**Note**: `skills/` contains meta-skill's built-in skill library. New skills created via meta-skill are placed in user-specified directories (e.g., `~/.qwen/skills/`, `./`), NOT in `meta-skill/skills/`.

---

## Extensions

This project works as a **Claude Code Plugin**, **Qwen Code Extension**, and **Cursor Plugin**.

### Installation

**Claude Code:**
```bash
/plugin marketplace add https://github.com/Z-JaDe/meta-skill
/plugin install meta-skill
```

**Qwen Code:**
```bash
# From remote URL
qwen extensions install https://github.com/Z-JaDe/meta-skill

# Or link local (for development)
qwen extensions link /path/to/meta-skill
```

**Cursor:**

In Cursor Agent chat, install from marketplace:

```text
/plugin-add meta-skill
```

### Configuration

| Platform | Configuration File |
|----------|-------------------|
| Claude Code | `.claude-plugin/marketplace.json` |
| Qwen Code | `qwen-extension.json` |
| Cursor | `.cursor-plugin/plugin.json` |

---

## Contributing

Please follow `CONTRIBUTING.md` for:

- minimal newcomer path,
- required `quick_validate.py` before contribution,
- `.test/` artifact policy,
- plugin metadata release sync checklist,
- `check_plugin_metadata.py` automated consistency check.

---

## License

MIT (see `LICENSE`)

---

## Acknowledgments

This project draws inspiration from:

- **Anthropic's `skill-creator`** - Skill creation methodology
- **Superpowers' `writing-skills`** - Skill writing patterns
