# Meta Skill

一个用于创建和管理 Skill 的元技能系统。

## 核心理念

**测试不通过，禁止创建或更新 Skill。**

## 核心流程

```
DISCOVERY → RED → GREEN → REFACTOR
```

| 阶段 | 说明 |
|------|------|
| **DISCOVERY** | 渐进式提问明确 Skill 定位、职责、边界 |
| **RED** | 记录无 Skill 时的失败场景 |
| **GREEN** | 写最小 Skill 通过测试 |
| **REFACTOR** | 用 Rules 检查漏洞并修补 |

## 目录结构

```
meta-skill/
├── skills/
│   └── meta-skill/        # 元技能本身
│       ├── SKILL.md
│       └── references/
│           └── self-evolution.md
├── evolutions/            # 自演进记录
│   └── TEMPLATE.md
└── tests/
    ├── evolution/         # 演进测试
    └── regression/        # 回归测试
```

## 自演进

`meta-skill` 可以用自身流程优化自己。详见 `skills/meta-skill/references/self-evolution.md`。

## 使用方式

当需要创建或修改 Skill 时，`meta-skill` 会自动触发：
1. 提问澄清需求（触发条件、职责、边界等）
2. 建议命名和目录结构
3. 执行 TDD 流程创建/修改 Skill
