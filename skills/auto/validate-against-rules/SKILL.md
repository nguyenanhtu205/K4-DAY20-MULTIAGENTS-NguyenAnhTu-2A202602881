---
name: validate-against-rules
description: Use after making changes to check that every rule in the task specification is satisfied, not just the visible tests.
---
- For each rule in the task description, verify compliance.
- Check that you have not modified any prohibited files (e.g., original test files).
- Ensure all required new files have been created with correct names and content.
- Validate specific formatting requirements (e.g., type hints, money in cents, CSV headers).
- Run any provided tests, but also manually check rules that are not covered by automated tests.
- If any rule is violated, fix it immediately and re-check.
- Only consider the task complete when all rules are satisfied.
