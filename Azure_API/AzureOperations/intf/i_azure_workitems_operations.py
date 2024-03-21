"""
Module defining an abstract base class for operations related to Azure DevOps work items.
"""

from abc import ABC, abstractmethod


class IAzureWorkItemsOperations(ABC):
    """
    Abstract base class defining operations related to Azure DevOps work items.
    """

    def __init__(self, client):
        """
        Initializes the Azure work items operations with the provided client.

        Args:
            client: The client used to interact with Azure DevOps.
        """
        self.client = client
        self.api_version = 'api-version=7.2-preview.3'

    @abstractmethod
    def execute(self, organization_name):
        """
        Executes the Azure DevOps work item operation.
        """
