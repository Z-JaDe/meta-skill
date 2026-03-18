---
name: meta-skill
description: Use when creating new skills from scratch or improving existing skills. Orchestrates intent-discovery → TDD → blind comparison → optimization.
---

# Meta Skill

## Overview

编排技能创建/更新流程。**纯调度，不执行**：不直接读写文件、不运行测试、不编写代码；仅调用 SubAgent/技能/脚本。

**输入**: 模糊想法（创建）/ 现有技能 + 改进需求（更新）  
**输出**: 打包好的 `.skill` 文件

**铁律**: `NO SKILL WITHOUT A FAILING TEST FIRST`（没有例外）

**硬性限制**:
| 限制 | 数值 |
|------|------|
| TDD 循环 | 最多 5 次 |
| Blind Comparison | 最多 3 轮 |

---

## 适用与不适用

| 适用（触发 meta-skill） | 不适用（停止并引导） |
|----------------------|----------------------|
| 创建新技能 | 修复技能 bug → 直接修复或引导使用 test-first |
| 优化现有技能 | 简单文档编辑 → 直接使用 ai-doc-optimizer |
| 技能质量提升 | 格式验证 → 直接使用 skill-format |
| 技能重构 | 紧急修复（先止血、事后补流程）→ 直接修复 |

**Bug 检测**: 用户描述"技能没触发""技能执行失败""格式错误"等 → 视为 Bug，**不触发 meta-skill**，引导使用对应技能或直接修复。

---

## Terminology

**核心术语**:

| 术语 | 定义 |
|------|------|
| TDD | 测试驱动开发：RED→GREEN→REFACTOR |
| RED | 编写测试→SubAgent 执行失败 |
| GREEN | 编写实现→SubAgent 执行通过 |
| REFACTOR | 修订技能→泛化+精简→保持通过 |
| Blind Comparison | 盲比较：评估者不知 candidate/baseline 身份 |
| candidate | 待验证的技能版本（新技能或优化后版本） |
| baseline | 对比基准（新技能=无技能；优化=旧版本） |
| 显著优于基线 | 新技能：选择率>70% AND 通过率提升>20%；优化：选择率>60% AND 通过率不降低 |
| SubAgent | 独立 Agent 实例。当前在主 Agent 则直接启动新实例；当前在 SubAgent 则通知主 Agent 启动 |

**辅助术语**:

| 术语 | 定义 |
|------|------|
| evals.json | 评估用例配置，含 eval 用例列表；有纪律强制标签时另含 pressure_scenarios |
| 返回 REFACTOR | 返回阶段 3 继续 TDD 循环 |
| improvement_suggestions | analyzer.md 输出；指明 eval 时仅重跑该部分，否则全重跑 |
| 主类型 | 技能核心功能分类：参考型、编排型、模式型、技术技能型 |
| 纪律强制标签 | 可叠加到任何主类型的属性：有强制规则 + 合规成本 + AI 易跳过 |
| 说辞 | rationalization=AI 用于合理化跳过规则的表述 |
| 压力叠加 | 多种压力同时作用（如时间紧+需求简单+SubAgent 失败）；≥3 种 |
| 改进需求 | 优化旧技能时用户提出的优化方向或问题描述 |
| 明显问题 | 歧义、冗余、结构混乱（任一即触发前置优化） |

---

## Core Pattern

```mermaid
flowchart TD
    Start[用户请求创建/优化技能] --> CheckScope{适用场景?}
    CheckScope -->|Bug/格式/简单编辑| Reject[停止: 引导使用对应工具]
    CheckScope -->|创建/优化技能| P1[调度 intent-discovery]
    P1 --> P2[类型判断<br/>主类型 + 标签]
    P2 --> P3{有纪律强制标签?}
    P3 -->|是| P3a[调度 test-first<br/>TDD + Anti-Rationalization 增强]
    P3 -->|否| P3b[调度 test-first<br/>标准 TDD]
    P3a --> P4{RED-GREEN-REFACTOR 通过？}
    P3b --> P4
    P4 -->|否 | P3
    P4 -->|是 | P5[Blind Comparison]
    P5 --> P6{显著优于基线？}
    P6 -->|否 | P3
    P6 -->|是 | P7[调度 ai-doc-optimizer<br/>优化最终文档]
    P7 --> P8[package_skill.py]
```

---

## Output Path Contract

**所有阶段 3-4 产出必须落于**: `.test/`

