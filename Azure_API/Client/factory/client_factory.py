"""
Module defining a factory for creating client objects.
"""

from Client import SyncClient, AsyncClient, Client
from Logger.logger import Logger


class ClientFactory:
    """
    Factory class for creating client objects.
    """

    @staticmethod
    def get_client(settings_file: str, async_mode=False, logger: Logger = None) -> Client:
        """
        Create a client based on the specified mode.

        Args:
            settings_file (str): The path to the settings file.
            async_mode (bool, optional): Whether to create an asynchronous client.
             Defaults to False.
            logger (Logger, optional): An optional logger object. Defaults to None.

        Returns:
            Client: The created client object.
        """
        if async_mode:
            return AsyncClient(settings_file, logger=logger)
        return SyncClient(settings_file, logger=logger)
