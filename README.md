# voice_transcribation
# Идея
Бот в телеграмме, который способен распознавать голосовые сообщения и делать их текстовое представление
# План
1. Собрать датасеты по транскрибации аудио
2. Реализовать бота в телеграмм
3. Изучить существующие готовые модели для транскрибации аудио
# Состояние готового сервиса
Подготовлен функционал для работы бота в телеграмме, для транскрибации используется open source модель whisper-large-v3-russian https://huggingface.co/antony66/whisper-large-v3-russian
# Запуск
```
pip install -r bot\requirements.txt
```
```
python3 -u bot
```
# Пример работы
![image](https://github.com/user-attachments/assets/a2572834-f28d-47ff-ae1c-a1400af75fe9)
Тестовое голосовое сообщение находится в папке test_audio
# Ссылка на бота 
https://t.me/transcribe_rus_voice_bot
