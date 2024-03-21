"""
Module defining a command to create a project in Azure DevOps.
"""
from AzureOperations import IAzureProjectOperations


class CreateProjectCommand(IAzureProjectOperations):
    """
    Command class for creating a new project in Azure DevOps organization.
    """

    def execute(self, organization_name):
        """
        Executes the command to create a new project.

        Args:
            organization_name (str): The name of the organization in Azure DevOps.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        project_name = input("Please enter the project name: ")
        description = input("Please enter the description of the project: ")
        endpoint = f'{organization_name}/_apis/projects?{self.api_version}'
        json_data = {
            "name": project_name,
            "description": description,
            "capabilities": {
                "versioncontrol": {
                    "sourceControlType": "Git"
                },
                "processTemplate": {
                    "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"
                }
            },
            "visibility": "private"
        }
        return self.client.make_request("POST", endpoint, json=json_data)
