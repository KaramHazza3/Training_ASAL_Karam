from Bots.intf.IBot import IBot
import httpx
from Settings import BotSettings


class TelegramBOT(IBot):
    """
    Telegram bot implementation.
    """

    def __init__(self, bot_settings: BotSettings):
        self.settings = bot_settings

    async def send_message_async(self, message: str):
        """
        Send a message using the Telegram bot asynchronously.

        Args:
            message (str): The message to be sent.
        """
        url = f"https://api.telegram.org/bot{self.settings.bot_token}/sendMessage"
        params = {
            "chat_id": self.settings.chat_id,
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

    def send_message(self, message: str):
        """
        Send a message using the Telegram bot synchronously.

        Args:
            message (str): The message to be sent.
        """
        url = f"https://api.telegram.org/bot{self.settings.bot_token}/sendMessage"
        params = {
            "chat_id": self.settings.chat_id,
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

