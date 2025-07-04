class DummyLLM:
    """Placeholder LLM that echoes the prompt."""

    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        return "LLM response: " + prompt
