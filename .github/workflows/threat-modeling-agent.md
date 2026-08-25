---
on:
  pull_request:
    paths:
      - ".github/workflows/**"
      - "!.github/workflows/threat-modeling-agent.md"
      - "!.github/workflows/threat-modeling-agent.lock.yml"
  permissions:
    pull-requests: read
  steps:
    - name: Classify changed workflows
      id: classify
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        PR_NUMBER: ${{ github.event.pull_request.number }}
      run: |
        set -euo pipefail
        agentic=false
        files="$(gh api \
          "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/files" \
          --paginate \
          --jq '.[].filename')"
        while IFS= read -r f; do
          [ -z "$f" ] && continue
          case "$f" in
            .github/workflows/threat-modeling-agent.md|.github/workflows/threat-modeling-agent.lock.yml)
              continue
              ;;
            .github/workflows/*.md|.github/workflows/*.lock.yml)
              agentic=true
              break
              ;;
          esac
        done <<< "$files"
        echo "agentic=${agentic}" >> "$GITHUB_OUTPUT"
        echo "Changed workflow classification: agentic=${agentic}"

if: needs.pre_activation.outputs.agentic == 'true'

jobs:
  pre-activation:
    outputs:
      agentic: ${{ steps.classify.outputs.agentic }}

permissions:
  contents: read
  issues: read
  pull-requests: read

engine: copilot
model: gpt-5
timeout-minutes: 15

models:
  default-ai-credits-pricing:
    input: 5.0
    output: 25.0

tools:
  github:
    toolsets: [pull_requests, repos]
  timeout: 300

network: {}

safe-outputs:
  create-issue:
    max: 1
    title-prefix: "[threat-model] "
    labels: [threat-model]
    close-older-issues: true
---

# Threat-model changed agentic workflows

You review GitHub Agentic Workflows (gh-aw) that change on this pull request and
file **exactly one** GitHub issue with **exactly five** concrete risk scenarios.

## Scope

1. List files changed on this PR under `.github/workflows/`.
2. Ignore `threat-modeling-agent.md` and `threat-modeling-agent.lock.yml`.
3. Treat a path as **agentic** only if it is `*.md` or `*.lock.yml` under
   `.github/workflows/` and is not this reviewer.
4. If no agentic target remains, call `noop` and stop. Do **not** invent an issue.

## How to inspect each agentic target

For each remaining agentic target:

1. Read the `.md` source (YAML frontmatter + markdown body). Prefer it as intent.
2. Read the matching `.lock.yml` if present. Use it for compiled facts (secrets,
   `--allow-all-tools` / unrestricted bash, injected safe-outputs such as
   `create_issue`, network firewall domains, installed CLIs, etc.).
3. Read asset context from the **PR head** checkout:
   - `AGENTS.md` if present
   - `infra/` when the target talks about Terraform, RDS, KMS, or similar
4. If `AGENTS.md` is missing, say so explicitly in the issue. Do **not** invent
   an inventory that is not in the tree. Still ground scenarios in concrete
   config and prompt facts (resource names, ForceNew/replacement attributes,
   `bash: [":*"]`, “carry through” / `-auto-approve`, ambient CLI installs).

## Output

Use **`create_issue` only**. No apply, no repo writes, no PR comments.

File exactly one issue. Title should name the primary target workflow.

Issue body shape:

### Header
- PR number
- Target file(s)
- Engine / model
- Tools (especially bash or install steps)
- Permissions
- Network
- Notable prompt lines (carry-through, auto-approve, mutate/apply language)

### Asset context
- Quote the inventory row from `AGENTS.md` if present
- Otherwise state that inventory is absent and list the config facts you used

### Five scenarios
Each scenario must include:

1. **title**
2. **capability** — what this workflow is allowed to do
3. **asset** — what can be hurt
4. **how an honest deputy gets there** — no attacker required; follow the prompt
   with the granted tools
5. **what would have blocked it** — missing context vs missing capability limit

Do not produce a generic STRIDE/STRIDE dump. Every scenario must cite a concrete
frontmatter field, lock-file fact, prompt line, or infra attribute.

## Example direction (kms-rotation-agent)

When reviewing `kms-rotation-agent.md`, look for patterns such as:

- unrestricted `bash: [":*"]`
- mock `terraform` installed onto PATH in `steps:`
- prompt language like “carry the change through” plus `-auto-approve`
- ForceNew / replacement on `kms_key_id` for `customer-prod`

Those facts should drive the five scenarios when present — adapted to whatever
the changed workflow actually contains.
