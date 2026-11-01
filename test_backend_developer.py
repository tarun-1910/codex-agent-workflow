
from core.codex_client import CodexClient
from agents.backend_developer import BackendDeveloper


def main():

    client = CodexClient()

    try:
        developer = BackendDeveloper(client)

        developer.run()

    finally:
        client.close()


if __name__ == "__main__":
    main()
