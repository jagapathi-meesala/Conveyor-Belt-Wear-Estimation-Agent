import argparse, json
from pathlib import Path
from core.assessment import assess

def main():
    parser=argparse.ArgumentParser(description="Conveyor belt wear screening")
    parser.add_argument("input", help="Path to input JSON")
    parser.add_argument("--output", help="Optional output JSON path")
    args=parser.parse_args()
    record=json.loads(Path(args.input).read_text(encoding="utf-8"))
    report=assess(record)
    rendered=json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(rendered+"\n", encoding="utf-8")
    print(rendered)
    return 0 if not report["data_quality_issues"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
