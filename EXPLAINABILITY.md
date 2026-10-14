# Explainability

## Inputs
The agent reads the supplied belt identifier, initial/current thickness, optional thresholds, inspection date, observations, and critical flags. It does not independently verify measurement instruments or provenance.

## Decision
It calculates thickness loss percentage when both thickness values are valid and initial thickness is positive. Configured warning/critical thresholds determine an indicative review band. Explicit critical flags are escalated regardless of the calculated percentage.

## Limits
This is a heuristic screening tool. It does not estimate remaining useful life, infer safe operating status, or replace manufacturer guidance or qualified inspection.

## Tool: assess-belt-wear
### Inputs and Data Sources
Uses supplied thickness values and thresholds.
### Decision and Reasoning
Computes percentage thickness loss and an indicative band.
### Outputs and Evidence
Returns calculations, flags, and rationale.
### Limits and Constraints
No sensor integration or validated degradation model.
### Failure Handling
Missing or invalid measurements are reported as review issues.
### Human Review
A qualified inspector must verify measurements and findings.

## Tool: validate-inspection-data
### Inputs and Data Sources
Uses the supplied JSON inspection record.
### Decision and Reasoning
Checks required fields, numeric ranges, and contradictory values.
### Outputs and Evidence
Returns data-quality issues.
### Limits and Constraints
Cannot authenticate source records.
### Failure Handling
Invalid data prevents a reliable wear calculation.
### Human Review
Resolve measurement and provenance issues before relying on the report.

## Tool: prioritize-maintenance
### Inputs and Data Sources
Uses calculated band, critical flags, and observations.
### Decision and Reasoning
Orders cases for review using explicit critical flags and configured wear bands.
### Outputs and Evidence
Returns an advisory priority and supporting reasons.
### Limits and Constraints
Priority is not an operating authorization.
### Failure Handling
Unclear evidence is marked for review.
### Human Review
Maintenance personnel follow site lockout, inspection, and escalation procedures.
