import json
from pathlib import Path

from core.codex_client import CodexClient


class ProjectManager:

    def __init__(self, client):
        self.client = client

    def generate_plan(self, project_idea: str):

        prompt = f"""
You are an experienced software project manager.

Analyze the following project idea:

{project_idea}

Create a complete project plan.

Return ONLY a valid JSON object with these three keys:

1. requirements
2. tasks
3. acceptance_criteria

Requirements:
- Describe the project purpose.
- List functional requirements.
- List non-functional requirements.
- Identify the main features.

Tasks:
- Break development into clear, ordered tasks.
- Mention frontend, backend, database and testing tasks where relevant.
- Include dependencies between tasks.

Acceptance criteria:
- Provide measurable conditions to verify completion.
- Include functional and testing criteria.

Do not use Markdown code fences.
Return valid JSON only.
"""

        response = self.client.send_message(prompt)

        # Extract JSON from the response
        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("Codex did not return valid JSON.")

        plan = json.loads(response[start:end])

        required_keys = [
            "requirements",
            "tasks",
            "acceptance_criteria"
        ]

        for key in required_keys:
            if key not in plan:
                raise ValueError(f"Missing section: {key}")

        return plan

    def save_plan(self, plan):

        output_dir = Path("workspace/generated_project")
        output_dir.mkdir(parents=True, exist_ok=True)

        files = {
            "requirements.md": plan["requirements"],
            "tasks.md": plan["tasks"],
            "acceptance_criteria.md": plan["acceptance_criteria"]
        }

        for filename, content in files.items():

            file_path = output_dir / filename

            file_path.write_text(
                str(content),
                encoding="utf-8"
            )

            print(f"Created: {file_path}")

    def run(self, project_idea: str):

        print("\nProject Manager Agent started...")

        plan = self.generate_plan(project_idea)

        self.save_plan(plan)

        print("\nProject planning completed!")