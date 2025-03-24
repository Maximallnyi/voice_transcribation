import os

from server import Bot
from utils import get_telegram_token


def launch_bot(telegram_token: str) -> None:
    app = Bot(telegram_token)
    app.run()


def main() -> None:
    launch_bot(
        telegram_token=get_telegram_token(),
    )


if __name__ == "__main__":
    main()
