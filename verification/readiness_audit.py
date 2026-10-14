from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
required=['agent.yaml','SOUL.md','RULES.md','DUTIES.md','AGENTS.md','EXPLAINABILITY.md','README.md','requirements.txt','core/assessment.py','core/cli.py','tools/assess-belt-wear.yaml','tools/validate-inspection-data.yaml','tools/prioritize-maintenance.yaml','skills/wear-assessment/SKILL.md','skills/maintenance-planning/SKILL.md','skills/data-quality/SKILL.md','tests/test_assessment.py','examples/belt_case.json','pytest.ini','verification/readiness_audit.py','.gitignore']
missing=[x for x in required if not (root/x).is_file()]
print(f'Required files: {len(required)-len(missing)}/{len(required)} present')
if missing:
 print('Missing:', ', '.join(missing)); sys.exit(1)
print('PASS: local readiness audit')
