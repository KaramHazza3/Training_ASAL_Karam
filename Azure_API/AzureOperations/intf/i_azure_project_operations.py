"""
Module defining an abstract base class for operations related to Azure DevOps projects.
"""

from abc import ABC, abstractmethod


class IAzureProjectOperations(ABC):
    """
    Abstract base class for operations related to Azure DevOps projects.
    """

    def __init__(self, client):
        """
        Initializes the Azure project operations with the provided client.

        Args:
            client: The client used to interact with Azure DevOps.
        """
        self.client = client
        self.api_version = 'api-version=7.2-preview.4'

    @abstractmethod
    def execute(self, organization_name: str):
        """
        Executes the Azure DevOps project operation.

        Args:
            organization_name (str): The name of the organization to perform the operation on.
        """
