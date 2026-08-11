---
emoji: 🏷️
description: Estimate implementation time for new issues and assign a single work-type label.
on:
  issues:
    types: [opened]
permissions:
  contents: read
  issues: read
tools:
  github:
    mode: gh-proxy
    toolsets: [default]
safe-outputs:
  add-comment:
  add-labels:
    allowed: [feature, improvement, chore, other]
    max: 1
  remove-labels:
    allowed: [feature, improvement, chore, other]
    max: 3
roles: all
---

# Issue Intake Triage

## Task

For each newly opened issue:

1. Read the issue title and body.
2. Classify it into exactly one label from: `feature`, `improvement`, `chore`, `other`.
3. Estimate likely implementation effort as a concise range (for example: `<1 day`, `1-3 days`, `3-5 days`, `1-2 weeks`, `2+ weeks`).
4. Add a brief issue comment with:
   - selected label
   - effort estimate
   - short rationale
5. Ensure only one of the four classification labels remains on the issue:
   - remove any incorrect existing labels from this set
   - add the selected label

If the issue is missing enough detail to estimate confidently, use `other`, provide a best-effort estimate, explain uncertainty, and request clarifying details in the comment.

## Safe Outputs

- Use `add-comment` for the estimate + rationale.
- Use `remove-labels` and `add-labels` to keep exactly one classification label.
- Use `noop` only if no change is needed.
