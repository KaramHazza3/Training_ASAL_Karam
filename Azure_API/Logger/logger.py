"""
Module defining an abstract base class for logging HTTP requests and responses.
"""

from abc import ABC, abstractmethod
from httpx import Request, Response
from Bots import TelegramBOT


class Logger(ABC):
    """
    Abstract base class for logging HTTP requests and responses.
    """

    def __init__(self, bot: TelegramBOT):
        self.bot = bot

    @abstractmethod
    def send_request_message(self, request: Request):
        """
        Send a message before making an HTTP request.

        Args:
            request (Request): The HTTP request object.
        """

    @abstractmethod
    def send_response_message(self, response: Response):
        """
        Send a message after receiving an HTTP response.

        Args:
            response (Response): The HTTP response object.
        """

    @abstractmethod
    def log_request(self, request: Request):
        """
        Log an HTTP request.

        Args:
            request (Request): The HTTP request object.
        """

    @abstractmethod
    def log_response(self, response: Response):
        """
        Log an HTTP response.

        Args:
            response (Response): The HTTP response object.
        """
