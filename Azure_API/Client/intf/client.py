"""
Module defining an abstract base class for clients.
"""

from abc import ABC, abstractmethod
from typing import Union, Final
from Config.azure_config import AzureConfig
from Logger.logger import Logger
from Responses.api_responses import SuccessResponse, ErrorResponse


class Client(ABC):
    """
    Abstract base class defining a client interface.
    """
    BASE_URL: Final = "https://dev.azure.com/"

    def __init__(self, settings_file: str, logger: Logger):
        """
        Initialize the Client with settings file and a bot instance.

        Args:
            settings_file (str): The path to the settings file.
        """
        self.logger = logger
        self.headers: dict = {
            'Authorization': f'Basic {AzureConfig.get_token(settings_file).api_token}',
        }
        self.event_hooks = {
            'request': [self.logger.log_request],
            'response': [self.logger.log_response],
        }

    @abstractmethod
    def make_request(self, method: str, url: str, content_type: str = 'application/json',
                     **kwargs) -> Union[SuccessResponse, ErrorResponse]:
        """
        Make a request.

        Args:
            method (str): The HTTP method (e.g., GET, POST).
            url (str): The URL to which the request is made.
            content_type (str, optional): The content type of the request.
             Defaults to 'application/json'.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Union[SuccessResponse, ErrorResponse]: A SuccessResponse or ErrorResponse object.
        """
