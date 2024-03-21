import asyncio
import os
from dotenv import load_dotenv
from Logger.async_logger import AsyncLogger
from Logger.sync_logger import SyncLogger
from CLIManager import AsyncCLIManager, SyncCLIManager
from Client import ClientFactory
from Bots import AsyncTelegramBOT
from Bots import SyncTelegramBOT


async def async_mode():
    print("Welcome to Azure DevOps CLI Program!")
    file_path = input("Please provide your settings file path: ")
    bot = AsyncTelegramBOT(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))
    logger = AsyncLogger(bot=bot)
    client = ClientFactory.get_client(file_path, True, logger)

    async_cli_manager = AsyncCLIManager(client)
    operation = async_cli_manager.list_operations()
    await async_cli_manager.do_operation(operation=operation)


def sync_mode():
    print("Welcome to Azure DevOps CLI Program!")
    file_path = input("Please provide your settings file path: ")
    bot = SyncTelegramBOT(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))
    logger = SyncLogger(bot=bot)
    client = ClientFactory.get_client(file_path, False, logger)

    cli_manager = SyncCLIManager(client)
    operation = cli_manager.list_operations()
    cli_manager.do_operation(operation=operation)


def main():
    load_dotenv()
    mode = input("Please choose 'sync' or 'async' mode: ").strip().lower()
    if mode == "async":
        asyncio.run(async_mode())
    elif mode == "sync":
        sync_mode()
    else:
        print("Invalid mode. Please choose either 'sync' or 'async'.")


if __name__ == "__main__":
    main()

## C:\\Users\\Karam\\Desktop\\Azure project\\Training_Karam_Hazza\\Azure_API\\settings.ini