| 阶段 | 产出 | 路径 | 说明 |
|------|------|------|------|
| 3 TDD | evals.json | `.test/iteration-N/evals.json` | N=迭代编号 |
| 3 TDD | grading.json | `.test/iteration-N/eval-M/{candidate,baseline}/run-K/grading.json` | M=eval 编号，K=run 编号（每 eval 跑 3 次） |
| 4 盲比较 | benchmark.json | `.test/iteration-N/benchmark.json` | |
| 4 盲比较 | comparison_result.json | `.test/iteration-N/comparison_result.json` | |
| 4 盲比较 | improvement_suggestions | `.test/iteration-N/improvement_suggestions` | |
| 失败 | failure.md | `.test/iteration-N/failure.md` | |

---

## 文档内容约束

| 文档 | 应包含 | 应避免 |
|------|--------|--------|
| SKILL.md | 触发条件、核心模式、实现步骤、依赖关系、反模式 | 完整代码实现、过度详细的示例 |
| evals.json | 测试用例、输入、期望输出、压力场景（有纪律强制标签时） | 模糊的期望、缺少边界条件 |
| improvement_suggestions | 具体问题、改进方向、重跑范围 | 泛泛而谈、缺少可执行建议 |

*本表即为各阶段产出的内容约束权威定义。*

---

## Implementation

**阶段速览**:
| 阶段 | 调度 | 输出 |
|------|------|------|
| 1 意图捕捉 | intent-discovery | requirements、context |
| 2 类型判断 | 无（本阶段判断） | skill_type（主类型+标签） |
| 3 TDD | test-first、skill-format | SKILL.md、evals、通过 |
| 4 盲比较 | grader、comparator、analyzer、aggregate_benchmark | 显著优于基线 |
| 5 文档优化 | ai-doc-optimizer | 收敛文档 |
| 6 打包 | package_skill.py | .skill 文件 |

### 阶段 1: 意图捕捉

**调度**: [必须] 技能 `intent-discovery`，渐进式提问澄清需求

| 传递项 | 值 |
|--------|-----|
| requirement_type | "skill-creation"（固定） |
| context | `{"language": "zh-CN \| en-US", "output_dir": "~/.qwen/skills/xxx 或 ./skills/xxx"}` |

**intent-discovery 输出**（JSON 结构）:
- `requirement_type`: "skill-creation"
- `requirements`: {what, when, output, test}
- `boundaries`: {in_scope, out_of_scope}
- `context`: {skill_name, description, language, output_dir}
- `next_steps`: []

**meta-skill 提取**: skill_name、description、language、output_dir 从 context；skill_type 在阶段 2 判断

### 阶段 2: 技能类型判断

**输入**: 阶段 1 的 intent-discovery 输出  
**输出**: skill_type（主类型 + 纪律强制标签）加入 context

```mermaid
flowchart TD
    Start[开始] --> Q1{核心功能？}
    Q1 -->|API/语法文档| Type1[参考型]
    Q1 -->|调度技能/Agent/脚本| Type2[编排型]
    Q1 -->|决策框架/权衡原则| Type3[模式型]
    Q1 -->|具体操作步骤| Type4[技术技能型]
    Type1 --> Q2{有强制规则+合规成本+AI易跳过？}
    Type2 --> Q2
    Type3 --> Q2
    Type4 --> Q2
    Q2 -->|是| Label[+ 纪律强制标签]
    Q2 -->|否| TDD1[标准 TDD]
    Label --> TDD2[TDD + Anti-Rationalization 增强]
```

**主类型**:
| 主类型 | 核心问题 | 特征 | 例子 |
|--------|---------|------|------|
| 参考型 | "语法/API 是什么？" | 文档、速查表、配置说明 | Git 命令参考、API 文档 |
| 编排型 | "调度谁？按什么顺序？" | 调度其他技能/Agent/脚本 | **Meta-Skill**、CI/CD 流程 |
| 模式型 | "怎么选？如何权衡？" | 决策框架、判断标准、权衡原则 | 架构设计原则、测试策略 |
| 技术技能型 | "怎么做？具体步骤？" | 操作步骤、工具使用 | 配置 Git、部署应用 |

**纪律强制标签**（可叠加到任何主类型）:
| 判断标准 | 说明 | 例子 |
|---------|------|------|
| 有强制规则 | 明确的"必须"或"禁止" | "必须先写测试"、"禁止跳过澄清" |
| 有合规成本 | 遵守规则需要额外工作量 | 调度 SubAgent 比自己写慢 |
| AI 易合理化跳过 | AI 容易找借口不遵守 | "这个很简单，不需要测试" |

