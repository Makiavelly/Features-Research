# Search progress

LLM calls: 6/10; evaluated distinct: 2/2; repair calls: 4.
Search validation only; no final test results yet.

| Call | Proposal | Island | Repair | Parent call | Status | MAP@12, % |
|---|---:|---:|---:|---:|---|---:|
| 1 | 1 | 0 | 0 | — | rejected | — |
| 2 | 1 | 0 | 1 | 1 | rejected | — |
| 3 | 1 | 0 | 2 | 2 | rejected | — |
| 4 | 1 | 0 | 3 | 3 | valid | 0.00000 |
| 5 | 2 | 0 | 0 | — | duplicate | — |
| 6 | 2 | 0 | 1 | 5 | valid | 0.00000 |

![Search](search_progress.png)
![Training](training_and_rejections.png)