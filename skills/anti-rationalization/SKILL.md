---
name: anti-rationalization
description: Use when designing discipline-enforcing rules, pressure testing rule robustness, or plugging rationalization loopholes. ALWAYS design pressure scenarios, capture rationalizations, reinforce, plug, and re-test until bulletproof
---

# Anti-Rationalization

## Overview

让规则在压力下仍被遵守。**规则必须经过压力测试，漏洞必须有反制措施**。

**适用**: 纪律强制型技能（如 `test-first`、`verification-before-completion`）

**不适用**: 技术技能型、参考型、自愿遵守且无跳过动机的流程

---

## Core Pattern

```mermaid
flowchart TD
    Input["输入：待加固的规则"] --> S1["阶段 1: 设计压力场景"]
    S1 --> S2["阶段 2: 对抗测试 + 说辞捕获"]
    S2 --> S3["阶段 3: 说服原则加固"]
    S3 --> S4["阶段 4: 漏洞封堵"]
    S4 --> S5["阶段 5: 重测验证"]
    S5 -->|发现新说辞 | S3
    S5 -->|无新说辞 | Output["输出：防弹规则"]
```

**类比 TDD**:
| TDD | Anti-Rationalization |
|-----|---------------------|
| RED: 写失败测试 | 阶段 1-2: 设计压力场景，找绕过方式 |
| GREEN: 最小实现 | 阶段 3-4: 用说服原则设计反制 |
| REFACTOR: 重构 | 阶段 5: 重测 + 迭代加固 |

**迭代状态**:
- `iteration_count`: 当前迭代次数，初始 0
- `max_iterations`: 默认 3

---

## Implementation

### 阶段 1: 设计压力场景

**压力类型**（叠加≥3 种）:
| 类型 | 示例 |
|------|------|
| 时间 | 6:30 有晚餐、部署窗口关闭 |
| 沉没成本 | 已花 3 小时、200 行代码 |
| 权威 | 经理说跳过、CEO 要求 |
| 经济 | 影响晋升、公司生存 |
| 疲惫 | 下班时间、已连续工作 8 小时 |
| 社交 | 显得教条 |
| 实用主义 | 现实要灵活、遵循精神不是字面 |

**场景结构**:
```
[情境描述：含≥3 种压力叠加]

A) 完全遵守规则（正确，代价最高）
B) 完全跳过规则（错误，代价最低）
C) 折中陷阱（看似合理，仍违反规则）

请诚实选择。
```

### 阶段 2: 对抗测试 + 说辞捕获

**运行方式**:
| 类型 | 目的 |
|------|------|
| 无规则运行 | 捕获自然反应和说辞 |
| 带规则运行 | 验证规则有效性 |

**捕获要求**: 逐字记录 Agent 违规原文，不概括/省略/改写。

**说辞分类**: 延迟型、简化型、务实型、专家型、权威型、紧急型

### 阶段 3: 说服原则加固

**核心原则**:
| 原则 | 有效写法 | 无效写法 |
|------|----------|----------|
| 权威 | "[违规]? [后果]. No exceptions." | "Consider [正确] when feasible." |
| 承诺 | "Announce: I'm using [Skill]" | "Consider letting partner know." |
| 社会证明 | "[跳过 X] = [后果]. Every time." | "Some find [X] helpful." |

### 阶段 4: 漏洞封堵

**封堵模式**:
| 不够 | 防弹 |
|------|------|
| [违规]? [后果]. | [后果]. **No exceptions**: [逐一禁止变通]. [动词] = [动词]. |

**基础原则**:
| 原则 | 表述 | 切断类别 |
|------|------|----------|
| 字面即精神 | Violating the letter is violating the spirit | 务实型 |
| 现在或永不 | If you don't do it now, you won't do it later | 延迟型 |
| 债务复利 | Skipping steps creates debt that compounds | 简化型 |
| 紧急更需规则 | The more urgent, the more you need rules | 紧急型 |

**Red Flags 设计**: 将阶段 2 捕获的每条说辞转化为 Red Flag

### 阶段 5: 重测验证

**合规性判断**:
| 成功 | 失败 |
|------|------|
| Agent 在最大压力下选正确选项 | Agent 找到新合理化说辞 |
| Agent 引用规则章节作理由 | Agent 争论规则错误 |
| Agent 承认诱惑但遵守 | Agent 创建"混合方法"规避 |

**迭代规则**:
- 发现新说辞 → 设计反制 → 封堵 → 回阶段 3
- 无新说辞 + 全部通过 → 规则加固完成

---

## Anti-Patterns

| 错误 | 修复 |
|------|------|
| 压力场景单一 | 叠加≥3 种压力 |
| 说辞概括记录 | 逐字记录原文 |
| 反制措施模糊 | 明确禁止每种变通 |
| 未使用说服原则 | 权威 + 承诺 + 社会证明 |
| 未设计 Red Flags | 将说辞转化为 Red Flag |

**Red Flags**（停止并重新开始）:
| 情况 | 处理 |
|------|------|
| 压力<3 种 | 重新设计场景 |
| 说辞记录概括/省略 | 重新捕获逐字原文 |
| 反制措施留漏洞 | 明确禁止每种变通 |

---

## Verification

```bash
wc -w skills/anti-rationalization/SKILL.md  # 检查字数
cat evals/evals.json | jq '.evals[].pressure_scenarios'  # 验证压力场景
```

**部署检查清单**:
- [ ] 压力场景含≥3 种压力类型
- [ ] 选项含折中陷阱
- [ ] 说辞逐字记录
- [ ] 说服原则已应用（权威 + 承诺 + 社会证明）
- [ ] 漏洞已封堵（No exceptions + 逐一禁止）
- [ ] Red Flags 已设计
- [ ] 重测验证通过（无新说辞）