**TDD 模式映射**:
| 主类型 + 标签 | TDD 模式 |
|--------------|---------|
| 任意主类型 + 纪律强制标签 | TDD + Anti-Rationalization 增强 |
| 任意主类型（无标签） | 标准 TDD |

### 阶段 3: TDD 循环（RED-GREEN-REFACTOR）

**调度**: [必须] 技能 `test-first`  
**最大迭代**: 5 次（超过→人工审查）

**模式选择**: 见阶段 2 TDD 模式映射

#### 标准 TDD（技术技能型、模式型、参考型）

```mermaid
flowchart LR
    R1[创建 evals.json] --> R2[SubAgent 执行 不加载技能]
    R2 --> R3[记录失败案例]
    R3 --> G1[SubAgent: skill-format 编写 SKILL.md]
    G1 --> G2[SubAgent: 执行 eval 加载技能]
    G2 --> G3[验证测试通过]
    G3 --> RF{需要改进?}
    RF -->|是| RF1[修订技能→泛化+精简]
    RF1 --> R1
    RF -->|否| Done[通过]
```

| 步骤 | 操作 | 输出 |
|------|------|------|
| RED | 创建 evals.json → SubAgent 执行（不加载技能）→ 记录失败案例 | evals.json、失败案例记录 |
| GREEN | SubAgent 调度 skill-format 编写 SKILL.md → 执行 eval（加载技能）→ 验证通过 | SKILL.md |
| REFACTOR | 需要改进 → 修订技能 → 泛化+精简 | 优化后的 SKILL.md |

#### Anti-Rationalization 增强（有纪律强制标签）

在标准 TDD 基础上，各阶段增加 anti-rationalization 策略：

| 步骤 | 标准 TDD | 增强内容 |
|------|---------|----------|
| RED | 创建 evals.json、记录失败案例 | + 设计压力场景（见术语：压力叠加）<br/>+ 对抗测试捕获说辞（逐字记录） |
| GREEN | 编写 SKILL.md、验证通过 | + 说服原则加固（权威+承诺+社会证明）<br/>+ 漏洞封堵（No exceptions + 逐一禁止）<br/>+ 设计 Red Flags 和 Anti-Patterns |
| REFACTOR | 修订技能 | + 重测验证（压力场景下）<br/>+ 发现新说辞 → 继续加固 |

**输出**: evals.json 含 pressure_scenarios；SKILL.md 含标准章节 + 纪律执行章节（Red Flags 表格）+ Anti-Patterns

**参考**: 按需调度 anti-rationalization 技能。

### 阶段 4: Blind Comparison

**对比策略**:
| 场景 | 对比方式 | 基线 |
|------|----------|------|
| 创建新技能 | new-skill vs baseline | baseline=无技能运行 |
| 优化旧技能 | new-skill vs old-skill | old-skill=优化前版本 |

**最大迭代**: 3 轮（每轮：每 eval 跑 3 次 candidate + 3 次 baseline）

```mermaid
flowchart TD
    S1[并行运行 candidate/baseline 每 eval 3 次] --> S2[grader.md→grading.json]
    S2 --> S3[aggregate_benchmark.py→benchmark.json]
    S3 --> S4[comparator.md 盲评→comparison_result.json]
    S4 --> S5[analyzer.md→improvement_suggestions]
    S5 --> S6{显著优于基线?}
    S6 -->|是| Pass[通过]
    S6 -->|否| Refactor[返回 REFACTOR]
```

| 步骤 | 调度 |
|------|------|
| 1 并行运行 candidate/baseline | SubAgent |
| 2 grader→grading.json | SubAgent |
| 3 aggregate_benchmark | 脚本 |
| 4 comparator 盲评→comparison_result.json | SubAgent |
| 5 analyzer→improvement_suggestions | SubAgent |
| 6 判断显著优于基线 | 无 |

**路径**: 见 Output Path Contract。**指标**: 选择率=comparator 选 candidate 比例；通过率=grader 断言通过比例。**失败**: 未通过→返回 REFACTOR（用 improvement_suggestions）。

### 阶段 5: 文档优化

**调度**: [必须] 技能 `ai-doc-optimizer`  
**收敛标准**: 连续 2 轮语义等价且结构稳定，或 max_iterations=5

| 情况 | 处理 |
|------|------|
| 语义丢失 | 输出 last_valid + 警告 |
| 达上限未收敛 | 输出 last_valid + 未解决问题列表 |

### 阶段 6: 打包部署

```bash
python3 scripts/package_skill.py .
```

**输出**: `.skill` 文件

