from httpx import Request, RequestError, Response, TimeoutException
from Loggers.ILogger import ILogger


class AsyncLogger(ILogger):
    """
    Asynchronous logger class for sending messages before and after making HTTP requests.
    """

    async def log_request(self, request: Request):
        """
        Log the request and send a message before making the request.

        Args:
            request (Request): The HTTP request object.
        """
        if not self.bot:
            return

        try:
            message = f"Sending {request.method} request to {request.url}"
            await self.bot.send_message_async(message=message)
        except RequestError as e:
            print(f"Error sending request message: RequestError - {e}")

        print(f"Sending request to {request.url}")

    async def log_response(self, response: Response):
        """
        Log the response and send a message after receiving the response.

        Args:
            response (Response): The HTTP response object.
        """
        if not self.bot:
            return

        await response.aread()

        try:
            message = (f"A response with status code {response.status_code} "
                       f"for {response.request.method} request "
                       f"to {response.request.url} has been received")
            await self.bot.send_message_async(message=message)
        except TimeoutException as e:
            print(f"Error sending response message: TimeoutException - {e}")

        print(f"Received response with status {response.status_code} from {response.url}")
