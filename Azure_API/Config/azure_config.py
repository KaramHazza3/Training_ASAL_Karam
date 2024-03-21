"""
Module defining a static configuration class for Azure.
"""

import configparser
import base64
from Responses import Settings


class AzureConfig:
    """
    Static configuration class for Azure.
    """

    @staticmethod
    def get_token(settings_file: str) -> Settings:
        """
        Get Azure API token from settings file.

        Args:
            settings_file (str): The path to the settings file.

        Returns:
            Settings: An object containing the API token.

        Raises:
            ValueError: If the settings file is missing, empty,
            or if the 'AUTH' section or 'PAT' key is missing.
        """
        if not settings_file:
            raise ValueError("Settings file path is empty or not provided.")

        config = configparser.ConfigParser()

        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                config.read_file(f)
        except FileNotFoundError:
            raise ValueError(f"The settings file '{settings_file}' does not exist.") from None
        except configparser.Error as e:
            raise ValueError(f"Error reading settings file '{settings_file}': {e}") from e

        try:
            pat = config.get('AUTH', 'PAT')
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise ValueError("The settings file is missing the 'AUTH' section or 'PAT' key."
                             " Please provide a valid file.") from e

        encoded_pat = base64.b64encode(f':{pat}'.encode('ascii')).decode('ascii')
        return Settings(api_token=encoded_pat)
