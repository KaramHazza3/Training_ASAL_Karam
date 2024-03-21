"""
Module defining an asynchronous Telegram bot.
"""

import httpx
from Bots import TelegramBOT


class AsyncTelegramBOT(TelegramBOT):
    """
    Asynchronous Telegram bot implementation.
    """

    async def send_message(self, message: str):
        """
        Send a message using the Telegram bot asynchronously.

        Args:
            message (str): The message to be sent.
        """
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": message
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, params=params)
                response.raise_for_status()
            except httpx.RequestError as e:
                print(f"Async Telegram BOT: An error occurred while requesting {e.request.url!r}.")
            except httpx.HTTPStatusError as e:
                print(f"Async Telegram BOT: Error response {e.response.status_code}"
                      f" while requesting {e.request.url!r}.")
