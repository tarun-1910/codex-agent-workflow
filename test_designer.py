from core.codex_client import CodexClient
from agents.designer import Designer


def main():

    client = CodexClient()

    try:
        designer = Designer(client)

        designer.run()

    finally:
        client.close()


if __name__ == "__main__":
    main()