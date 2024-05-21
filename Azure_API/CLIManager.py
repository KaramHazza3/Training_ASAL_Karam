import asyncio
from typing import Callable, Union
from Bots.impl.TelegramBot import TelegramBOT
from Client.ClientFactory import ClientFactory
from Client.intf.IAzureClient import IAzureClient
from Configurations.BotConfig import BotConfig
from Enums.ClientType import ClientType
from Loggers.AsyncLogger import AsyncLogger
from Loggers.SyncLogger import SyncLogger


def operation_handler(func):
    if asyncio.iscoroutinefunction(func):
        return lambda *args, **kwargs: print(asyncio.run(func(*args, **kwargs)))
    else:
        return lambda *args, **kwargs: print(func(*args, **kwargs))


class CLIManager:
    @staticmethod
    def _print_welcome_message() -> None:
        print("Welcome to Azure DevOps CLI Program!")

    @staticmethod
    def _list_operations() -> str:
        """
        List available operations and prompt user to choose one.

        Returns:
            int: The chosen operation.
        """
        print("1- Create Project")
        print("2- List Projects")
        print("3- Get Project")
        print("4- Create a work item")
        print("5- List all work items")
        print("6- Get an work item")
        print("7- Update an item")
        print("8- Delete an item")
        operation = input("Choose a number for the operation you need: ")
        return operation

    @staticmethod
    def _setup_client(config_file, user_choose):
        bot_settings = BotConfig.create_bot_settings(config_file)
        telegram_bot = TelegramBOT(bot_settings)

        if user_choose == "1":
            async_logger = AsyncLogger(bot=telegram_bot)
            return ClientFactory.create_client(config_file, ClientType.ASYNC, async_logger)
        elif user_choose == "2":
            sync_logger = SyncLogger(bot=telegram_bot)
            return ClientFactory.create_client(config_file, ClientType.SYNC, sync_logger)
        raise ValueError("Invalid client type")

    @staticmethod
    def _choose_client(config_file) -> IAzureClient:
        user_choose = input("Press 1 for async and 2 for sync: ")
        return CLIManager._setup_client(config_file, user_choose)

    @staticmethod
    def run(config_file):
        client = CLIManager._choose_client(config_file)
        CLIManager._print_welcome_message()
        operation = CLIManager._list_operations()
        CLIManager._do_operation(client, operation)

    @staticmethod
    def _do_operation(client: IAzureClient, operation: str) -> Union[Callable, None]:
        if operation == "1":
            project_name = input("Provide the new project name: ")
            return operation_handler(client.create_project)(project_name)

        elif operation == "2":
            return operation_handler(client.list_projects)()

        elif operation == "3":
            project_name = input("Provide the project name you wanna retrieve: ")
            return operation_handler(client.get_project)(project_name)

        elif operation == "4":
            project_name = input("Provide the project name of the work item you wanna retrieve: ")
            work_item_type = input("Provide the work item type: ")
            work_item_title = input("Provide the work item title: ")
            return operation_handler(client.create_work_item)(project_name,
                                                              work_item_type,
                                                              work_item_title)
        elif operation == "5":
            project_name = input("Provide the project name of the work items you wanna list: ")
            return operation_handler(client.list_work_items)(project_name)

        elif operation == "6":
            project_name = input("Provide the project name of the work item you wanna retrieve: ")
            work_item_id = input("Provide the work item id: ")
            return operation_handler(client.get_work_item)(project_name, work_item_id)

        elif operation == "7":
            project_name = input("Provide the project name of the work item you wanna retrieve: ")
            work_item_id = input("Provide the work item id you wanna edit: ")
            new_title = input("Provide the new title of the work item you wanna edit: ")
            return operation_handler(client.update_work_item_title)(project_name,
                                                                    work_item_id,
                                                                    new_title)
        elif operation == "8":
            project_name = input("Provide the project name of the work item you wanna delete: ")
            work_item_id = input("Provide the work item id you wanna delete: ")
            return operation_handler(client.delete_work_item)(project_name, work_item_id)

        else:
            print("Invalid operation.")
            return None
