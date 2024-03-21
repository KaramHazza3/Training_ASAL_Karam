import os

import pytest
from Bots import SyncTelegramBOT
from Client import ClientFactory
from Logger.sync_logger import SyncLogger
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def project_json():
    return {
        "name": "yahyaAbbadi",
        "description": "its a project for testing",
        "capabilities": {
            "versioncontrol": {"sourceControlType": "Git"},
            "processTemplate": {"templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"}
        },
        "visibility": "private"
    }


@pytest.fixture
def bad_project_json():
    return {
        "name": "",
        "description": "its a project for testing",
        "capabilities": {
            "versioncontrol": {"sourceControlType": "Git"},
            "processTemplate": {"templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"}
        },
        "visibility": "private"
    }


@pytest.fixture
def work_item_json():
    return [{
        "op": "add",
        "path": "/fields/System.Title",
        "from": "null",
        "value": "testing"
    }]


@pytest.fixture
def bad_work_item_json():
    return [{
        "op": "blalabla",
        "path": "/fields/System.Title",
        "from": "null",
        "value": ""
    }]


@pytest.fixture()
def work_item_with_id_and_destroy_endpoint():
    return ("https://dev.azure.com/karamanaxd2017/karamid/_apis/wit/workitems"
            "/11?destroy=True&api-version=7.2-preview.3")


@pytest.fixture()
def work_item_create_bad_endpoint():
    return "https://dev.azure.com/karamanaxd2017/karamid/_apis/wit/workitems/$task?api-version=7.2-preview.3"


@pytest.fixture()
def work_item_create_endpoint():
    return "https://dev.azure.com/karamanaxd2017/karamid/_apis/wit/workitems/$task?api-version=7.2-preview.3"


@pytest.fixture()
def work_item_with_id_endpoint():
    return "https://dev.azure.com/karamanaxd2017/karamid/_apis/wit/workitems/12?api-version=7.2-preview.3"


@pytest.fixture()
def work_item_with_bad_id_endpoint():
    return "https://dev.azure.com/karamanaxd2017/karamid/_apis/wit/workitems/9121?api-version=7.2-preview.3"


@pytest.fixture()
def project_endpoint():
    return "https://dev.azure.com/karamanaxd2017/_apis/projects?api-version=7.2-preview.4"


@pytest.fixture()
def project_endpoint_with_id():
    return ("https://dev.azure.com/karamanaxd2017/_apis/projects/"
            "ddf8d283-c2ac-4888-ae41-b0b86f5c0746?api-version=7.2-preview.4")


@pytest.fixture()
def project_endpoint_with_bad_name():
    return "https://dev.azure.com/karamanaxd2017/_apis/projects/alolololo?api-version=7.2-preview.4"


@pytest.fixture()
def project_endpoint_with_name():
    return "https://dev.azure.com/karamanaxd2017/_apis/projects/karam?api-version=7.2-preview.4"


@pytest.fixture
def client(settings_file, logger):
    return ClientFactory.get_client(settings_file, False, logger)


@pytest.fixture
def settings_file():
    return 'C:\\Users\\Karam\\Desktop\\Azure project\\Training_Karam_Hazza\\Azure_API\\settings.ini'


@pytest.fixture()
def logger(bot):
    return SyncLogger(bot)


@pytest.fixture()
def bot():
    return SyncTelegramBOT(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))


def test_create_project_success(client, project_endpoint, project_json):
    result = client.make_request("POST", project_endpoint, json=project_json)
    assert result.status_code == 202


# def test_create_project_failure(client, project_endpoint, bad_project_json):
#     result = create_client.make_request("POST", project_endpoint, json=bad_project_json)
#     assert result.status_code == 400
#
#
# def test_list_projects_success(client, project_endpoint):
#     result = client.make_request("GET", project_endpoint)
#     returned_result = result.data
#     project_count = returned_result['count']
#     assert result.status_code == 200
#     assert project_count == 32
#
#
# def test_list_projects_failure(client, project_endpoint):
#     result = client.make_request("GET", project_endpoint)
#     returned_result = result.data
#     project_count = returned_result['count']
#     assert result.status_code != 404
#     assert project_count != 100
#
#
# def test_get_project_success(client, project_endpoint_with_name):
#     result = client.make_request("GET", project_endpoint_with_name)
#     assert result.status_code == 200
#
#
# def test_get_project_failure(client, project_endpoint_with_bad_name):
#     result = client.make_request("GET", project_endpoint_with_bad_name)
#     assert result.status_code == 404
#
#
# def test_delete_project_success(client, project_endpoint_with_id):
#     result = client.make_request("DELETE", project_endpoint_with_id)
#     assert result.status_code == 202
#
#
# def test_delete_project_failure(client, project_endpoint_with_id):
#     result = client.make_request("DELETE", project_endpoint_with_id)
#     assert result.status_code == 404
#
#
# def test_create_work_item_success(client, work_item_create_endpoint, work_item_json):
#     content_type = 'application/json-patch+json'
#     result = client.make_request("POST", work_item_create_endpoint, content_type=content_type, json=work_item_json)
#     assert result.status_code == 200
#
#
# def test_create_work_item_failure(client, work_item_create_bad_endpoint, bad_work_item_json):
#     content_type = 'application/json-patch+json'
#     result = client.make_request("POST", work_item_create_bad_endpoint, content_type=content_type, json=bad_work_item_json)
#     assert result.status_code == 400
#
#
# def test_get_work_item_success(client, work_item_with_id_endpoint):
#     result = client.make_request("GET", work_item_with_id_endpoint)
#     assert result.status_code == 200
#
#
# def test_get_work_item_failure(client, work_item_with_bad_id_endpoint):
#     result = client.make_request("GET", work_item_with_bad_id_endpoint)
#     assert result.status_code == 404
#
#
# def test_delete_work_item_success(client, work_item_with_id_and_destroy_endpoint):
#     result = client.make_request("DELETE", work_item_with_id_and_destroy_endpoint)
#     assert result.status_code == 204
#     assert result.data == ""
#
#
# def test_update_work_item(client, work_item_with_id_endpoint, work_item_json):
#     content_type = 'application/json-patch+json'
#     result = client.make_request("PATCH", work_item_with_id_endpoint, content_type=content_type, json=work_item_json)
#     returned_result = result.data
#     changed_title = returned_result['fields']['System.Title']
#     assert result.status_code == 200
#     assert changed_title == "testing"
