# benchmark.json

**生产者**: `scripts/aggregate_benchmark.py`  
**消费者**: `agents/analyzer.md`, 用户

---

## 核心字段

| 字段 | 类型 | 用途 |
|------|------|------|
| `run_summary.with_skill.pass_rate.mean` | float | 带技能配置的平均通过率 |
| `run_summary.without_skill.pass_rate.mean` | float | 不带技能配置的平均通过率 |
| `run_summary.delta.pass_rate` | string | 通过率差异（如 "+0.25"） |

---

## 完整格式

```json
{
  "metadata": {
    "skill_name": "skill-name",
    "skill_path": "skills/skill-name/SKILL.md",
    "executor_model": "model-name",
    "analyzer_model": "model-name",
    "timestamp": "2026-03-09T12:00:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },
  "runs": [
    {
      "eval_id": 1,
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.80,
        "passed": 8,
        "failed": 2,
        "total": 10,
        "time_seconds": 45.2,
        "tokens": 12000,
        "tool_calls": 15,
        "errors": 0
      },
      "expectations": [...],
      "notes": []
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {
        "mean": 0.85,
        "stddev": 0.05,
        "min": 0.80,
        "max": 0.90
      },
      "time_seconds": {
        "mean": 45.2,
        "stddev": 5.1,
        "min": 40.0,
        "max": 50.5
      },
      "tokens": {
        "mean": 12000,
        "stddev": 1000,
        "min": 11000,
        "max": 13000
      }
    },
    "without_skill": {
      "pass_rate": {"mean": 0.60, "stddev": 0.10, "min": 0.50, "max": 0.70},
      "time_seconds": {"mean": 32.7, "stddev": 3.2, "min": 30.0, "max": 36.0},
      "tokens": {"mean": 10000, "stddev": 800, "min": 9200, "max": 10800}
    },
    "delta": {
      "pass_rate": "+0.25",
      "time_seconds": "+12.5s",
      "tokens": "+2000"
    }
  },
  "notes": []
}
```
