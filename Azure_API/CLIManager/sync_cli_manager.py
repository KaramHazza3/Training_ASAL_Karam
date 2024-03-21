"""
Module defining a synchronous CLI manager for handling operations.
"""

from CLIManager import CLIManager


class SyncCLIManager(CLIManager):
    """
    Synchronous CLI manager for handling operations.
    """

    def do_operation(self, operation: int):
        """
        Perform the specified operation synchronously.

        Args:
            operation (int): The operation to be performed.

        Returns:
            None
        """
        command = self.commands.get(operation)
        if command:
            data = command.execute(self.organization)
            print(data)
        else:
            print("Invalid operation")
