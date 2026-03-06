---
name: meta-skill
description: Use when creating or modifying a Skill
---

# Meta Skill

## Overview

**核心原则**：测试不通过，禁止创建或更新 Skill。

**重要说明**：本 Skill 用于创建/修改其他 Skill，同时它本身也是创建 Skill 的最佳示例。

## When to Use
- 创建新 Skill
- 修改现有 Skill（包括 description）
- **自演进** → 用户发现本 Skill 不足时，用它自己的规则优化它（见 `references/self-evolution.md`）

## Intent Recognition

| 意图 | 行动 |
|------|------|
| 创建新 Skill | **提问澄清**（定位、命名、目录） → TDD |
| 迭代当前 Skill | **简要澄清** → TDD |
| 自演进 | 用户发起 → 子 Agent 在 beta 分支 TDD 迭代 N 次 → 人工确认 → 合并主分支 |

## Core Pattern

```
DISCOVERY → RED → GREEN → REFACTOR
```

### Phase 1: DISCOVERY（渐进式提问）

通过提问明确 Skill 要素：

| 要素 | 问题示例 |
|------|---------|
| **触发条件** | "什么场景下应触发这个 Skill？用户会说什么？" |
| **核心职责** | "它具体做什么？不做什么？" |
| **输入信号** | "用户会提供什么信息/文件？" |
| **输出行为** | "它应该执行什么操作/返回什么？" |
| **边界案例** | "哪些情况容易混淆？不应触发？" |

**命名&目录**：如用户未指定，给出选项供选择：
- **名字建议**：`skill-name`（小写、连字符、语义化）
- **目录**：`skills/{name}/SKILL.md`
- **语言**：优先与用户交流语言一致，可选中文/英文
- **Metadata**：`name`、`description`（第三人称触发条件）

### Phase 2: TDD（实现验证）

| Phase | Action |
|-------|--------|
| **RED** | 无 Skill 运行压力场景 → 记录失败行为 + rationalizations |
| **GREEN** | 写最小 Skill 解决该失败 |
| **REFACTOR** | 发现新漏洞 → 修补 → 重新验证 |

## Rules

1. **Iron Law** - 没有例外（"简单更新"也要测试）
2. **Description = 触发条件** - 第三人称，不总结流程
3. **原理 > 规则** - 解释 why，避免 ALWAYS/NEVER
4. **渐进式披露** - Metadata → SKILL.md → Bundled Resources
5. **Token 效率** - getting-started <150 词，高频 <200 词
6. **评估循环** - 3-5 测试用例，并行运行 baseline，用数据迭代
7. **漏洞封闭** - 添加 "spirit vs letter" 阻断论证
8. **目录规范** - `skill-name/SKILL.md`，仅小写字母、数字、连字符
9. **避免二义性** - 术语、边界、示例清晰无歧义

## Anti-Rationalization

| Excuse | Reality |
|--------|---------|
| "太简单不用测试" | 简单代码也会挂，测试只需 30 秒 |
| "只是小更新" | 小更新也会引入漏洞 |

## CSO Keywords
errors, flaky, hang, timeout, race condition, cleanup, teardown, zombie, pollution

## Common Mistakes

| ❌ | ✅ |
|---|---|
| description 总结 workflow | description = "Use when [症状]" |
| 批量创建不测试 | 一个失败 → 一个 Skill → 验证 |
| 多语言稀释示例 | 单一完整可运行示例 |
| 通用标签 helper1, step3 | 语义化命名 |
| 只测"正常场景" | 压力场景：时间 + 沉没成本 + 疲惫 |

## Example: 创建 pdf Skill

**DISCOVERY 对话**：
```
用户：创建一个处理 PDF 的 Skill

Q: "什么场景下触发？" → "处理这个 PDF"、"分析 PDF 文件"
Q: "做什么？不做什么？" → 提取/分析/总结，不编辑/转换
Q: "输入？" → PDF 文件路径或内容
Q: "输出？" → 结构化内容
Q: "边界？" → "创建 PDF"（生成）、"打印 PDF"不触发
```

**TDD 流程**：RED → GREEN → REFACTOR

**输出**：`skills/pdf/SKILL.md`
