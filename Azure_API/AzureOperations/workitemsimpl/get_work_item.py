"""
Module defining a command to get a work item in Azure DevOps.
"""

from AzureOperations import IAzureWorkItemsOperations

class GetWorkItemCommand(IAzureWorkItemsOperations):
    """
    Command class for getting a work item in Azure DevOps.
    """

    def execute(self, organization_name):
        """
        Execute the command to get a work item.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        work_item_id = int(input("Please enter the work item id: "))
        endpoint = f'{organization_name}/_apis/wit/workitems/{work_item_id}?{self.api_version}'
        return self.client.make_request("GET", endpoint)
