from Configurations.BotConfig import BotConfig
from Enums.BotType import BotType
from .impl.TelegramBot import TelegramBOT


class BotFactory:
    @staticmethod
    def create_bot(config_file, bot_type: BotType):
        bot_settings = BotConfig.create_bot_settings(config_file)
        if bot_type == BotType.TELEGRAM:
            return TelegramBOT(bot_settings)
