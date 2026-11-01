
from orchestrator.workflow import Workflow


def main():

    project_idea = """
    Build an Expense Tracker application.

    Features:
    - Add daily expenses.
    - Edit and delete expenses.
    - Categorize expenses.
    - View monthly spending.
    - Calculate total expenses.
    - Display spending by category.

    Technology:
    - Frontend: HTML, CSS, JavaScript.
    - Backend: Python FastAPI.
    - Database: SQLite.
    - Testing: Pytest.
    """

    workflow = Workflow()

    workflow.run(project_idea)


if __name__ == "__main__":
    main()
