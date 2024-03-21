"""
Module defining an asynchronous logger class for sending messages
 before and after making HTTP requests.
"""

from httpx import Request, Response, RequestError, TimeoutException
from Logger.logger import Logger


class AsyncLogger(Logger):
    """
    Asynchronous logger class for sending messages before and after making HTTP requests.
    """

    async def send_request_message(self, request: Request):
        """
        Send a message before making a request.

        Args:
            request (Request): The HTTP request object.
        """
        try:
            message = f"Sending {request.method} request to {request.url}"
            await self.bot.send_message(message=message)
        except RequestError as e:
            print(f"Error sending request message: RequestError - {e}")

    async def send_response_message(self, response: Response):
        """
        Send a message after receiving a response.

        Args:
            response (Response): The HTTP response object.
        """
        try:
            message = (f"A response with status code {response.status_code} "
                       f"for {response.request.method} request"
                       f" to {response.request.url} has been received ")
            await self.bot.send_message(message=message)
        except TimeoutException as e:
            print(f"Error sending response message: TimeoutException - {e}")

    async def log_request(self, request: Request):
        """
        Log the request.

        Args:
            request (Request): The HTTP request object.
        """
        if self.bot:
            await self.send_request_message(request=request)
        print(f"Sending request to {request.url}")

    async def log_response(self, response: Response):
        """
        Log the response.

        Args:
            response (Response): The HTTP response object.
        """
        if self.bot:
            await response.aread()
            await self.send_response_message(response=response)
        print(f"Received response with status {response.status_code} from {response.url}")
