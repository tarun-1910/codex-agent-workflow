from core.codex_client import CodexClient


def main():
    client = CodexClient()

    try:
        response = client.send_message(
            "Reply with exactly: Reusable Codex client working."
        )

        print(response)

    finally:
        client.close()


if __name__ == "__main__":
    main()