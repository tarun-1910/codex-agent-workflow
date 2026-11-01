
import json
from pathlib import Path

from core.codex_client import CodexClient


class BackendDeveloper:

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

    def generate_backend(self):

        design, requirements = self.read_design()

        prompt = f"""
You are a senior Python backend developer.

Build the backend for the TaskFlow application.

PROJECT REQUIREMENTS:
{requirements}

DESIGN SPECIFICATION:
{design}

TECHNOLOGY:
- Python
- FastAPI
- SQLite
- Pydantic

Generate exactly these three files:

1. main.py
2. database.py
3. requirements.txt

Requirements:

main.py:
- Create a FastAPI application.
- Implement POST /tasks to create a task.
- Implement GET /tasks to list all tasks.
- Implement GET /tasks/{{task_id}} to retrieve one task.
- Implement PUT /tasks/{{task_id}} to update a task.
- Implement DELETE /tasks/{{task_id}} to delete a task.
- Include input validation using Pydantic.
- Return appropriate HTTP status codes.
- Handle missing tasks with HTTP 404.
- Enable CORS for a local frontend.
- Include a root endpoint.

database.py:
- Use Python's sqlite3 module.
- Create the SQLite database automatically.
- Create a tasks table if it does not exist.
- Include task fields such as id, title, description,
  status, created_at and updated_at.
- Use parameterized SQL queries.

requirements.txt:
- Include FastAPI and Uvicorn.

Additional instructions:
- Keep the implementation simple and suitable for an MVP.
- Do not use API keys.
- Do not use external databases.
- Make sure the generated files work together.
- Do not include unnecessary dependencies.

Return ONLY valid JSON in this format:

{{
  "main.py": "complete Python source code",
  "database.py": "complete Python source code",
  "requirements.txt": "complete dependency list"
}}

Do not use Markdown code fences.
Escape JSON special characters correctly.
"""

        print("Backend Developer is generating code...")

        response = self.client.send_message(prompt)

        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("Codex did not return valid JSON.")

        files = json.loads(response[start:end])

        required_files = [
            "main.py",
            "database.py",
            "requirements.txt"
        ]

        for filename in required_files:
            if filename not in files:
                raise ValueError(f"Missing backend file: {filename}")

            if not isinstance(files[filename], str):
                raise ValueError(f"Invalid content in {filename}")

            if not files[filename].strip():
                raise ValueError(f"Empty content in {filename}")

        return files

    def save_backend(self, files):

        output_dir = Path(
            "workspace/generated_project/backend"
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

        print("\nBackend Developer Agent started...")

        files = self.generate_backend()

        self.save_backend(files)

        print("\nBackend development completed!")
