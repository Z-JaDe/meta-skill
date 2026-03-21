# Meta Skill

**创建完备且检索优化的自定义 AI 技能。** meta-skill 使用 **TDD + 反模式压力测试 + 双盲检测** 确保技能完备性，通过 **冗余移除 + 歧义澄清 + 渐进式披露** 最大化 AI 检索效率。

[English](README.md)

---

## 快速开始：创建你的第一个技能

```bash
# 在 Qwen Code 或 Claude Code 中，只需问：
"Create a skill for [你的需求]"
```

**示例：**
```
"Create a skill for automatic code review"
"Create a skill for writing unit tests"
"Create a skill for optimizing prompts"
```

meta-skill 将自动：

**确保完备性：**
1. **TDD** - 先写测试定义预期行为
2. **反模式压力测试** - 在压力场景下捕获并封堵漏洞
3. **双盲检测** - 验证候选方案显著优于基线

**优化 AI 检索：**
4. **歧义澄清** - 解析模糊语义
5. **冗余移除** - 消除重复内容
6. **渐进式披露** - 信息结构从简单到复杂

7. **打包** 为 `.skill` 文件即可使用

---

## 核心理念

**自演进：元技能使用自己的流程来创建和持续改进技能（包括它自己），直到收敛。**

`skills/` 目录包含 meta-skill 在创建流程中调用的内置技能库。

---

## 核心流程

```
意图发现 → 类型判断 → TDD 循环 → 双盲检测 → AI 检索优化 → 打包
```

README 仅保留轻量流程视图。

**唯一权威流程与硬门禁定义：**

- `skills/meta-skill/SKILL.md`

| 阶段（简版） | 主要组件 |
|--------------|----------|
| 意图发现 | `intent-discovery` |
| 类型判断 | `meta-skill` 阶段 2 判断（主类型 + 纪律强制标签） |
| TDD 循环 | `test-first` + `skill-format`（有纪律强制标签时再叠加 `anti-rationalization`） |
| 双盲检测 | `agents/{grader,comparator,analyzer}` + `scripts/aggregate_benchmark.py` |
| AI 检索优化 | `ai-doc-optimizer` |
| 打包 | `scripts/package_skill.py` |

### 术语中英文固定映射

| 中文 | English |
|------|---------|
| 意图发现 | Intent Discovery |
| 类型判断 | Type Decision |
| 双盲检测 | Blind Comparison |
| 反模式压力测试 | Anti-Rationalization Pressure Testing |
| 说辞 | Rationalization |
| 渐进式披露 | Progressive Disclosure |

---

## 技能系统架构

```
┌─────────────────────────────────────────────────────────────┐
│  skills/  (内置技能库)                                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  meta-skill/ (编排器)                                 │   │
│  │  - SKILL.md                                          │   │
│  │  - agents/ (grader, analyzer, comparator)            │   │
│  │  - scripts/ (package_skill.py, aggregate_benchmark)  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  子技能 (meta-skill 在流程中调用)                       │   │
│  │  - intent-discovery/  - test-first/                  │   │
│  │  - anti-rationalization/  - skill-format/            │   │
│  │  - ai-doc-optimizer/                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**注意**: 创建**新技能**时，输出到用户指定的目录（`~/.qwen/skills/`、`./` 等），而不是 `meta-skill/skills/`。

---

## 技能关系图

```mermaid
flowchart TB
    User[用户请求创建技能] --> Meta[meta-skill<br/>编排器]

    Meta --> ID[intent-discovery<br/>需求澄清]
    ID --> Meta

    Meta --> TF[test-first<br/>TDD 方法论]
    TF --> AR[anti-rationalization<br/>压力测试]
    AR --> TF
    TF --> SF[skill-format<br/>格式验证]
    SF --> TF

    Meta --> AO[ai-doc-optimizer<br/>迭代优化]
    AO --> AO

    subgraph Flow[创建流程]
        ID
        TF
        AO
    end

    subgraph Support[支持技能]
        AR
        SF
    end

    Meta --> Flow
    Flow --> Support
```

---

## 技能列表

### 内置技能库

这些技能协作创建新技能：

| 技能 | 在技能创建中的角色 |
|------|-------------------|
| `meta-skill` | **编排器** — 协调整个技能创建流水线 |
| `intent-discovery` | **需求分析师** — 渐进式提问澄清模糊需求 |
| `test-first` | **TDD 引擎** — 先写测试确保正确性 |
| `anti-rationalization` | **质量保证** — 压力测试规则防止漏洞 |
| `skill-format` | **验证器** — 确保 SKILL.md 遵循正确格式 |
| `ai-doc-optimizer` | **优化器** — 迭代优化文档供 AI 高效读取 |

### 技能如何协作

当你让 meta-skill 创建新技能时：

```
用户请求 → intent-discovery → 类型判断
           → test-first + skill-format（按需叠加 anti-rationalization）
           → 双盲检测 → ai-doc-optimizer → 打包
```

每个子技能处理创建过程的特定方面，确保最终技能：
- **定义清晰**（需求明确）
- **测试覆盖**（TDD 驱动）
- **健壮可靠**（抗说辞压力测试）
- **文档完善**（AI 读取优化）
- **格式正确**（格式验证通过）

---

## 自演进

`skills/` 中的所有技能都通过 meta-skill 流程创建和维护：

```
v0.1: 单一体化技能（500+ 行，复杂）
    ↓ TDD + 拆分 (通过 meta-skill)
v0.2: 拆分为专注的子技能
    ↓ 重构 (通过 meta-skill)
v0.3: 移除冗余，澄清歧义
    ↓ 收敛 (通过 meta-skill)
v1.0: 最终优化版本
```

**核心洞察**：meta-skill 使用它编排的相同流程来进化自己和子技能。

---

## 目录结构

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

**注意**：`skills/` 包含 meta-skill 的内置技能库。通过 meta-skill 创建的新技能放在用户指定的目录中（如 `~/.qwen/skills/`、`./`），而不是 `meta-skill/skills/`。

---

## 扩展支持

本项目同时支持 **Claude Code Plugin**、**Qwen Code Extension** 和 **Cursor Plugin**。

### 安装方式

**Claude Code：**
```bash
/plugin marketplace add https://github.com/Z-JaDe/meta-skill
/plugin install meta-skill
```

**Qwen Code：**
```bash
# 从远程 URL 安装
qwen extensions install https://github.com/Z-JaDe/meta-skill

# 或链接本地扩展（开发模式）
qwen extensions link /path/to/meta-skill
```

**Cursor：**

在 Cursor Agent 聊天中，从市场安装：

```text
/plugin-add meta-skill
```

### 配置文件

| 平台 | 配置文件 |
|------|---------|
| Claude Code | `.claude-plugin/marketplace.json` |
| Qwen Code | `qwen-extension.json` |
| Cursor | `.cursor-plugin/plugin.json` |

---

## 贡献指南

请按 `CONTRIBUTING.md` 执行贡献动作，包含：

- 新人最小路径，
- 修改后必须执行 `quick_validate.py`，
- `.test/` 产物策略，
- 插件元数据发布同步清单，
- `check_plugin_metadata.py` 自动一致性检查。

---

## 许可证

MIT（见 `LICENSE`）

---

## 致谢

本项目受到以下项目启发：

- **Anthropic 的 `skill-creator`** - 技能创建方法论
- **Superpowers 的 `writing-skills`** - 技能编写模式
