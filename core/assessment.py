from __future__ import annotations

VALID_BANDS = ("normal", "warning", "critical", "review_required")

def validate_record(record: dict) -> list[str]:
    issues=[]
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    if not record.get("belt_id"):
        issues.append("missing belt_id")
    for key in ("initial_thickness_mm", "current_thickness_mm"):
        value=record.get(key)
        if value is None:
            issues.append(f"missing {key}")
        elif isinstance(value, bool) or not isinstance(value, (int,float)):
            issues.append(f"{key} must be numeric")
        elif value <= 0:
            issues.append(f"{key} must be greater than zero")
    if record.get("wear_warning_pct", 20) < 0 or record.get("wear_critical_pct", 35) < 0:
        issues.append("wear thresholds must be non-negative")
    if record.get("wear_warning_pct", 20) > record.get("wear_critical_pct", 35):
        issues.append("warning threshold exceeds critical threshold")
    return issues

def assess(record: dict) -> dict:
    issues=validate_record(record)
    result={"belt_id": record.get("belt_id") if isinstance(record,dict) else None,
            "status":"review_required", "wear_percent":None, "thickness_loss_mm":None,
            "priority":"human_review", "evidence":[], "data_quality_issues":issues,
            "disclaimer":"Indicative screening only; not a remaining-life estimate or authorization to operate."}
    if issues:
        result["evidence"].append("Wear calculation withheld because input validation failed.")
        return result
    initial=float(record["initial_thickness_mm"]); current=float(record["current_thickness_mm"])
    loss=initial-current
    wear=loss/initial*100
    result["thickness_loss_mm"]=round(loss,4)
    result["wear_percent"]=round(wear,2)
    if loss < 0:
        result["status"]="review_required"
        result["data_quality_issues"].append("current thickness exceeds initial thickness; verify measurements or baseline")
        result["evidence"].append("Calculated negative thickness loss; manual verification required.")
    else:
        warning=float(record.get("wear_warning_pct",20)); critical=float(record.get("wear_critical_pct",35))
        if wear >= critical:
            result["status"]="critical"; result["priority"]="urgent_inspection"
        elif wear >= warning:
            result["status"]="warning"; result["priority"]="schedule_inspection"
        else:
            result["status"]="normal"; result["priority"]="routine_review"
        result["evidence"].append(f"Thickness decreased by {round(loss,4)} mm from the supplied initial measurement.")
        result["evidence"].append(f"Wear estimate {round(wear,2)}% compared with supplied thresholds: warning {warning}%, critical {critical}%.")
    flags=record.get("critical_flags", []) or []
    if flags:
        result["status"]="critical"; result["priority"]="urgent_inspection"
        result["evidence"].append("Critical flags supplied: " + ", ".join(map(str,flags)))
    observations=record.get("observations", []) or []
    if observations:
        result["evidence"].append("Inspector observations supplied: " + "; ".join(map(str,observations)))
    return result
