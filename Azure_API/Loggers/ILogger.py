"""
Module defining an abstract base class for logging HTTP requests and responses.
"""

from abc import ABC, abstractmethod
from httpx import Request, Response
from Bots.intf.IBot import IBot


class ILogger(ABC):
    """
    Abstract base class for logging HTTP requests and responses.
    """

    def __init__(self, bot: IBot):
        self.bot = bot

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