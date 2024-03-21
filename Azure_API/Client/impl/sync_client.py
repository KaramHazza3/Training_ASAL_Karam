"""
Module defining a synchronous client for making HTTP requests.
"""

from typing import Union
from urllib.parse import urljoin
import httpx
from Responses.api_responses import SuccessResponse, ErrorResponse
from Client import Client


class SyncClient(Client):
    """
    Synchronous client for making HTTP requests.
    """

    def make_request(self, method: str, url: str, content_type='application/json', **kwargs
                     ) -> Union[SuccessResponse, ErrorResponse]:
        """
        Make a synchronous HTTP request.

        Args:
            method (str): The HTTP method (e.g., GET, POST).
            url (str): The URL to which the request is made.
            content_type (str, optional): The content type of the request.
             Defaults to 'application/json'.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Union[SuccessResponse, ErrorResponse]: A SuccessResponse or ErrorResponse object.
        """
        self.headers['Content-Type'] = content_type
        with httpx.Client(event_hooks=self.event_hooks) as client:
            response = client.request(method, urljoin(self.BASE_URL, url),
                                      headers=self.headers, **kwargs)
            if response.status_code == 204:
                return SuccessResponse(status_code=response.status_code, data="")
            if response.is_success:
                return SuccessResponse(status_code=response.status_code, data=response.json())
            return ErrorResponse(status_code=response.status_code, error=response.text)
