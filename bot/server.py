from typing import List, Any

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from transformers import pipeline
import torch

from utils import get_error_message


class Bot(object):
    def __init__(
        self, token: str
    ) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.keyboard: List[Any] = []
        self.model = pipeline(
                    "automatic-speech-recognition",
                    model="antony66/whisper-large-v3-russian",
                    device="cuda" if torch.cuda.is_available() else "cpu",
                    generate_kwargs={"language": "ru", "max_new_tokens": 128},
                    return_timestamps=True
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        reply_markup = InlineKeyboardMarkup(self.keyboard)
        await update.message.reply_text(
            "Привет! Я попробую преобразовать твоё сообщение в текст.\n"
            "Пожалуйста, отправь сюда голосовое сообщение",
            reply_markup=reply_markup,
        )

    async def query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        message = await update.message.reply_text(
            "Преобразую твоё аудиосообщение ...",
            reply_to_message_id=update.message.message_id,
        )
        if update.message.voice is not None:
            audio = await update.message.voice.get_file()

        try:
            result = self.model(audio.file_path)['text']
        except Exception as exc:
            await get_error_message(context, message.chat_id)
            print(exc)
            raise RuntimeError(f"Ошибка сервиса. Причина: {exc}")

        try:
            text = result
        except Exception as exc:
            await get_error_message(context, message.chat_id)
            print(exc)

        await context.bot.delete_message(
            chat_id=message.chat_id, message_id=message.message_id
        )

        await context.bot.send_message(
            chat_id=message.chat_id,
            text=text,
        )

    def run(self) -> None:
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(
            MessageHandler(
                filters.VOICE & ~filters.COMMAND,
                self.query,
            )
        )

        print("Запускаю бота...")
        self.app.run_polling()
