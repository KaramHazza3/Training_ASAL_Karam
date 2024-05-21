from typing import Union, Dict, Iterable
from urllib.parse import urljoin
import httpx
from Client.intf.IAzureClient import IAzureClient
from Settings import response, SuccessResponse, ErrorResponse


class AzureAsyncClient(IAzureClient):

    async def _make_request(self, method: str, url: str, content_type='application/json', **kwargs
                            ) -> response:
        """
        Make an asynchronous HTTP request.

        Args:
            method (str): The HTTP method (e.g., GET, POST).
            url (str): The URL to which the request is made.
            content_type (str, optional): The content type of the request.
             Defaults to 'application/json'.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Union[SuccessResponse, ErrorResponse]: A SuccessResponse or ErrorResponse object.
        """
        self.headers['Content-Type'] = content_type
        async with httpx.AsyncClient(event_hooks=self.event_hooks if hasattr(self, 'event_hooks') else None) as client:
            result_response = await client.request(method,
                                                   urljoin(self.azure_settings.base_url, url),
                                                   headers=self.headers, **kwargs)
            if result_response.status_code == 204:
                return SuccessResponse(status_code=result_response.status_code, data="")
            if result_response.is_success:
                return SuccessResponse(status_code=result_response.status_code, data=result_response.json())
            return ErrorResponse(status_code=result_response.status_code, error=result_response.text)

    async def create_project(self, project_name: str) -> response:

        endpoint = f'{self.azure_settings.organization_name}/_apis/projects?{self.azure_settings.api_version}'

        data: Dict = {
            "name": project_name,
            "description": f"this is a project for {project_name}",
            "capabilities": {
                "versioncontrol": {
                    "sourceControlType": "Git"
                },
                "processTemplate": {
                    "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"
                }
            }
        }
        return await self._make_request("POST", url=endpoint, json=data)

    async def list_projects(self):

        endpoint = f'{self.azure_settings.organization_name}/_apis/projects?{self.azure_settings.api_version}'
        return await self._make_request("GET", url=endpoint)

    async def get_project(self, project_identifier: str) -> response:

        endpoint = (f'{self.azure_settings.organization_name}/_apis/projects/{project_identifier}?'
                    f'{self.azure_settings.api_version}')
        return await self._make_request("GET", url=endpoint)

    async def list_work_items(self, project_name: str) -> response:

        endpoint = f'{self.azure_settings.organization_name}/{project_name}/_apis/wit/wiql?{self.azure_settings.api_version}'
        data: Dict = {
            "query": "SELECT [Id] from WorkItems"
        }
        return await self._make_request("POST", url=endpoint, json=data)

    async def get_work_item(self, project_name: str, work_item_id: str) -> response:

        endpoint = (f'{self.azure_settings.organization_name}/{project_name}/_apis/wit/WorkItems/{work_item_id}'
                    f'?{self.azure_settings.api_version}')
        return await self._make_request("GET", url=endpoint)

    async def delete_work_item(self, project_name: str, work_item_id: str) -> response:

        endpoint = (f'{self.azure_settings.organization_name}/{project_name}/_apis/wit/WorkItems/{work_item_id}'
                    f'?{self.azure_settings.api_version}')
        return await self._make_request("DELETE", endpoint)

    async def create_work_item(self, project_name: str, work_item_type: str, work_item_title: str) -> response:
        endpoint = (f'{self.azure_settings.organization_name}/{project_name}/_apis/wit/WorkItems/${work_item_type}'
                    f'?{self.azure_settings.api_version}')
        data: Iterable[Dict] = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": work_item_title
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": "This is a new work item"
            }
        ]
        return await self._make_request("POST", endpoint, content_type= 'application/json-patch+json', json=data)

    async def update_work_item_title(self, project_name: str, work_item_id: str, title: str) -> response:
        endpoint = (f'{self.azure_settings.organization_name}/{project_name}/_apis/wit/WorkItems/{work_item_id}'
                    f'?{self.azure_settings.api_version}')
        data: Iterable[Dict] = [{
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        }]
        return await self._make_request("patch", endpoint, content_type= 'application/json-patch+json', json=data)
