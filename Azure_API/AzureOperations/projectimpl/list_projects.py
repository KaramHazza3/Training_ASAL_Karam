"""
Module defining a command to list projects in Azure DevOps.
"""

from AzureOperations import IAzureProjectOperations


class ListProjectsCommand(IAzureProjectOperations):
    """
    Command class for listing projects in Azure DevOps organization.
    """

    def execute(self, organization_name: str):
        """
        Execute the command to list projects.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        endpoint = f'{organization_name}/_apis/projects?{self.api_version}'
        return self.client.make_request("GET", endpoint)
