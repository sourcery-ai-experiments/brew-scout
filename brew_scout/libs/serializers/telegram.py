from pydantic import BaseModel


class Common(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    username: str


class From(Common):
    is_bot: bool
    language_code: str


class Chat(Common):
    type: str


class Location(BaseModel):
    latitude: float
    longitude: float


class Message(BaseModel):
    message_id: int
    message_from: From
    chat: Chat
    date: int
    text: str | None
    location: Location | None

    class Config:
        fields = {"message_from": "from"}


class TelegramHookIn(BaseModel):
    update_id: int
    message: Message
