
import json
from pathlib import Path

from core.codex_client import CodexClient


class FrontendDeveloper:

    def __init__(self, client):
        self.client = client

    def read_design(self):

        project_dir = Path("workspace/generated_project")

        design_file = project_dir / "design_spec.md"
        requirements_file = project_dir / "requirements.md"

        if not design_file.exists():
            raise FileNotFoundError("Design specification not found.")

        design = design_file.read_text(encoding="utf-8")
        requirements = requirements_file.read_text(encoding="utf-8")

        return design, requirements

    def generate_frontend(self):

        design, requirements = self.read_design()

        prompt = f"""
You are a senior frontend developer.

Build the frontend for the TaskFlow application.

PROJECT REQUIREMENTS:
{requirements}

DESIGN SPECIFICATION:
{design}

TECHNOLOGY:
- HTML5
- CSS3
- Vanilla JavaScript

Generate exactly these three files:

1. index.html
2. style.css
3. script.js

Requirements:
- Follow the supplied design specification.
- Implement the task management interface.
- Support creating, viewing, updating and deleting tasks.
- Allow users to change task status.
- Include appropriate form validation.
- Use localStorage for temporary frontend persistence.
- Make the interface responsive.
- Use clean, maintainable code.
- Do not use React or other frontend frameworks.
- Do not use external API keys.

Return ONLY a valid JSON object in this format:

{{
  "index.html": "complete HTML source code",
  "style.css": "complete CSS source code",
  "script.js": "complete JavaScript source code"
}}

Important:
- Return all three files.
- Keep each file's complete source code in its string value.
- Escape JSON special characters correctly.
- Do not use Markdown code fences.
"""

        print("Frontend Developer is generating code...")

        response = self.client.send_message(prompt)

        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("Codex did not return JSON.")

        files = json.loads(response[start:end])

        required_files = [
            "index.html",
            "style.css",
            "script.js"
        ]

        for filename in required_files:
            if filename not in files:
                raise ValueError(f"Missing frontend file: {filename}")

            if not isinstance(files[filename], str) or not files[filename].strip():
                raise ValueError(f"Invalid content in {filename}")

        return files

    def save_frontend(self, files):

        output_dir = Path(
            "workspace/generated_project/frontend"
        )

        output_dir.mkdir(parents=True, exist_ok=True)

        for filename, content in files.items():

            file_path = output_dir / filename

            file_path.write_text(
                content,
                encoding="utf-8"
            )

            print(f"Created: {file_path}")

    def run(self):

        print("\nFrontend Developer Agent started...")

        files = self.generate_frontend()

        self.save_frontend(files)

        print("\nFrontend development completed!")
