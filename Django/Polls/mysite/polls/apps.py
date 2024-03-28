"""
App configuration for the Polls application.
"""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
    AppConfig for the Polls application.
    """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'polls'
