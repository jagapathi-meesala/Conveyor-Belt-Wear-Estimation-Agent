# Conveyor Belt Wear Estimation Agent

A small Python agent that reviews supplied belt inspection measurements, calculates indicative thickness loss, flags data-quality issues, and prioritizes human maintenance review.

## Inputs
JSON with `belt_id`, `initial_thickness_mm`, `current_thickness_mm`, optional `wear_warning_pct`, `wear_critical_pct`, `inspection_date`, and optional `observations` / `critical_flags`.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python verification/readiness_audit.py
python -m core.cli examples/belt_case.json --output report.json
```

## Safety and limitations
Wear percentage is calculated as `(initial - current) / initial * 100`. Negative wear (current thickness greater than initial) is flagged as a data review issue. The result is not a remaining-life prediction, a structural-integrity certification, or permission to operate. Real-world decisions require manufacturer specifications, standardized inspection methods, environmental/contextual data, and qualified personnel.
