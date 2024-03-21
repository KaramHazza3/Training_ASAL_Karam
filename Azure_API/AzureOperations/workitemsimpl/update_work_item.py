"""
Module defining a command to update a work item in Azure DevOps.
"""

from AzureOperations import IAzureWorkItemsOperations


class UpdateWorkItemCommand(IAzureWorkItemsOperations):
    """
    Command class for updating a work item in Azure DevOps.
    """

    def execute(self, organization_name):
        """
        Execute the command to update a work item.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        work_item_id = int(input("Please enter the work item id: "))
        value = input("Please enter the new title: ")
        endpoint = f'{organization_name}/_apis/wit/workitems/{work_item_id}?{self.api_version}'
        json_data = [{
            "op": "add",
            "path": "/fields/System.Title",
            "value": value
        }]
        content_type = 'application/json-patch+json'
        return self.client.make_request("PATCH", endpoint,
                                        content_type=content_type, json=json_data)
