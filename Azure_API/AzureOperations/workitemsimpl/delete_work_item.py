"""
Module defining a command to delete a work item in Azure DevOps.
"""

from AzureOperations import IAzureWorkItemsOperations

class DeleteWorkItemCommand(IAzureWorkItemsOperations):
    """
    Command class for deleting a work item in Azure DevOps.
    """

    def execute(self, organization_name):
        """
        Execute the command to delete a work item.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        work_item_id = int(input("Please enter the work item id: "))
        destroy = input("Do you want to destroy it? Write 'yes' to confirm: ").lower() == 'yes'
        endpoint = (f'{organization_name}/_apis/wit/workitems'
                    f'/{work_item_id}?destroy={destroy}&{self.api_version}')
        return self.client.make_request("DELETE", endpoint)
