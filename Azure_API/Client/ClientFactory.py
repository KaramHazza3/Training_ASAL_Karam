from Client.impl.AzureAsyncClient import AzureAsyncClient
from Client.impl.AzureSyncClient import AzureSyncClient
from Client.intf.IAzureClient import IAzureClient
from Configurations.AzureDevOpsConfig import AzureDevOpsConfig
from Enums.ClientType import ClientType
from Loggers.ILogger import ILogger


class ClientFactory:

    @staticmethod
    def create_client(config_file, client_type: ClientType, logger: ILogger = None) -> IAzureClient:
        client_settings = AzureDevOpsConfig.create_azure_devops_settings(config_file)
        if client_type == ClientType.SYNC:
            return AzureSyncClient(azure_settings=client_settings, logger=logger)
        if client_type == ClientType.ASYNC:
            return AzureAsyncClient(azure_settings=client_settings, logger=logger)
        raise ValueError("Invalid client type")
