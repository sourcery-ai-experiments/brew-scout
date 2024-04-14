from unittest import mock

import pytest

from brew_scout.libs.domains.telegram import TelegramMethods
from brew_scout.libs.services.bus.client import TelegramClient


@pytest.fixture()
def payload(faker):
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


async def test_handle_telegram_hook_if_city_not_found(client, caplog, payload):
    with mock.patch.object(TelegramClient, "post", return_value=None) as mocked:
        res = await client.post("/api/v1/hook/telegram?run_now=1", json=payload)

    latitude, longitude = payload["message"]["location"]["latitude"], payload["message"]["location"]["longitude"]

    assert res.status_code == 204
    assert [f"City not found with given coordinates: {latitude} {longitude}"] == [
        record.message for record in caplog.records if record.funcName == "process_hook"
    ]
    mocked.assert_called_once_with(
        TelegramMethods.SEND_MESSAGE,
        {
            "chat_id": payload["message"]["chat"]["id"],
            "text": "Sorry, your city has not been added yet.",
            "parse_mode": "html",
        },
    )
