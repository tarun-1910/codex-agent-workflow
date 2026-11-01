from pathlib import Path

from core.codex_client import CodexClient


class Designer:

    def __init__(self, client):
        self.client = client

    def read_requirements(self):

        project_dir = Path("workspace/generated_project")

        requirements = (
            project_dir / "requirements.md"
        ).read_text(encoding="utf-8")

        tasks = (
            project_dir / "tasks.md"
        ).read_text(encoding="utf-8")

        acceptance = (
            project_dir / "acceptance_criteria.md"
        ).read_text(encoding="utf-8")

        return requirements, tasks, acceptance

    def generate_design(self):

        requirements, tasks, acceptance = (
            self.read_requirements()
        )

        prompt = f"""
You are a senior software architect and UI/UX designer.

Your responsibility is to design the application
based on the Project Manager's documents.

PROJECT REQUIREMENTS:
{requirements}

DEVELOPMENT TASKS:
{tasks}

ACCEPTANCE CRITERIA:
{acceptance}

Create a detailed design specification in Markdown.

Include these sections:

1. Project Overview
2. Application Architecture
3. Frontend Design
4. Backend Architecture
5. Database Design
6. API Endpoint Design
7. UI Pages and Components
8. User Flow
9. Folder Structure
10. Technology Decisions
11. Design Considerations and Risks

Important instructions:

- Follow the technologies specified in the requirements.
- Do not introduce unnecessary technologies.
- Keep the architecture suitable for an MVP.
- Explain how frontend, backend and database communicate.
- Include a proposed database schema.
- Include API methods, paths and descriptions.
- Make the design practical for developers to implement.

Return the complete Markdown document only.
"""

        print("Designer is analyzing project requirements...")

        response = self.client.send_message(prompt)

        if not response.strip():
            raise ValueError("Designer returned an empty response.")

        return response

    def save_design(self, design):

        output_dir = Path("workspace/generated_project")
        output_dir.mkdir(parents=True, exist_ok=True)

        design_file = output_dir / "design_spec.md"

        design_file.write_text(
            design,
            encoding="utf-8"
        )

        print(f"Created: {design_file}")

    def run(self):

        print("\nDesigner Agent started...")

        design = self.generate_design()

        self.save_design(design)

        print("\nDesign specification completed!")