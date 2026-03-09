# grading.json

**生产者**: `agents/grader.md`  
**消费者**: `scripts/aggregate_benchmark.py`

---

## 核心字段

| 字段 | 类型 | 用途 |
|------|------|------|
| `summary.pass_rate` | float | 断言通过率，用于计算 delta |
| `summary.passed` | int | 通过的断言数 |
| `summary.failed` | int | 失败的断言数 |
| `summary.total` | int | 总断言数 |

---

## 完整格式

```json
{
  "expectations": [
    {
      "text": "断言描述",
      "passed": true,
      "evidence": "证据引用"
    }
  ],
  "summary": {
    "passed": 8,
    "failed": 2,
    "total": 10,
    "pass_rate": 0.80
  },
  "execution_metrics": {
    "total_tool_calls": 15,
    "output_chars": 12450,
    "transcript_chars": 3200,
    "errors_encountered": 0
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "提取的声明",
      "type": "factual",
      "verified": true,
      "evidence": "验证证据"
    }
  ],
  "user_notes_summary": {
    "uncertainties": [],
    "needs_review": [],
    "workarounds": []
  },
  "eval_feedback": {
    "suggestions": [],
    "overall": "整体评估"
  }
}
```
