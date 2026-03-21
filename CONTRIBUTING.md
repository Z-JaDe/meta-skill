# 贡献指南（最小路径）

本文件只定义贡献时的最小必需动作，避免流程分歧。

## 0) 先看哪里

1. 先读 `skills/meta-skill/SKILL.md`（唯一权威流程）
2. 再看 `README.md` / `README_CN.md`（轻量介绍）
3. 按目标修改对应技能目录下的 `SKILL.md`

## 1) 修改一个 Skill 的标准步骤

1. 修改 `skills/<skill-name>/SKILL.md`
2. 本地校验（必须）：

```bash
python3 skills/meta-skill/scripts/quick_validate.py skills/<skill-name>
```

3. 如需打包，执行：

```bash
python3 skills/meta-skill/scripts/package_skill.py skills/<skill-name> ./dist
```

## 2) `.test/` 策略（固定）

- `.test/` 为本地评测产物目录，默认不提交（已在 `.gitignore` 忽略）
- 需要长期保留的示例资产，不放 `.test/`，请放到明确目录（如 `Resources/` 或技能目录下独立样例文件）
- PR 前请确认没有误提交本地评测产物

## 3) 插件元数据发布同步清单（必须逐项勾选）

涉及发布时，请同步检查以下文件中的重复字段：

- `.claude-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `qwen-extension.json`

必查字段：

- `version`
- `description`
- `homepage` / `repository`（若该文件定义了这些字段）
- `license`（若该文件定义了该字段）

建议先执行自动检查，再做人工复核：

```bash
python3 scripts/check_plugin_metadata.py
python3 scripts/check_plugin_metadata.py --strict-optional
```

## 4) 文档维护边界

- `README.md` / `README_CN.md`：只保留简版流程，不再复制完整阶段细节
- 流程细节、门禁、路径契约统一维护在 `skills/meta-skill/SKILL.md`
