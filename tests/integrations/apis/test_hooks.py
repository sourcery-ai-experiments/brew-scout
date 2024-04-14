from unittest import mock

import pytest

from brew_scout.libs.domains.telegram import TelegramMethods
from brew_scout.libs.services.bus.client import TelegramClient


@pytest.fixture()
def start_payload(faker):
    first_name, last_name, username = faker.first_name(), faker.last_name(), faker.user_name()

    return {
        "update_id": faker.pyint(),
        "message": {
            "message_id": faker.pyint(),
            "from": {
                "id": faker.pyint(),
                "is_bot": "false",
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
                "username": f"{username}",
                "language_code": "en",
            },
            "chat": {
                "id": faker.pyint(),
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
                "username": f"{username}",
                "type": "private",
            },
            "date": 1713100485,
            "text": "/start",
            "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
        },
    }


@pytest.fixture()
def location_payload(faker):
    first_name, last_name, username = faker.first_name(), faker.last_name(), faker.user_name()

    return {
        "update_id": faker.pyint(),
        "message": {
            "message_id": faker.pyint(),
            "from": {
                "id": faker.pyint(),
                "is_bot": "false",
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
                "username": f"{username}",
                "language_code": "en",
            },
            "chat": {
                "id": faker.pyint(),
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
                "username": f"{username}",
                "type": "private",
            },
            "date": 1713014702,
            "location": {"latitude": faker.pyfloat(), "longitude": faker.pyfloat()},
        },
    }


async def test_handle_telegram_hook_if_start_message(client, caplog, start_payload):
    with mock.patch.object(TelegramClient, "post", return_value=None) as mocked:
        res = await client.post("/api/v1/hook/telegram?run_now=1", json=start_payload)

    assert res.status_code == 204
    assert [f'Start message from @{start_payload["message"]["chat"]["username"]}'] == [
        record.message for record in caplog.records if record.funcName == "process_hook"
    ]
    mocked.assert_called_once_with(
        TelegramMethods.SEND_MESSAGE,
        {
            "chat_id": start_payload["message"]["chat"]["id"],
            "text": "Hi there, send me your location and I will try to find some coffee shops in your area.",
            "parse_mode": "html",
            "reply_markup": '{"keyboard":[[{"text":"📍 Current location","request_location":true}]],"one_time_keyboard":true,"resize_keyboard":true}',
        },
    )


async def test_handle_telegram_hook_if_city_not_found(client, caplog, location_payload):
    with mock.patch.object(TelegramClient, "post", return_value=None) as mocked:
        res = await client.post("/api/v1/hook/telegram?run_now=1", json=location_payload)

    latitude, longitude = (
        location_payload["message"]["location"]["latitude"],
        location_payload["message"]["location"]["longitude"],
    )

    assert res.status_code == 204
    assert [f"City not found with given coordinates: {latitude} {longitude}"] == [
        record.message for record in caplog.records if record.funcName == "process_hook"
    ]
    mocked.assert_called_once_with(
        TelegramMethods.SEND_MESSAGE,
        {
            "chat_id": location_payload["message"]["chat"]["id"],
            "text": "Sorry, your city has not been added yet.",
            "parse_mode": "html",
        },
    )
