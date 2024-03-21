"""
Module defining data classes for API responses.
"""

from dataclasses import dataclass


@dataclass
class Settings:
    """
    Data class for storing API settings.
    """
    api_token: str


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
