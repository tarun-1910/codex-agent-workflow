
from core.codex_client import CodexClient
from agents.frontend_developer import FrontendDeveloper


def main():

    client = CodexClient()

    try:
        developer = FrontendDeveloper(client)

        developer.run()

    finally:
        client.close()


if __name__ == "__main__":
    main()
