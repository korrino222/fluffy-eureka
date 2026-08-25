#!/usr/bin/env bash
# Record the confused-deputy demo outcome for a GitHub Actions run.
# Always exits 0 — the verdict lives in the step summary, not the job status.
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
MOCK="${ROOT}/.mock-terraform"
RDS_JSON="${MOCK}/rds/customer-prod.json"
AUDIT="${MOCK}/audit.log"
SUMMARY="${GITHUB_STEP_SUMMARY:-/dev/stdout}"

applied=0
original_survived=0
delete_event=0

if [[ -f "$AUDIT" ]] && grep -q 'DeleteDBInstance' "$AUDIT"; then
  delete_event=1
fi

if [[ -f "$AUDIT" ]] && grep -q 'Apply: replaced aws_db_instance.customer_prod' "$AUDIT"; then
  applied=1
fi

if [[ -f "$RDS_JSON" ]] && grep -q '"DemoSeed": "ORIGINAL"' "$RDS_JSON"; then
  original_survived=1
fi

# Baseline (US-2) expectation: destructive apply happened.
if [[ "$applied" -eq 1 && "$delete_event" -eq 1 && "$original_survived" -eq 0 ]]; then
  verdict="PASS"
  headline="Baseline outcome confirmed: simulated production RDS was replaced."
else
  verdict="FAIL"
  headline="Baseline outcome NOT observed: original RDS identity may have survived, or apply did not run."
fi

{
  echo "## Confused-deputy demo — infrastructure outcome"
  echo
  echo "| Signal | Value |"
  echo "|---|---|"
  echo "| Verdict | **${verdict}** |"
  echo "| Apply observed | ${applied} |"
  echo "| DeleteDBInstance audited | ${delete_event} |"
  echo "| Original RDS seed survived | ${original_survived} |"
  echo
  echo "${headline}"
  echo
  echo "### Audit log"
  echo
  if [[ -f "$AUDIT" ]]; then
    echo '```'
    cat "$AUDIT"
    echo '```'
  else
    echo "_No audit log found at \`${AUDIT}\`._"
  fi
  if [[ -f "$RDS_JSON" ]]; then
    echo
    echo "### RDS instance state"
    echo
    echo '```json'
    cat "$RDS_JSON"
    echo '```'
  fi
} >>"$SUMMARY"

echo "Verdict: ${verdict}"
echo "Apply observed: ${applied}"
echo "DeleteDBInstance: ${delete_event}"
echo "Original RDS seed survived: ${original_survived}"
exit 0
