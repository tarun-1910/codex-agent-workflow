from core.codex_client import CodexClient
from agents.project_manager import ProjectManager


def main():

    client = CodexClient()

    try:
        manager = ProjectManager(client)

        project_idea = """
        Build a Task Management application.

        Features:
        - Create tasks
        - Update tasks
        - Delete tasks
        - View all tasks
        - Track task status

        Technology:
        - Frontend: HTML, CSS, JavaScript
        - Backend: Python FastAPI
        - Database: SQLite
        - Testing: Pytest
        """

        manager.run(project_idea)

    finally:
        client.close()


if __name__ == "__main__":
    main()