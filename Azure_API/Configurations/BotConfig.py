from Settings import BotSettings
from Configurations.ConfigUtils import ConfigUtils


class BotConfig:
    @staticmethod
    def create_bot_settings(config_file):
        bot_token = config_file.get('BOT_TOKEN')
        chat_id = config_file.get('CHAT_ID')

        ConfigUtils.check_configs(config_file=config_file, keys=['BOT_TOKEN', 'CHAT_ID'])
        return BotSettings(bot_token=bot_token, chat_id=chat_id)
