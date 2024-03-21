"""
Module defining an asynchronous CLI manager for handling operations.
"""

from CLIManager import CLIManager


class AsyncCLIManager(CLIManager):
    """
    Asynchronous CLI manager for handling operations.
    """

    async def do_operation(self, operation: int):
        """
        Perform the specified operation asynchronously.

        Args:
            operation (int): The operation to be performed.

        Returns:
            None
        """
        command = self.commands.get(operation)
        if command:
            data = await command.execute(self.organization)
            print(data)
        else:
            print("Invalid operation")
