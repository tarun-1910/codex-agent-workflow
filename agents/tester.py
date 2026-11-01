
import json
from pathlib import Path

from core.codex_client import CodexClient


class Tester:

    def __init__(self, client):
        self.client = client

    def read_project_files(self):

        project_dir = Path("workspace/generated_project")

        files_to_read = [
            project_dir / "requirements.md",
            project_dir / "acceptance_criteria.md",
            project_dir / "design_spec.md",
            project_dir / "frontend/index.html",
            project_dir / "frontend/style.css",
            project_dir / "frontend/script.js",
            project_dir / "backend/main.py",
            project_dir / "backend/database.py",
            project_dir / "backend/requirements.txt"
        ]

        project_content = {}

        for file_path in files_to_read:

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Missing project file: {file_path}"
                )

            project_content[str(file_path)] = (
                file_path.read_text(encoding="utf-8")
            )

        return project_content

    def analyze_project(self):

        project_content = self.read_project_files()

        prompt = f"""
You are a senior software QA engineer.

Review the following generated TaskFlow application.

PROJECT FILES:
{json.dumps(project_content, indent=2)}

Perform a detailed code review.

Check:

1. Frontend HTML correctness.
2. CSS and responsive design.
3. JavaScript functionality.
4. Backend API implementation.
5. SQLite database implementation.
6. API endpoint consistency.
7. Input validation.
8. Error handling.
9. Security issues.
10. Acceptance criteria coverage.

Identify:
- Bugs
- Missing features
- Integration problems
- Potential runtime errors

Return ONLY valid JSON using this structure:

{{
    "status": "PASS or FAIL",
    "summary": "Overall assessment",
    "issues": [
        {{
            "severity": "HIGH, MEDIUM or LOW",
            "file": "filename",
            "problem": "Description",
            "suggested_fix": "How to fix it"
        }}
    ],
    "recommendations": [
        "Recommendation"
    ]
}}

Do not use Markdown code fences.
"""

        print("Tester is analyzing the application...")

        response = self.client.send_message(prompt)

        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("Tester did not return valid JSON.")

        report = json.loads(response[start:end])

        if report.get("status") not in ["PASS", "FAIL"]:
            raise ValueError("Invalid test status.")

        return report

    def save_report(self, report):

        output_dir = Path("workspace/generated_project")
        output_dir.mkdir(parents=True, exist_ok=True)

        report_file = output_dir / "test_report.json"

        report_file.write_text(
            json.dumps(report, indent=4),
            encoding="utf-8"
        )

        print(f"Created: {report_file}")

    def run(self):

        print("\nTester Agent started...")

        report = self.analyze_project()

        self.save_report(report)

        print("\nTest Status:", report["status"])
        print("Summary:", report["summary"])

        print("\nIssues found:")

        for issue in report["issues"]:
            print(
                f"- [{issue['severity']}] "
                f"{issue['file']}: {issue['problem']}"
            )

        print("\nTesting completed!")
