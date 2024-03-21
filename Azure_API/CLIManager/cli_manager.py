"""
Module defining a CLI manager for handling operations.
"""

from abc import ABC, abstractmethod
from AzureOperations import (CreateProjectCommand, DeleteProjectCommand,
                             GetProjectCommand, ListProjectsCommand,
                             CreateWorkItemCommand, DeleteWorkItemCommand,
                             GetWorkItemCommand, ListWorkItemTypesCommand,
                             ListWorkItemsCommand, UpdateWorkItemCommand)
from Client import Client


class CLIManager(ABC):
    """
    Abstract base class defining a CLI manager for handling operations.
    """

    def __init__(self, client: Client):
        self.client = client
        self.organization = input("Please enter the organization name: ")
        self.commands = {
            1: CreateProjectCommand(client),
            2: ListProjectsCommand(client),
            3: GetProjectCommand(client),
            4: DeleteProjectCommand(client),
            5: CreateWorkItemCommand(client),
            6: ListWorkItemTypesCommand(client),
            7: ListWorkItemsCommand(client),
            8: GetWorkItemCommand(client),
            9: UpdateWorkItemCommand(client),
            10: DeleteWorkItemCommand(client)
        }

    @staticmethod
    def list_operations() -> int:
        """
        List available operations and prompt user to choose one.

        Returns:
            int: The chosen operation.
        """
        print("1- Create Project")
        print("2- List Projects")
        print("3- Get Project")
        print("4- Delete Project")
        print("5- Create a work item")
        print("6- List work item types for a process")
        print("7- List all work items")
        print("8- Get an item")
        print("9- Update an item")
        print("10- Delete an item")
        operation = input("Choose a number for the operation you need: ")
        return int(operation)

    @abstractmethod
    def do_operation(self, operation: int):
        pass
