"""
Custom HTTP adapter — for testing arbitrary chatbots/web apps that
don't follow OpenAI or Ollama schemas. You configure how the prompt
gets inserted into the request and where the response text lives.

Usage:
    adapter = CustomHTTPAdapter(
        url="https://example.com/api/chat",
        method="POST",
        request_template={"message": "{prompt}", "session_id": "abc123"},
        response_path=["data", "reply"],
    )
    response = adapter.send("some prompt")
"""

import requests


def _dig(obj, path):
    """Walk a nested dict/list using a list of keys/indices."""
    for key in path:
        if isinstance(obj, list):
            obj = obj[int(key)]
        else:
            obj = obj[key]
    return obj


def _fill_template(template, prompt):
    """Recursively replace the '{prompt}' placeholder in a nested structure."""
    if isinstance(template, str):
        return template.replace("{prompt}", prompt)
    if isinstance(template, dict):
        return {k: _fill_template(v, prompt) for k, v in template.items()}
    if isinstance(template, list):
        return [_fill_template(v, prompt) for v in template]
    return template


from .base_adapter import BaseAdapter


class CustomHTTPAdapter(BaseAdapter):
    name = "custom_http"

    def __init__(self, url: str, method: str = "POST", headers: dict = None, # type: ignore
                 request_template: dict = None, response_path: list = None, # type: ignore
                 timeout: int = 30):
        self.url = url
        self.method = method.upper()
        self.headers = headers or {"Content-Type": "application/json"}
        self.request_template = request_template or {"message": "{prompt}"}
        self.response_path = response_path or ["response"]
        self.timeout = timeout

    def health_check(self) -> bool:
        try:
            r = requests.request(self.method, self.url, headers=self.headers, timeout=5)
            return r.status_code < 500
        except requests.RequestException:
            return False

    def send(self, prompt: str) -> str:
        body = _fill_template(self.request_template, prompt)
        try:
            r = requests.request(
                self.method, self.url, headers=self.headers, json=body, timeout=self.timeout
            )
            r.raise_for_status()
            data = r.json()
            return str(_dig(data, self.response_path))
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Could not reach {self.url}.")
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Request to {self.url} timed out after {self.timeout}s.")
        except (KeyError, IndexError, ValueError):
            raise RuntimeError(
                f"Could not extract response using path {self.response_path}. "
                f"Check your response_path configuration."
            )