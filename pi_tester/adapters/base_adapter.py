"""
Base adapter interface for PI Tester.

Every target adapter (Ollama, OpenAI-style API, custom HTTP endpoint, etc.)
must implement this interface. To add a new target, subclass BaseAdapter
and implement send(). That's the entire contract.
"""

from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """
    Abstract base class for all LLM target adapters.

    Implement send() to wire up a new target. Everything else
    (payload iteration, detection, reporting) works automatically
    once this contract is satisfied.
    """

    name = "base"

    @abstractmethod
    def send(self, prompt: str) -> str:
        """
        Send a prompt to the target and return the raw text response.

        Args:
            prompt: The injection payload text to send.

        Returns:
            The target's response as a plain string.

        Raises:
            ConnectionError: if the target is unreachable.
            RuntimeError: for any other adapter-specific failure.
        """
        raise NotImplementedError

    def health_check(self) -> bool:
        """
        Optional: override to verify the target is reachable before
        running a full test suite. Default assumes always healthy.
        """
        return True