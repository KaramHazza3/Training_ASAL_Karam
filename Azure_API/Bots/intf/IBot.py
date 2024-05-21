from abc import ABC, abstractmethod


class IBot(ABC):
    @abstractmethod
    def send_message_async(self, message):
        pass

    @abstractmethod
    def send_message(self, message):
        pass
