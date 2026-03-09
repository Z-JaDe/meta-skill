---
name: skill-format
description: Use when formatting or validating SKILL.md files when skill not loading, wrong triggers, description summarizing workflow, abstract naming, or excessive word count
---

# SKILL Format

## Overview

SKILL 为 AI Agent 执行而写，非为人脑理解。确保技能可被发现、正确触发、严格执行。

**CRITICAL**: Description 总结工作流程 → AI 只看描述不读全文

**适用**: 格式化/验证 SKILL.md、修复触发问题

**不适用**: 人类文档、创意写作、营销文案

---

## Core Pattern

### Description 规范

```yaml
# ❌ BAD: 描述工作流程
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# ✅ GOOD: 仅触发条件
description: Use when implementing any feature or bugfix, before writing implementation code
```

### 命名规范

```markdown
# ❌ BAD: 名词开头
## Skill Creation

# ✅ GOOD: 动名词开头
## Creating Skills
```

---

## Implementation

| 步骤 | 要点 | 示例 |
|------|------|------|
| 命名 | 动名词开头 | ✅ `creating-skills` ❌ `skill-creation` |
| Description | 仅触发条件 | ✅ `Use when implementing` ❌ `Use for TDD...` |
| 关键词 | 错误/症状/同义词 | `skill not loading`, `wrong triggers` |
| 跨引用 | 技能名 + `**REQUIRED:**` | `**REQUIRED:** Use test-first` |

**CRITICAL**: Description 若总结流程，AI 将跳过全文

---

## Anti-Patterns

| 错误 | 修复 |
|------|------|
| Description 总结流程 | 仅保留触发条件 |
| Description 使用冒号分隔 trigger keywords | 用 when/due to/with 自然融入 |
| 第一人称 | 改用第三人称 |
| 抽象命名 | 使用具体动词/症状 |
| 过度详细 | 移至 --help 或跨引用 |
| 使用 @ 引用 | 仅用技能名 |

---

## Verification

```bash
wc -w skills/path/SKILL.md  # 字数
head -5 skills/path/SKILL.md  # Frontmatter
ls skills/ | grep -E '^[a-z0-9-]+$'  # 命名
```

**部署检查清单**:
- [ ] 命名：仅字母 + 连字符
- [ ] Frontmatter：仅 name + description
- [ ] Description：以 "Use when..." 开头，无流程总结
- [ ] 跨引用：使用技能名，无 @ 路径
