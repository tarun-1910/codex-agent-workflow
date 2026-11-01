from openai_codex import Codex


class CodexClient:

    def __init__(self):
        self.codex = Codex()
        self.thread = self.codex.thread_start()

    def send_message(self, prompt: str) -> str:
        result = self.thread.run(prompt)
        return result.final_response

    def close(self):
        self.codex.close()