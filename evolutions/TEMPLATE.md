# Evolution v{版本号}

**迭代次数**：默认 3 次（可指定）

**外部测试集**：5-10 个 `.repo` 中的 Skill

---

## 迭代记录

### Iteration N

**输入版本**：v{版本号}-draft-N
**基准版本**：iteration-1 基于原始 SKILL.md，iteration-2+ 基于 iteration-(N-1) 修补后的版本

| Skill | 触发条件 | TDD 结果 | 问题 |
|-------|---------|---------|------|
| test-skill-a | "XXX" | ❌ → ✅ | |
| test-skill-b | "XXX" | ✅ | - |
| test-skill-c | "XXX" | ❌ → ✅ | |

**发现的问题**（SKILL.md 草案的漏洞）：

**REFACTOR**（修补 SKILL.md 草案）：- [ ]

**回归用例**：- [ ] case-XXX-*.md:

---

## 结论

**总迭代次数**：N | **提前终止**：是/否

**最终状态**：
- [ ] 所有迭代测试通过
- [ ] 回归测试通过
- [ ] 外部测试集通过
- [ ] 已更新 `skills/meta-skill/SKILL.md`
- [ ] 准备提交 PR
