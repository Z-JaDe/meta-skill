# Self-Evolution

**用 `meta-skill` 创建新的 `meta-skill` 替代自己**

## 触发条件

用户指令："优化 meta-skill"、"meta-skill 有问题"、"改进这个 Skill"

## 核心概念

**一次迭代** = 基于当前 SKILL.md 生成新版草案 → 创建 3 个测试 Skill 验证 → TDD 发现 SKILL.md 的漏洞 → 修补 SKILL.md 草案 → 记录到 log.md

**核心原则**：
- 测试 Skill 用于暴露 SKILL.md 的漏洞，是手段不是目的
- 每次迭代使用不同的 3 个测试 Skill（避免路径依赖）
- 每次迭代结束时，SKILL.md 草案已修复当轮发现的问题

## 演进流程

```
1. 用户发起自演进（可指定迭代次数，默认 3 次）
   ↓
2. 确定版本号（如 v1.1），创建 beta 分支：git checkout -b evolution-v{版本号}
   ↓
3. 创建演进记录文件夹：evolutions/v{版本号}/
   ↓
4. 【检查外部测试集】确认 `.repo` 目录存在
   - 如不存在或为空 → **终止自演进**
   - 如存在 → 从 `.repo` 中选取 5-10 个有代表性的 Skill（覆盖不同领域）作为外部测试集
   ↓
5. 子 Agent 迭代 N 次（或提前终止）：
   每次迭代（iteration-1, iteration-2...）：
   a) 生成草案：
      - iteration-1: 基于原始 skills/meta-skill/SKILL.md 生成草案
      - iteration-2+: 基于 iteration-(N-1) 修补后的 SKILL.md 草案生成新版
      - 输出：evolutions/v{版本号}/iteration-N/SKILL.md
   b) 创建测试：
      - 创建 3 个测试 Skill 到 evolutions/v{版本号}/iteration-N/test-skill-{a,b,c}/
      - 要求：覆盖不同领域，与之前迭代不重复
   c) TDD 验证：
      - 用新版 SKILL.md 草案创建测试 Skill
      - 如失败 → 记录漏洞 → 修补 SKILL.md 草案 → 重新验证
   d) 记录：
      - 填写 evolutions/v{版本号}/iteration-N/log.md
      - 如发现新漏洞类型 → 创建回归用例 tests/regression/case-XXX-*.md
   ↓
6. 达到指定次数 OR 提前终止：
   - 提前终止：连续 2 次迭代未发现新漏洞类型
   - 判断：如 iteration-N 和 iteration-(N+1) 均无新漏洞 → 在 iteration-(N+1) 后终止
   - 示例：iteration-1 有漏洞，iteration-2 和 iteration-3 无 → 在 iteration-3 后终止
   ↓
7. 【子 Agent 自评】
   - 运行 tests/regression/ 所有回归用例 → 必须全部通过
   - 用新版 SKILL.md 创建外部测试集中的 Skill → 必须全部成功
   - 确认验收标准 → 提交 PR
   ↓
8. 【人工确认】用户评审变更 + 批准
   ↓
9. 合并到主分支 → git tag v{版本号} → 更新 skills/meta-skill/SKILL.md
```

## 终止条件

- ✅ 达到指定迭代次数（默认 3 次）
- ✅ **提前终止**：连续 2 次迭代未发现新漏洞类型
- ⚠️ 发现架构级问题（SKILL.md 结构需要重构） → 升级版本号（minor → major）

## 目录结构

```
meta-skill/
├── .repo/                       # 外部 Skill 仓库（已忽略）
├── evolutions/
│   ├── TEMPLATE.md
│   └── v{版本号}/
│       └── iteration-N/
│           ├── test-skill-{a,b,c}/  # 测试 Skill
│           └── log.md               # 迭代记录
├── skills/meta-skill/
│   ├── SKILL.md                 # 当前版本（迭代完成后更新）
│   └── references/self-evolution.md
└── tests/regression/
    ├── README.md
    └── case-001-*.md            # 回归用例
```

**关键说明**：
- **版本号**：自演进开始时确定（小改动→v1.1，架构重构→v2.0）
- **回归用例**：连续编号，发现新漏洞类型时创建
- **最终版本**：迭代完成后直接更新 `skills/meta-skill/SKILL.md`

## 回归测试用例管理

**原则**：每个用例代表一个方向/场景，不重复；发现新漏洞类型时创建回归用例；定期清理重复。

## 迭代日志格式

`evolutions/v{版本号}/iteration-N/log.md`：

```markdown
# Iteration N

**输入版本**：v{版本号}-draft-N

| Skill | 触发条件 | TDD 结果 | 问题 |
|-------|---------|---------|------|
| test-skill-a | "XXX" | ❌ → ✅ | |
| test-skill-b | "XXX" | ✅ | - |
| test-skill-c | "XXX" | ❌ → ✅ | |

## 发现的问题（SKILL.md 草案的漏洞）

1.

## REFACTOR 行动（修补 SKILL.md 草案）

- [ ]

## 回归用例创建

- [ ] case-0XX-*.md: [说明]
```

## 验收标准

- [ ] 完成指定迭代次数 **或** 提前终止
- [ ] 每次迭代的 3 个测试 Skill 全部通过 TDD
- [ ] 新漏洞类型已创建回归用例
- [ ] `tests/regression/` 所有回归用例通过
- [ ] 外部测试集全部通过（用新版 SKILL.md 创建这些 Skill，验证能成功）
- [ ] Token 效率符合要求（getting-started <150 词，高频 <200 词）
- [ ] 迭代记录完整
- [ ] 变更有清晰的 commit message

## 测试 Skill 设计要求

每次迭代创建的 3 个测试 Skill 应覆盖不同领域，模拟真实用户需求，与之前迭代不重复。
