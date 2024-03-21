"""
Module defining a command to delete a project from Azure DevOps.
"""

from AzureOperations import IAzureProjectOperations


class DeleteProjectCommand(IAzureProjectOperations):
    """
    Command class for deleting a project from Azure DevOps organization.
    """

    def execute(self, organization_name):
        """
        Execute the command to delete a project.

        Args:
            organization_name (str): The name of the organization in Azure DevOps.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        project_id = input("Please enter the project id that you would delete: ")
        endpoint = f'{organization_name}/_apis/projects/{project_id}?{self.api_version}'
        return self.client.make_request("DELETE", endpoint)
