"""
Module defining a synchronous Telegram bot.
"""

import httpx
from Bots import TelegramBOT


class SyncTelegramBOT(TelegramBOT):
    """
    Synchronous Telegram bot implementation.
    """

    def send_message(self, message: str):
        """
        Send a message using the Telegram bot synchronously.

        Args:
            message (str): The message to be sent.
        """
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": message
        }
        with httpx.Client() as client:
            try:
                response = client.post(url, params=params)
                response.raise_for_status()
            except httpx.RequestError as e:
                print(f"Sync Telegram BOT: An error occurred while requesting {e.request.url!r}.")
            except httpx.HTTPStatusError as e:
                print(f"Sync Telegram BOT: Error response {e.response.status_code}"
                      f" while requesting {e.request.url!r}.")
