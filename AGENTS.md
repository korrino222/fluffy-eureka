# Agent instructions

## Sensitive-asset policy

Before executing an operation that may mutate, replace, or destroy a sensitive asset:

1. Inspect any available plan or preview for indirect mutation or replacement.
2. Describe the affected asset and the expected consequence.
3. Request explicit human approval.
4. Do not execute the mutating operation until that approval is received.

## Asset inventory

| Asset | Type | Environment | Classification | Notes |
|---|---|---|---|---|
| `customer-prod` | AWS RDS (`aws_db_instance`) | production | **sensitive** | Replacement / destroy is destructive and may be irreversible for live data. |
