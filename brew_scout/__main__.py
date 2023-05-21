import typing as t
import uvicorn
from argparse import ArgumentParser
from pydantic import PostgresDsn

from .libs.settings import AppSettings
from .libs.setup_app import setup_app


def init_args_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("--database_dsn", type=str)

    return parser


def main(database_dsn: str) -> None:
    settings = AppSettings(database_dsn=t.cast(PostgresDsn, database_dsn))
    app = setup_app(settings)
    uvicorn.run(app=app, host=settings.host, port=settings.port, http="httptools")


if __name__ == "__main__":
    parser = init_args_parser()
    args = parser.parse_args()

    main(args.database_dsn)