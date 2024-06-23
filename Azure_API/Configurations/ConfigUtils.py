import configparser


class ConfigUtils:
    @staticmethod
    def check_configs(config_file, keys):
        for key in keys:
            if key not in config_file:
                raise Exception(f"Please make sure you have a value for {key} in the config file. (settings.ini)")

    @staticmethod
    def read_config_file(section_name: str):
        config_file_path = input("Please provide the path of your config file to load: ")
        config_file = configparser.ConfigParser()
        config_file.read(config_file_path)
        return config_file[section_name]
