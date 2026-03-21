# comparison_result.json

**生产者**: `agents/comparator.md`  
**消费者**: meta-skill 判断逻辑

---

## 核心字段

| 字段 | 类型 | 用途 |
|------|------|------|
| `winner` | string | "A" 或 "B"（禁止 TIE） |
| `winner_role` | string | `"primary"` 或 `"baseline"` |
| `winner_is_primary` | boolean | true 表示赢家属于 primary 角色 |
| `reasoning` | string | 选择理由 |

---

## 完整格式

```json
{
  "winner": "A",
  "winner_role": "primary",
  "winner_is_primary": true,
  "reasoning": "Output A provides a complete solution with proper formatting and all required fields.",
  "rubric": {
    "A": {
      "content": {
        "correctness": 5,
        "completeness": 5,
        "accuracy": 4
      },
      "structure": {
        "organization": 4,
        "formatting": 5,
        "usability": 4
      },
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {"correctness": 3, "completeness": 2, "accuracy": 3},
      "structure": {"organization": 3, "formatting": 2, "usability": 3},
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["Complete solution", "Well-formatted", "All fields present"],
      "weaknesses": ["Minor style inconsistency in header"]
    },
    "B": {
      "score": 5,
      "strengths": ["Readable output", "Correct basic structure"],
      "weaknesses": ["Missing date field", "Formatting inconsistencies"]
    }
  },
  "expectation_results": {
    "A": {
      "passed": 8,
      "total": 10,
      "pass_rate": 0.80,
      "details": [{"text": "...", "passed": true}]
    },
    "B": {
      "passed": 6,
      "total": 10,
      "pass_rate": 0.60,
      "details": [{"text": "...", "passed": true}]
    }
  }
}
```
