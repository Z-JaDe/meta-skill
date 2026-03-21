---
name: skill-format
description: Use when formatting or validating SKILL.md due to skill not loading, wrong triggers, description summarizing workflow, abstract naming, or excessive word count
---

# SKILL Format

## Overview

SKILL 为 AI Agent 执行而写，非为人脑理解。

**核心目标**: 确保技能可被发现、正确触发、严格执行

**CRITICAL**: Description 是触发路由，不是执行说明。若写成流程总结，会导致误触发或错路由。

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

### Description 优化三步

| 步骤 | 目标 | 检查标准 |
|------|------|----------|
| 1. 触发条件 | 说清何时调用 | 以 `Use when...` 开头，包含场景/症状 |
| 2. 边界限定 | 避免误触发 | 明确不属于本技能的相邻场景（用 `due to`/`with` 收束） |
| 3. 去流程化 | 避免偷塞实现步骤 | 不出现阶段顺序、实现动作链、长流程描述 |
| 4. 可检索性 | 降低漏触发 | 建议 1 句完成，长度 15-220 字符，包含至少 1 个可观察症状关键词 |

**推荐模板**:

```yaml
description: Use when <trigger condition> due to <observable symptoms or constraints>.
```

### 命名规范

```markdown
# ❌ BAD: 名词开头
## Skill Creation

# ✅ GOOD: 动名词开头
## Creating Skills
```

---

## 内容要求

### 1. Agent 调度机制（编排型技能必须包含）

编排型技能 = 调用 SubAgent 执行 2+ 阶段的技能。

**执行分工**:
- 主 Agent: 调度和协调 SubAgent 流转，判断收敛/完成
- SubAgent: 执行具体阶段/步骤

**SubAgent 启动机制**:
- 当前在主 Agent → 直接启动新 SubAgent 实例
- 当前在 SubAgent → 通知主 Agent 启动新 SubAgent 实例

### 2. 内容质量要求（所有技能必须遵守）

**写作前准备**:
1. **了解 ai-doc-optimizer**: 内容写好后大概率会被优化；提前写好 → 降低被优化概率
2. **明确定位**: 从第一性原理出发思考技能核心目的
3. **旧技能分析**（优化场景）: 假设从零设计、对比旧技能取舍、收集用户要求

**内容标准**:
- 零歧义：术语定义明确，流程确定
- 零冗余：无填充语、弱动词、重复陈述
- 结构化：3+ 项用列表/表格，流程用 Mermaid(优先)/DOT
- 独立完整：零依赖封闭语境，不依赖外部文件/链接

---

## Implementation

**执行流程**:
1. 读取现有 SKILL.md
2. 验证格式（命名、Description、Frontmatter）
3. 验证内容（见 内容标准）
4. 输出修复建议或修复后的 SKILL.md

**格式规范**:

| 步骤 | 要点 | 示例 |
|------|------|------|
| 命名 | 动名词开头 | ✅ `creating-skills` ❌ `skill-creation` |
| Description | 仅触发条件 + 边界，不总结工作流 | ✅ `Use when implementing` ❌ `Use for TDD...` |
| 关键词 | 错误/症状/同义词 | `skill not loading`, `wrong triggers` |
| 跨引用 | 技能名 + `**REQUIRED:**` | `**REQUIRED:** Use test-first` |

---

## Dependencies

| 依赖 | 关系 | 说明 |
|------|------|------|
| ai-doc-optimizer | 参考 | 内容质量标准同 ai-doc-optimizer |
| test-first | 可选 | 创建技能时可能需要 |

---

## Anti-Patterns

| 错误 | 修复 | 典型说辞（不得合理化） |
|------|------|------------------------|
| Description 总结流程 | 仅保留触发条件 | "描述流程更清楚"；"用户更容易理解" |
| Description 塞入硬约束口号（如 ALWAYS / NO EXCEPTIONS） | 将硬约束移入正文 Overview/Anti-Patterns | "放在 description 更醒目"；"这样不会忘记" |
| Description 过短/过长导致误触发 | 控制在单句 15-220 字符并包含症状关键词 | "越短越好"；"写长一点更保险" |
| Description 使用冒号分隔 trigger keywords | 用 when/due to/with 自然融入 | "这样更简洁"；"冒号更清晰" |
| 第一人称 | 改用第三人称 | "第一人称更亲切"；"这样写更自然" |
| 抽象命名 | 使用具体动词/症状 | "抽象命名更通用"；"这样更专业" |
| 过度详细 | 移至 --help 或跨引用 | "详细点更好"；"避免用户不理解" |
| 使用 @ 引用 | 仅用技能名 | "@ 引用更明确"；"这样更规范" |

---

## Verification

```bash
wc -w skills/<path>/SKILL.md   # <path>=占位符；字数
head -5 skills/<path>/SKILL.md # Frontmatter
ls skills/
rg "^name: [a-z0-9-]+$" skills --glob "*/SKILL.md"  # frontmatter 命名抽检
```

**部署检查清单**:
- [ ] 命名：仅字母 + 连字符
- [ ] Frontmatter：至少 name + description（可选：license / allowed-tools / metadata / compatibility）
- [ ] Description：以 "Use when..." 开头，包含触发条件/边界，无流程总结
- [ ] Description：单句（建议）且 15-220 字符，包含至少 1 个可观察症状关键词
- [ ] 跨引用：使用技能名，无 @ 路径
