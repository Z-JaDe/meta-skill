# Meta-Skill 迭代提示词

**用途**：通过多 Agent 对比评估，迭代优化 meta-skill

---

## 核心流程

```
1. 4 个参赛者用各自方法创建同样的 2 个测试 Skill
   ↓
2. 对比 8 个测试 Skill 的质量 → 评估 4 个方法的优劣
   ↓
3. meta-skill 向最佳方法学习 → 生成优化建议 → 确认更新
```

---

## 第 1 步：4 个参赛者创建 5 个测试 Skill

### 参赛者

| # | 方法 | 参考路径 |
|---|------|----------|
| A | 当前 meta-skill | `skills/meta-skill/SKILL.md` |
| B | writing-skills | `.repo/superpowers/skills/writing-skills/SKILL.md` |
| C | skill-creator (Anthropic) | `.repo/anthropics-skills/skills/skill-creator/SKILL.md` |
| D | skill-creator (OpenAI) | `.repo/openai-skills/skills/.system/skill-creator/SKILL.md` |

### 测试集（动态选择 2 个）

**选择标准**：
- 覆盖不同领域
- 复杂度分布：简单 (30%)、中等 (40%)、复杂 (30%)
- 从 `.repo` 中随机选取，增加变数

**示例池**：
| Skill | 领域 | 复杂度 |
|-------|------|--------|
| `pdf` | 文件处理 | 简单 |
| `xlsx` | 数据处理 | 中等 |
| `docx` | 文档处理 | 中等 |
| `test-driven-development` | 开发流程 | 复杂 |
| `systematic-debugging` | 调试 | 中等 |
| `mcp-builder` | 工具构建 | 复杂 |
| `frontend-design` | UI 设计 | 中等 |
| `webapp-testing` | 测试 | 复杂 |
| `algorithmic-art` | 创意编程 | 复杂 |

**每次迭代从池中随机选 2 个，确保不重复**

### 执行方式

4 个子 Agent 各自独立：
- 用指定的方法创建同样的 5 个测试 Skill
- 记录创建时间、Token 消耗
- 输出到各自目录

### 输出结构

```
evolutions/v{version}/
├── contestant-A-meta/
│   └── test-skills/
│       ├── pdf/SKILL.md
│       ├── xlsx/SKILL.md
│       └── ...
├── contestant-B-writing-skills/
│   └── test-skills/
│       ├── pdf/SKILL.md
│       ├── xlsx/SKILL.md
│       └── ...
├── contestant-C-anthropic-skill-creator/
│   └── test-skills/
│       ├── pdf/SKILL.md
│       ├── xlsx/SKILL.md
│       └── ...
└── contestant-D-openai-skill-creator/
    └── test-skills/
        ├── pdf/SKILL.md
        ├── xlsx/SKILL.md
        └── ...
```

---

## 第 2 步：对比评估

主 Agent 对比 20 个测试 Skill 的质量，评估 4 个方法的优劣：

### 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 触发条件准确性 | 20% | description 是否准确定义触发场景 |
| 边界案例覆盖 | 15% | 是否明确定义不应触发的场景 |
| 结构规范性 | 15% | 是否符合 Skill 结构规范 |
| 可执行性 | 15% | 示例是否可运行，步骤是否清晰 |
| Token 效率 | 10% | getting-started <150 词 |
| 漏洞封闭 | 10% | 是否有反理性化/边界测试 |
| 创建效率 | 5% | 时间和 Token 消耗 |

### 输出

```markdown
## 对比结果

| 参赛者 | 测试 Skill 平均分 | 排名 |
|--------|------------------|------|
| A (当前 meta-skill) | X.X | #? |
| B (writing-skills) | X.X | #? |
| C (Anthropic skill-creator) | X.X | #? |
| D (OpenAI skill-creator) | X.X | #? |

## 各参赛者优势
- A: ...
- B: ...
- C: ...
- D: ...
```

---

## 第 3 步：meta-skill 向最佳方法学习

### 优化建议格式

```markdown
## meta-skill 优化建议

### 当前优势（保持）
- ...

### 向冠军学习（第 1 名的方法）
1. ...
2. ...

### 向其他参赛者学习（可借鉴的实践）
- 来自 B: ...
- 来自 C: ...
- 来自 D: ...

### 优先级
- **P0**（必须）：...
- **P1**（重要）：...
- **P2**（可选）：...
```

### 用户确认

在应用前必须确认：
- [ ] 展示变更对比（diff）
- [ ] 说明每条变更的理由
- [ ] 用户明确批准

### 执行更新

```bash
# 1. 创建 beta 分支
git checkout -b meta-skill-v{next}

# 2. 应用优化
# 3. 运行回归测试
# 4. 用户评审
# 5. 合并到主分支
# 6. 打标签
```

---

## 使用示例

**用户指令**：
```
迭代优化 meta-skill，用多方法对比
```

**Agent 响应**：
```
我将执行以下流程：

1. 4 个参赛者创建 2 个测试 Skill
   - A: 当前 meta-skill
   - B: writing-skills 方法
   - C: Anthropic skill-creator 方法
   - D: OpenAI skill-creator 方法

2. 对比 8 个测试 Skill 的质量 → 评估 4 个方法

3. meta-skill 向最佳方法学习 → 生成优化建议

预计耗时：15-20 分钟
是否继续？ [Y/n]
```
