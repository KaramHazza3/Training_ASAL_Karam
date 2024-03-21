"""
Module defining a command to create a work item in Azure DevOps.
"""

from AzureOperations import IAzureWorkItemsOperations


class CreateWorkItemCommand(IAzureWorkItemsOperations):
    """
    Command class for creating a work item in Azure DevOps.
    """

    def execute(self, organization_name):
        """
        Execute the command to create a work item.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        project_identifier = input("Please enter ID OR Name of the project: ")
        item_type = input("Please enter the type of the work item: ")
        value = input("Please enter the title of the work item: ")
        endpoint = (f'{organization_name}/{project_identifier}/_apis/wit/workitems'
                    f'/${item_type}?{self.api_version}')
        json_data = [{
            "op": "add",
            "path": "/fields/System.Title",
            "from": "null",
            "value": value
        }]
        content_type = 'application/json-patch+json'
        return self.client.make_request("POST", endpoint, content_type=content_type, json=json_data)
