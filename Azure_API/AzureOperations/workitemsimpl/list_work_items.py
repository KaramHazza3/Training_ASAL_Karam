"""
Module defining a command to list work items in Azure DevOps.
"""

from AzureOperations import IAzureWorkItemsOperations


class ListWorkItemsCommand(IAzureWorkItemsOperations):
    """
    Command class for listing work items in Azure DevOps.
    """

    def execute(self, organization_name):
        """
        Execute the command to list work items.

        Args:
            organization_name (str): The name of the Azure DevOps organization.

        Returns:
            dict: JSON response from the Azure DevOps API.
        """
        project_identifier = input("Please enter ID OR Name of the project: ")
        ids = input("Please enter the ids (separate them by comma (,)): ")
        endpoint = (f'{organization_name}/{project_identifier}'
                    f'/_apis/wit/workitems/?ids={ids}&{self.api_version}')
        return self.client.make_request("GET", endpoint)
