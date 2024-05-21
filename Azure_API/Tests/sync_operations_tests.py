import configparser

import pytest
from Bots import TelegramBOT
from Client.impl.AzureSyncClient import AzureSyncClient
from Loggers.SyncLogger import SyncLogger
from Settings import BotSettings, AzureSettings

settings_file = configparser.ConfigParser()
settings_file.read('./settings.ini')
config_file = settings_file['AUTH']


@pytest.fixture
def telegram_bot():
    bot_token = config_file['BOT_TOKEN']
    chat_id = config_file['CHAT_ID']
    bot_settings = BotSettings(bot_token=bot_token, chat_id=chat_id)
    return TelegramBOT(bot_settings)


@pytest.fixture
def sync_logger(telegram_bot):
    return SyncLogger(telegram_bot)


@pytest.fixture
def azure_settings():
    personal_access_token = config_file['PAT']
    organization_name = config_file['ORGANIZATION_NAME']
    return AzureSettings(organization_name=organization_name, pat=personal_access_token)


@pytest.fixture
def sync_client(azure_settings, sync_logger):
    return AzureSyncClient(azure_settings=azure_settings, logger=sync_logger)


def test_list_projects(sync_client):
    result = sync_client.list_projects()
    assert result.status_code == 200
    assert len(result.data) > 0


def test_create_new_project_existed(sync_client):
    result = sync_client.create_project("karamid")
    assert result.status_code == 400


def test_create_new_project_not_existed(sync_client):
    result = sync_client.create_project("ysefxz2")
    assert result.status_code == 202


def test_get_project_existed(sync_client):
    result = sync_client.get_project("karamid")
    assert result is not None


def test_get_project_not_existed(sync_client):
    result = sync_client.get_project("uuuuuuuu")
    assert result.status_code == 404


def test_list_work_items(sync_client):
    result = sync_client.list_work_items("karamid")
    assert result.status_code == 200
    assert len(result.data) > 0


def test_get_work_item_existed(sync_client):
    work_items = sync_client.list_work_items("karamid")
    assert 'workItems' in work_items.data
    work_item_id = work_items.data['workItems'][0]['id']
    result = sync_client.get_work_item("karamid", work_item_id)
    assert result.status_code == 200
    assert result.data['id'] == work_item_id


def test_get_work_item_not_existed(sync_client):
    result = sync_client.get_work_item("karamid", 500)
    assert result.status_code == 404


def test_delete_work_item_existed(sync_client):
    work_items = sync_client.list_work_items("karamid")
    assert 'workItems' in work_items.data
    work_item_id = work_items.data['workItems'][0]['id']
    result = sync_client.delete_work_item("karamid", work_item_id)
    assert result.status_code == 200


def test_delete_work_item_not_existed(sync_client):
    result = sync_client.delete_work_item("karamid", 500)
    assert result.status_code == 404


def test_create_work_item(sync_client):
    result = sync_client.create_work_item("karamid", "Task", "title from tests")
    assert result.status_code == 200
    assert result.data['fields']['System.Title'] == "title from tests"


def test_edit_work_item_existed(sync_client):
    work_items = sync_client.list_work_items("karamid")
    assert 'workItems' in work_items.data
    work_item_id = work_items.data['workItems'][0]['id']
    result = sync_client.update_work_item_title("karamid", work_item_id,
                                                'new title from tests 2')

    assert result.status_code == 200


def test_edit_work_item_not_existed(sync_client):
    result = sync_client.update_work_item_title("karamid", 500,
                                                'new title from tests 2')
    assert result.status_code == 404
