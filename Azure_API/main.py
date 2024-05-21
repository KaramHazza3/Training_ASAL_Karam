from CLIManager import CLIManager
from Configurations.ConfigUtils import ConfigUtils


def main():
    config_file = ConfigUtils.read_config_file("AUTH")
    CLIManager.run(config_file)


if __name__ == "__main__":
    main()

## C:\\Users\\karam\Desktop\\New folder\\Training_Karam_Hazza\\Azure_API\\settings.ini
