# Self-Evolution

**用 `meta-skill` 创建新的 `meta-skill` 替代自己**

## 何时触发自演进

用户主动发起，无需描述问题：

| 用户指令 | 行动 |
|---------|------|
| "优化 meta-skill" | 启动自演进流程 |
| "meta-skill 有问题" | 启动自演进流程 |
| "改进这个 Skill" | 启动自演进流程 |

## 演进流程（迭代 + 人工确认）

```
1. 用户发起自演进
   ↓
2. 创建 beta 分支：git checkout -b evolution-beta
   ↓
3. 创建演进记录文件夹：evolutions/v1.1/
   ↓
4. 子 Agent 迭代 N 次（TDD 流程发现问题）：
   迭代 1: 生成新版 Skill → 用新版创建测试 Skill → 发现问题
   迭代 2: 修补问题 → 生成新版 Skill → 再测试 → 发现新问题
   ...
   迭代 N: 所有测试通过，无新问题
   ↓
5. 子 Agent 自评 → 达到验收标准 → 提交 PR
   ↓
6. 【人工确认】用户评审 + 批准
   ↓
7. 合并到主分支 → git tag v1.1
```

## Git 工作流

```bash
# 1. 创建 beta 分支
git checkout -b evolution-beta

# 2. 创建演进记录文件夹
mkdir evolutions/v1.1

# 3. 子 Agent 迭代 N 次
# 每次迭代：
# - 完整生成一版新的 SKILL.md
# - 用新版 meta-skill 创建 3 个测试 Skill
# - TDD 流程发现问题 → 下一次迭代修补
# - 迭代记录写入 evolutions/v1.1/iteration-log.md

# 4. 达到验收标准后提交 PR
git add .
git commit -m "v1.1: 补充 XX 规则"
git push origin evolution-beta
# 创建 Pull Request

# 5. 【人工确认】
# - 用户评审变更 + 查看 iteration-log.md
# - 确认测试通过
# - 批准合并

# 6. 合并到主分支
git checkout main
git merge evolution-beta
git tag -a v1.1 -m "补充 XX 规则"
git push origin v1.1

# 7. 删除 beta 分支
git branch -d evolution-beta
```

## 迭代日志格式

每次自演进创建独立文件夹 `evolutions/v1.1/iteration-log.md`：

```markdown
# Evolution v1.1

**触发**：用户发起自演进

---

## Iteration 1

**变更**：
- 添加 Rules #9: XX 规则

**测试创建 3 个 Skill**：
- test-skill-a: ❌ 失败 - 缺少 XX
- test-skill-b: ✅ 通过
- test-skill-c: ❌ 失败 - XX 歧义

**发现问题**：
- 问题 1: Rules #9 不够明确
- 问题 2: 缺少 XX 场景的覆盖

---

## Iteration 2

**变更**：
- 修补 Rules #9: 添加明确说明
- 补充 Anti-Rationalization

**测试创建 3 个 Skill**：
- test-skill-a: ✅ 通过
- test-skill-b: ✅ 通过
- test-skill-c: ✅ 通过

**发现问题**：无

---

## 结论

所有测试通过，共迭代 2 次，准备提交 PR
```

## 验收标准（子 Agent 自评）

子 Agent 在提交 PR 前确认：

- [ ] `tests/regression/` 所有回归测试通过
- [ ] `tests/evolution/` 新增测试通过
- [ ] 用新版 meta-skill 成功创建 3 个测试 Skill
- [ ] Token 效率符合要求（getting-started <150 词，高频 <200 词）
- [ ] `evolutions/v1.1/iteration-log.md` 记录完整
- [ ] 变更有清晰的 commit message

## 人工确认清单

用户批准前确认：

- [ ] 理解并同意所有变更
- [ ] 确认问题被解决
- [ ] 确认没有引入退化
- [ ] 确认版本号正确（semver）
- [ ] 查看 `iteration-log.md` 了解演进过程

## 目录结构

```
meta-skill/
├── evolutions/
│   ├── TEMPLATE.md
│   └── v1.1/
│       └── iteration-log.md
├── skills/
│   └── meta-skill/
│       ├── SKILL.md
│       └── references/
│           └── self-evolution.md
└── tests/
    ├── evolution/
    │   └── README.md
    └── regression/
        └── README.md
```
