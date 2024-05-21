import configparser

import pytest
from Bots import TelegramBOT
from Client.impl.AzureAsyncClient import AzureAsyncClient
from Loggers.AsyncLogger import AsyncLogger
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
def async_logger(telegram_bot):
    return AsyncLogger(telegram_bot)


@pytest.fixture
def azure_settings():
    personal_access_token = config_file['PAT']
    organization_name = config_file['ORGANIZATION_NAME']
    return AzureSettings(organization_name=organization_name, pat=personal_access_token)


@pytest.fixture
def async_client(azure_settings, async_logger):
    return AzureAsyncClient(azure_settings=azure_settings, logger=async_logger)


@pytest.mark.asyncio
async def test_list_projects(async_client):
    result = await async_client.list_projects()
    assert result.status_code == 200
    assert len(result.data) > 0


@pytest.mark.asyncio
async def test_create_new_project_existed(async_client):
    result = await async_client.create_project("karamid")
    assert result.status_code == 400


@pytest.mark.asyncio
async def test_create_new_project_not_existed(async_client):
    result = await async_client.create_project("ysefxz2")
    assert result.status_code == 202


@pytest.mark.asyncio
async def test_get_project_existed(async_client):
    result = await async_client.get_project("karamid")
    assert result is not None


@pytest.mark.asyncio
async def test_get_project_not_existed(async_client):
    result = await async_client.get_project("uuuuuuuu")
    assert result.status_code == 404


@pytest.mark.asyncio
async def test_list_work_items(async_client):
    result = await async_client.list_work_items("karamid")
    assert result.status_code == 200
    assert len(result.data) > 0


@pytest.mark.asyncio
async def test_get_work_item_existed(async_client):
    work_items = await async_client.list_work_items("karamid")
    assert 'workItems' in work_items.data
    work_item_id = work_items.data['workItems'][0]['id']
    result = await async_client.get_work_item("karamid", work_item_id)
    assert result.status_code == 200
    assert result.data['id'] == work_item_id


@pytest.mark.asyncio
async def test_get_work_item_not_existed(async_client):
    result = await async_client.get_work_item("karamid", 500)
    assert result.status_code == 404


@pytest.mark.asyncio
async def test_delete_work_item_existed(async_client):
    work_items = await async_client.list_work_items("karamid")
    assert 'workItems' in work_items.data
    work_item_id = work_items.data['workItems'][0]['id']
    result = await async_client.delete_work_item("karamid", work_item_id)
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_delete_work_item_not_existed(async_client):
    result = await async_client.delete_work_item("karamid", 500)
    assert result.status_code == 404


@pytest.mark.asyncio
async def test_create_work_item(async_client):
    result = await async_client.create_work_item("karamid", "Task", "title from tests")
    assert result.status_code == 200
    assert result.data['fields']['System.Title'] == "title from tests"


@pytest.mark.asyncio
async def test_edit_work_item_existed(async_client):
    work_items = await async_client.list_work_items("karamid")
    assert 'workItems' in work_items.data
    work_item_id = work_items.data['workItems'][0]['id']
    result = await async_client.update_work_item_title("karamid", work_item_id,
                                                       'new title from tests 2')

    assert result.status_code == 200


@pytest.mark.asyncio
async def test_edit_work_item_not_existed(async_client):
    result = await async_client.update_work_item_title("karamid", 500,
                                                       'new title from tests 2')
    assert result.status_code == 404
