"""
Module defining an abstract base class for a BOT (Base Operational Technology).
"""

from abc import ABC, abstractmethod


class TelegramBOT(ABC):
    """
    Abstract base class defining the interface for a BOT (Base Operational Technology).
    """
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    @abstractmethod
    def send_message(self, message: str):
        """
        Abstract method to send a message.

        Args:
            message (str): The message to be sent.

        Returns:
            None
        """
