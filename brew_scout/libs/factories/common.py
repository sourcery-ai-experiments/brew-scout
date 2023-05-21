from fastapi import Request

from ..settings import AppSettings, SETTINGS_KEY


def settings_factory(request: Request) -> AppSettings:
    return request.app.extra[SETTINGS_KEY]
