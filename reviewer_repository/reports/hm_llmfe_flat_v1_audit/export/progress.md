# Search progress

LLM calls: 23/300; evaluated distinct: 20/20; repair calls: 3.
Search validation only; no final test results yet.

| Call | Proposal | Island | Repair | Parent call | Status | MAP@12, % |
|---|---:|---:|---:|---:|---|---:|
| 1 | 1 | 0 | 0 | — | valid | 0.77540 |
| 2 | 2 | 0 | 0 | — | valid | 0.77056 |
| 3 | 3 | 0 | 0 | — | valid | 0.94267 |
| 4 | 4 | 1 | 0 | — | valid | 0.74542 |
| 5 | 5 | 1 | 0 | — | valid | 0.72976 |
| 6 | 6 | 1 | 0 | — | rejected | — |
| 7 | 6 | 1 | 1 | 6 | rejected | — |
| 8 | 6 | 1 | 2 | 7 | rejected | — |
| 9 | 6 | 1 | 3 | 8 | valid | 0.71110 |
| 10 | 7 | 2 | 0 | — | valid | 0.71919 |
| 11 | 8 | 2 | 0 | — | valid | 0.70256 |
| 12 | 9 | 2 | 0 | — | valid | 0.73505 |
| 13 | 10 | 2 | 0 | — | valid | 0.75531 |
| 14 | 11 | 2 | 0 | — | valid | 0.71544 |
| 15 | 12 | 2 | 0 | — | valid | 0.70158 |
| 16 | 13 | 1 | 0 | — | valid | 0.72571 |
| 17 | 14 | 1 | 0 | — | valid | 0.77698 |
| 18 | 15 | 1 | 0 | — | valid | 0.66293 |
| 19 | 16 | 0 | 0 | — | valid | 0.83593 |
| 20 | 17 | 0 | 0 | — | valid | 0.87515 |
| 21 | 18 | 0 | 0 | — | valid | 0.89136 |
| 22 | 19 | 0 | 0 | — | valid | 0.82133 |
| 23 | 20 | 0 | 0 | — | valid | 0.76721 |

![Search](search_progress.png)
![Training](training_and_rejections.png)