**验证规则**（scripts/quick_validate.py 执行）:
| 规则 | 要求 |
|------|------|
| 命名 | kebab-case |
| frontmatter | 有效 YAML，description 含冒号需加引号 |
| 行数 | <500 行（硬限制）；≥250 行需渐进式披露（警告） |
| 格式 | Mermaid 流程图（禁止 ASCII），3+ 项用列表/表格 |

---

## HARD-GATE 检查点

| 序号 | 检查项 | 阶段 |
|------|--------|------|
| 1 | 是否通过 intent-discovery 澄清需求？ | 1 |
| 2 | 是否判断技能类型（主类型+标签）？ | 2 |
| 3 | 是否通过 SubAgent 执行 TDD？ | 3 |
| 4 | evals.json 是否包含压力场景（有纪律强制标签时）？ | 3 |
| 5 | SKILL.md 是否包含 Red Flags 和 Anti-Patterns（有纪律强制标签时）？ | 3 |
| 6 | 是否通过 Blind Comparison 且达标？ | 4 |
| 7 | 产出是否位于 `.test/iteration-N/`？ | 3-4 |
| 8 | 是否通过 ai-doc-optimizer 优化最终文档？ | 5 |
| 9 | 是否通过 package_skill.py 打包？ | 6 |

---

## Dependencies

| 依赖 | 阶段 | 必须/可选 |
|------|------|----------|
| intent-discovery | 1 | 必须 |
| ai-doc-optimizer | 5 | 必须 |
| test-first | 3 | 必须 |
| skill-format | 3 | 必须 |
| anti-rationalization | 3（有纪律强制标签） | 参考 |
| agents/grader.md | 4 | 必须 |
| scripts/aggregate_benchmark.py | 4 | 必须 |
| agents/comparator.md | 4 | 必须 |
| agents/analyzer.md | 4 | 必须 |
| scripts/package_skill.py | 6 | 必须 |

---

## Anti-Patterns

| 错误 | Red Flag | 反制 | 典型说辞（不得合理化） |
|------|----------|------|------------------------|
| 跳过 intent-discovery | "需求很清楚" | 模糊需求是技能失败首因 | "我已经知道要做什么"；"这个很简单，直接开始" |
| 跳过 RED 阶段 | "技能很简单，不需要测试" | 跳过测试=无法证明有效 | "写个测试太浪费时间"；"我确定这个能工作" |
| 自己写 SKILL.md | "我知道格式，直接写" | 格式知识可能过时 | "格式我很熟"；"调度太慢了" |
| 跳过 Blind Comparison | "测试通过了，肯定比基线好" | 测试通过≠优于基线 | "TDD 都过了，还比什么" |
| 跳过 ai-doc-optimizer | "文档已经很清晰了" | 优化是必须的收敛过程 | "文档写得很好了" |
| TDD 失败后继续 | "再试一次可能就过了" | 必须 REFACTOR，不能重复失败 | "可能是偶然失败" |
| Blind Comparison 未达标继续 | "70% 太严格了" | 降低标准=降低质量 | "60% 也不错了" |
| 自己执行任务 | "这个很快，我直接做" | meta-skill 不执行，只调度 | "调度太慢，我自己写" |
| 有纪律强制标签但未应用增强 | "压力场景不重要" | 有标签时 TDD 必须融入压力测试、说辞捕获、漏洞封堵 | "压力测试没必要" |
| 以复杂为由绕过流程 | "meta-skill 太复杂了" | 跳过=不符合期望，必须重新来过；流程存在即因为跳过代价更高 | "太复杂了，让我直接帮你重新设计 xxx，基于你的需求" |

**核心原则**: 见 Overview + 硬性限制；各阶段技能/SubAgent/脚本均须调度，不可跳过。

---

## Failure Handling

| 类型/情况 | 处理 |
|-----------|------|
| 可修复 | 按错误信息修复后重试 |
| 需重构 | 返回 REFACTOR |
| 超过迭代上限 | 记录 `.test/iteration-N/failure.md`（失败阶段、错误信息、已尝试修复、建议）→ 人工审查 |
| 用户拒绝回答 | 基于已有信息继续，标记假设到 boundaries |
| 需求频繁变更 | 确定当前版本→继续→变更作为新迭代 |
| 范围扩大 | 提醒边界→新需求放入 out_of_scope |
| 类型模糊 | 默认技术技能型→REFACTOR 调整 |

---

## Verification

`wc -w skills/meta-skill/SKILL.md`；`ls skills/meta-skill/agents/ scripts/`  
**清单**: 意图澄清 ✓ / 类型判断 ✓ / TDD 通过 ✓ / Blind Comparison 通过 ✓ / 文档优化 ✓ / 打包 ✓
