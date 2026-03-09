# analysis_result.json

**生产者**: `agents/analyzer.md`  
**消费者**: meta-skill REFACTOR 阶段

---

## 核心字段

| 字段 | 类型 | 用途 |
|------|------|------|
| `improvement_suggestions[]` | array | 改进建议列表，用于 REFACTOR |

---

## 完整格式

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "skills/my-skill/SKILL.md",
    "loser_skill": "skills/old-skill/SKILL.md",
    "comparator_reasoning": "Output A had complete formatting and all fields"
  },
  "winner_strengths": [
    "明确的 5 步流程指令",
    "包含 validate_output.py 脚本捕获格式错误",
    "OCR 失败时的 fallback 指导"
  ],
  "loser_weaknesses": [
    "'适当处理文档'指令模糊导致不一致行为",
    "缺少验证脚本，agent 自己 improvis 出错",
    "无 OCR 失败指导，agent 直接放弃"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": ["跳过可选日志步骤"]
    },
    "loser": {
      "score": 6,
      "issues": ["未使用技能模板", "自创方法"]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "将'适当处理'替换为明确步骤：1) 提取文本 2) 识别章节 3) 按模板格式化",
      "expected_impact": "消除导致不一致行为的歧义"
    },
    {
      "priority": "high",
      "category": "tools",
      "suggestion": "添加 validate_output.py 脚本",
      "expected_impact": "在最终输出前捕获格式错误"
    },
    {
      "priority": "medium",
      "category": "error_handling",
      "suggestion": "添加 fallback 指令：'如果 OCR 失败，尝试：1) 不同分辨率 2) 图像预处理 3) 手动提取'",
      "expected_impact": "防止困难文档早期失败"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "读取技能→遵循 5 步流程→使用验证脚本→修复 2 个问题→输出",
    "loser_execution_pattern": "读取技能→不明确方法→尝试 3 种不同方法→无验证→输出有错误"
  }
}
```
