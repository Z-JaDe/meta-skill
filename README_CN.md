# Meta Skill

一个自进化的技能系统：meta-skill 编排 **TDD 驱动 → 双盲检测 → AI 检索优化** 流水线，迭代创建和进化技能。

---

## 核心理念

**自演进：元技能使用自己的流程来创建和持续改进技能（包括它自己），直到收敛。**

`skills/` 目录包含 meta-skill 在创建流程中调用的内置技能库。

---

## 核心流程

```
意图发现 → TDD 驱动 (RED-GREEN-REFACTOR + Anti-Rationalization) → 双盲检测 → AI 检索优化 → 打包部署
```

| 阶段 | 技能 | 说明 |
|------|------|------|
| **意图发现** | `intent-discovery` | 渐进式提问澄清模糊需求，输出 `output_dir` 和技能类型 |
| **TDD 驱动** | `test-first` + `anti-rationalization` | **RED**: 设计压力场景 + 捕获说辞 → **GREEN**: 说服原则加固 + 漏洞封堵 → **REFACTOR**: 重测验证直到无新说辞 |
| **双盲检测** | `agents/{grader,comparator,analyzer}` | 盲评 candidate vs baseline，验证显著优于基线（选择率>70% AND 通过率提升>20%） |
| **AI 检索优化** | `ai-doc-optimizer` | 迭代优化直到收敛（连续 2 轮语义等价或 max_iterations=5） |
| **打包部署** | `scripts/package_skill.py` | 生成 `.skill` 文件，验证：行数<500、Mermaid 流程图、kebab-case 命名 |

**Anti-Rationalization 融入 TDD**:
| TDD 阶段 | Anti-Rationalization 策略 |
|---------|--------------------------|
| **RED** | 设计≥3 种压力叠加场景，对抗测试捕获说辞（逐字记录） |
| **GREEN** | 用说服原则加固（权威 + 承诺 + 社会证明），封堵漏洞（No exceptions + 逐一禁止） |
| **REFACTOR** | 重测验证，发现新说辞→继续加固，直到无新说辞 |

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

| 技能 | 描述 |
|------|------|
| `meta-skill` | **编排器** — 协调技能创建/演进流程 |
| `intent-discovery` | 通过渐进式提问澄清模糊需求 |
| `test-first` | TDD 方法论：先写测试再实现 |
| `anti-rationalization` | 压力测试规则并封堵合理化漏洞 |
| `skill-format` | 格式化和验证 SKILL.md 文件 |
| `ai-doc-optimizer` | 通过迭代收敛优化文档供 AI 高效读取 |

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

### Claude Code Plugin

本项目是一个 **Claude Code Plugin**，提供自进化的技能系统用于创建新技能。

**安装方式：**
```bash
/plugin marketplace add https://github.com/Z-JaDe/meta-skill
/plugin install meta-skill
```

### Qwen Code Extension

本项目是一个 **Qwen Code Extension**，提供自进化的技能系统用于创建新技能。

**安装方式：**
```bash
# 从远程 URL 安装
qwen extensions install https://github.com/Z-JaDe/meta-skill

# 或链接本地扩展（开发模式）
qwen extensions link /path/to/meta-skill
```

**使用方法：**

安装后，通过以下提问创建新技能：

```
Create a skill for [你的需求]
```

meta-skill 将自动编排：
1. **意图发现** - 渐进式提问澄清需求
2. **TDD 驱动** - 先写测试，再实现并压力测试
3. **双盲检测** - 对比候选与基线
4. **AI 优化** - 迭代优化直到收敛
5. **打包部署** - 生成验证后的 `.skill` 文件

### 配置文件

| 平台 | 配置文件 |
|------|---------|
| Claude Code | `.claude-plugin/marketplace.json` |
| Qwen Code | `qwen-extension.json` |

---

## 许可证

MIT

---

## 致谢

本项目受到以下项目启发：

- **Anthropic 的 `skill-creator`** - 技能创建方法论
- **Superpowers 的 `writing-skills`** - 技能编写模式
