"""
Module defining a command to retrieve project details from Azure DevOps.
"""

from AzureOperations import IAzureProjectOperations


class GetProjectCommand(IAzureProjectOperations):
    """
    Command class for retrieving project details from Azure DevOps organization.
    """

    def execute(self, organization_name):
        """
        Execute the command to retrieve project details.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        project_identifier = input("Please enter ID OR Name of the project: ")
        endpoint = f'{organization_name}/_apis/projects/{project_identifier}?{self.api_version}'
        return self.client.make_request("GET", endpoint)
