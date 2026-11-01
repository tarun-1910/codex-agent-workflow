
from openai_codex import Codex

def main():
    with Codex() as codex:
        thread = codex.thread_start()

        result = thread.run(
            "Reply with exactly: Codex SDK connection successful."
        )

        print(result.final_response)


if __name__ == "__main__":
    main()
