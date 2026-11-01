
from core.codex_client import CodexClient

from agents.project_manager import ProjectManager
from agents.designer import Designer
from agents.frontend_developer import FrontendDeveloper
from agents.backend_developer import BackendDeveloper
from agents.tester import Tester


class Workflow:

    def __init__(self):
        self.client = CodexClient()

    def run(self, project_idea):

        try:
            print("\n========== WORKFLOW STARTED ==========\n")

            # Stage 1: Project Manager
            print("\n[1/5] Project Manager")
            manager = ProjectManager(self.client)
            manager.run(project_idea)

            # Stage 2: Designer
            print("\n[2/5] Designer")
            designer = Designer(self.client)
            designer.run()

            # Stage 3: Frontend Developer
            print("\n[3/5] Frontend Developer")
            frontend = FrontendDeveloper(self.client)
            frontend.run()

            # Stage 4: Backend Developer
            print("\n[4/5] Backend Developer")
            backend = BackendDeveloper(self.client)
            backend.run()

            # Stage 5: Tester
            print("\n[5/5] Tester")
            tester = Tester(self.client)
            tester.run()

            print("\n========== WORKFLOW COMPLETED ==========")

        except Exception as error:
            print("\nWORKFLOW FAILED!")
            print(f"Error: {error}")
            raise

        finally:
            self.client.close()
