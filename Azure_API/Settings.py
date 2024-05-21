"""
Module defining data classes for API responses.
"""
import base64
from dataclasses import dataclass
from typing import Union, Dict


@dataclass
class AzureSettings:
    """
    Settings for Azure DevOps API.

    Attributes:
        organization_name (str): Organization name.
        pat (str): Personal access token for authentication.
        api_version (str): API version (default is "api-version=7.0").
        base_url (str): Base URL for Azure DevOps API (default is "https://dev.azure.com").
    """
    organization_name: str
    pat: str
    api_version: str = "api-version=7.0"
    base_url: str = "https://dev.azure.com/"

    def get_header(self, content_type: str = "application/json") -> Dict:
        """
        Generate headers for API requests.

        Args:
            content_type (str): Content type for the request (default is "application/json").

        Returns:
            dict: Request headers.
        """
        to_encode_token = f":{self.pat}"
        encoded_credentials = base64.b64encode(to_encode_token.encode('ascii')).decode('ascii')
        return {"Authorization": f"Basic {encoded_credentials}", "Content-Type": content_type}


@dataclass
class ErrorResponse:
    """
    Data class representing an error response from the API.
    """
    status_code: int
    error: str


@dataclass
class SuccessResponse:
    """
    Data class representing a successful response from the API.
    """
    status_code: int
    data: str


@dataclass
class BotSettings:
    """
    Settings for the Telegram bot.

    Attributes:
        bot_token (str): Telegram bot token.
        chat_id (str): The chat ID for sending messages.
    """
    bot_token: str
    chat_id: str


response = Union[SuccessResponse, ErrorResponse]
