
from core.codex_client import CodexClient
from agents.tester import Tester


def main():

    client = CodexClient()

    try:
        tester = Tester(client)
        tester.run()

    finally:
        client.close()


if __name__ == "__main__":
    main()
