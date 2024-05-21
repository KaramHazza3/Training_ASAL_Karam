from abc import ABC, abstractmethod
from Loggers.ILogger import ILogger
from Settings import response, AzureSettings


class IAzureClient(ABC):
    def __init__(self, azure_settings: AzureSettings, logger: ILogger):
        self.azure_settings = azure_settings

        self.base_url = azure_settings.base_url
        self.headers = self.azure_settings.get_header()
        self.logger = logger

        self.event_hooks = {
            'request': [self.logger.log_request],
            'response': [self.logger.log_response],
        }

    @abstractmethod
    def _make_request(self, method: str, url: str, content_type='application/json', **kwargs
                      ) -> response:
        pass

    @abstractmethod
    def create_project(self, project_name: str) -> response:
        pass

    @abstractmethod
    def list_projects(self):
        pass

    @abstractmethod
    def get_project(self, project_name: str) -> response:
        pass

    @abstractmethod
    def list_work_items(self, project_name: str) -> response:
        pass

    @abstractmethod
    def get_work_item(self, project_name: str, work_item_id: str) -> response:
        pass

    @abstractmethod
    def delete_work_item(self, project_name: str, work_item_id: str) -> response:
        pass

    @abstractmethod
    def create_work_item(self, project_name: str, work_item_type: str, work_item_title: str) -> response:
        pass

    @abstractmethod
    def update_work_item_title(self, project_name: str, work_item_id: str, title: str) -> response:
        pass
