from core.assessment import assess, validate_record

def test_critical_wear():
    r=assess({"belt_id":"B1","initial_thickness_mm":10,"current_thickness_mm":6,"wear_warning_pct":20,"wear_critical_pct":35})
    assert r["wear_percent"] == 40
    assert r["status"] == "critical"

def test_warning_wear():
    r=assess({"belt_id":"B1","initial_thickness_mm":10,"current_thickness_mm":7.5,"wear_warning_pct":20,"wear_critical_pct":35})
    assert r["status"] == "warning"

def test_missing_measurement():
    r=assess({"belt_id":"B1","initial_thickness_mm":10})
    assert r["status"] == "review_required" and r["wear_percent"] is None

def test_negative_loss_requires_review():
    r=assess({"belt_id":"B1","initial_thickness_mm":10,"current_thickness_mm":11})
    assert r["status"] == "review_required"

def test_critical_flag_escalates():
    r=assess({"belt_id":"B1","initial_thickness_mm":10,"current_thickness_mm":9,"critical_flags":["exposed_cords"]})
    assert r["status"] == "critical" and r["priority"] == "urgent_inspection"

def test_invalid_thresholds():
    assert any("warning threshold" in x for x in validate_record({"belt_id":"B1","initial_thickness_mm":10,"current_thickness_mm":8,"wear_warning_pct":40,"wear_critical_pct":30}))

def test_normal_wear():
    r=assess({"belt_id":"B1","initial_thickness_mm":10,"current_thickness_mm":9.5})
    assert r["status"] == "normal" and r["wear_percent"] == 5
