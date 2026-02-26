"""Grade excel-report eval outputs against assertions."""
import json
import re
import sys
from pathlib import Path

def grade_report(report_path, eval_name, assertions):
    """Grade a single report against its assertions."""
    results = {"expectations": []}

    # Check file exists
    exists = Path(report_path).exists()
    content = ""
    if exists:
        content = Path(report_path).read_text(encoding="utf-8", errors="replace").lower()

    for a in assertions:
        text = a["text"]
        passed = False
        evidence = ""

        if "file exists" in text.lower():
            passed = exists
            evidence = f"File {'found' if exists else 'NOT found'} at {report_path}"

        elif "executive summary" in text.lower():
            passed = "executive summary" in content
            evidence = "Section heading found" if passed else "No 'Executive Summary' heading found"

        elif "key findings" in text.lower():
            passed = "key findings" in content or "findings" in content
            evidence = "Section heading found" if passed else "No 'Key Findings' heading found"

        elif "recommendations" in text.lower():
            passed = "recommendation" in content
            evidence = "Section heading found" if passed else "No 'Recommendations' heading found"

        elif "specific numeric" in text.lower():
            numbers = re.findall(r'\d+\.?\d*', content)
            passed = len(numbers) > 5
            evidence = f"Found {len(numbers)} numeric values in report"

        elif "200 rows" in text.lower():
            passed = "200" in content
            evidence = "Row count 200 mentioned" if passed else "Row count 200 not found"

        elif "150 rows" in text.lower():
            passed = "150" in content
            evidence = "Row count 150 mentioned" if passed else "Row count 150 not found"

        elif "50 rows" in text.lower():
            passed = "50" in content
            evidence = "Row count 50 mentioned" if passed else "Row count 50 not found"

        elif "outlier" in text.lower() and "order" in text.lower():
            passed = ("outlier" in content or "900" in content or "1000" in content
                      or "1,0" in content or "unusual" in content or "extreme" in content)
            evidence = "Outlier orders referenced" if passed else "No mention of high-value outlier orders"

        elif "product categories" in text.lower() or "3 of the 5" in text.lower():
            categories = ["electronics", "clothing", "home", "garden", "books", "sports"]
            found = [c for c in categories if c in content]
            passed = len(found) >= 3
            evidence = f"Found categories: {', '.join(found)}" if found else "No product categories mentioned"

        elif "missing values" in text.lower():
            passed = ("missing" in content or "null" in content or "nan" in content
                      or "empty" in content or "incomplete" in content)
            evidence = "Missing values discussed" if passed else "No mention of missing data"

        elif "salary outlier" in text.lower():
            passed = ("outlier" in content or "180" in content or "250" in content
                      or "unusual" in content or "extreme" in content or "high" in content)
            evidence = "Salary outliers mentioned" if passed else "No salary outlier discussion found"

        elif "temperature" in text.lower() and "humidity" in text.lower():
            has_temp = "temperature" in content or "temp" in content
            has_humid = "humidity" in content
            has_press = "pressure" in content
            passed = has_temp and has_humid and has_press
            evidence = f"Temp={'Y' if has_temp else 'N'}, Humidity={'Y' if has_humid else 'N'}, Pressure={'Y' if has_press else 'N'}"

        elif "sensor id" in text.lower():
            ids_found = [sid for sid in ["s-01", "s-02", "s-03"] if sid in content]
            passed = len(ids_found) > 0
            evidence = f"Sensor IDs found: {', '.join(ids_found)}" if ids_found else "No sensor IDs referenced"

        else:
            evidence = "No automated check available for this assertion"

        results["expectations"].append({
            "text": text,
            "passed": passed,
            "evidence": evidence
        })

    return results


def main():
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("excel-report-workspace/iteration-1")

    eval_dirs = {
        "ecommerce-orders": {
            "with_skill": "ecommerce_orders-report.md",
            "without_skill": "ecommerce_orders-report.md"
        },
        "employee-survey": {
            "with_skill": "employee_survey-report.md",
            "without_skill": "employee_survey-report.md"
        },
        "sensor-readings": {
            "with_skill": "sensor_readings-report.md",
            "without_skill": "sensor_readings-report.md"
        }
    }

    summary = {"total": 0, "passed": 0, "by_eval": {}}

    for eval_name, configs in eval_dirs.items():
        eval_dir = workspace / eval_name
        metadata_path = eval_dir / "eval_metadata.json"

        if not metadata_path.exists():
            print(f"  SKIP {eval_name}: no eval_metadata.json")
            continue

        metadata = json.loads(metadata_path.read_text())
        assertions = metadata["assertions"]

        for config_name, report_filename in configs.items():
            report_path = eval_dir / config_name / "outputs" / report_filename
            grading = grade_report(str(report_path), eval_name, assertions)

            # Save grading.json
            grading_path = eval_dir / config_name / "grading.json"
            grading_path.write_text(json.dumps(grading, indent=2))

            passed = sum(1 for e in grading["expectations"] if e["passed"])
            total = len(grading["expectations"])
            summary["total"] += total
            summary["passed"] += passed
            summary["by_eval"][f"{eval_name}/{config_name}"] = {
                "passed": passed, "total": total, "rate": f"{passed/total*100:.0f}%"
            }

            print(f"  {eval_name}/{config_name}: {passed}/{total} passed ({passed/total*100:.0f}%)")
            for e in grading["expectations"]:
                status = "PASS" if e["passed"] else "FAIL"
                print(f"    [{status}] {e['text']}")
                if not e["passed"]:
                    print(f"           {e['evidence']}")

    print(f"\nOverall: {summary['passed']}/{summary['total']} assertions passed")

    summary_path = workspace / "grading_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
