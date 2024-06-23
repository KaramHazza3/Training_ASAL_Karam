from Settings import AzureSettings
from Configurations.ConfigUtils import ConfigUtils


class AzureDevOpsConfig:

    @staticmethod
    def create_azure_devops_settings(config_file):
        pat = config_file.get('PAT')
        organization_name = config_file.get('ORGANIZATION_NAME')

        ConfigUtils.check_configs(config_file=config_file, keys=['PAT', 'ORGANIZATION_NAME'])
        return AzureSettings(pat=pat, organization_name=organization_name)
