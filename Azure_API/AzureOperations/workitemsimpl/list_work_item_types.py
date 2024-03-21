"""
Module defining a command to list work item types in Azure DevOps.
"""

from AzureOperations import IAzureWorkItemsOperations

class ListWorkItemTypesCommand(IAzureWorkItemsOperations):
    """
    Command class for listing work item types in Azure DevOps.
    """

    def execute(self, organization_name):
        """
        Execute the command to list work item types.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        process_id = input("Please enter the process id: ")
        endpoint = (f'{organization_name}/_apis/work/processes/{process_id}'
                    f'/workitemtypes?api-version=6.0-preview.2')
        return self.client.make_request("GET", endpoint)
