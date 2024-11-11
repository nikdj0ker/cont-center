import base64
import logging

import os
import wget

import asyncio

from rest_framework import status
from rest_framework.response import Response

from thoth.bitrix.crest import call_method

from .models import Bot

from aiogram import Bot as aiogram_Bot, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

logger = logging.getLogger("django")


async def get_file(token, media_id):
    bot = aiogram_Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    file = await bot.get_file(media_id)
    full_file_path = f"media/{file.file_path}"
    await bot.download(media_id, full_file_path)
    await bot.session.close()
    return full_file_path


def upload_file_to_bitrix(media_id, full_file_path, appinstance, storage_id):
    filename = full_file_path.split("/")[-1]
    with open(full_file_path, 'rb') as media_file:
        fileContent = base64.b64encode(media_file.read()).decode('utf-8')

    payload = {
        "id": storage_id,
        "fileContent": fileContent,
        # "data": {"NAME": f"{media_id}_{filename}"},
        "data": {"NAME": f"{filename}"}
    }

    upload_to_bitrix = call_method(appinstance, "disk.storage.uploadfile", payload)
    # print(upload_to_bitrix)
    os.remove(full_file_path)

    if "result" in upload_to_bitrix:
        return [upload_to_bitrix["result"]["DOWNLOAD_URL"], upload_to_bitrix["result"]["ID"]]
    # elif "error" in upload_to_bitrix:
    #     storage_id = call_method(appinstance, "disk.storage.getforapp", {})['result']['ID']
    #     data = call_method(appinstance, "disk.storage.getchildren", {"id": storage_id})
    #     files = data.get("result", [])
    #     for file in files:
    #         if file.get("NAME") == filename:
    #             print(file.get("DOWNLOAD_URL"))
    #             return file.get("DOWNLOAD_URL")
    else:
        return None


async def send_message(token, user_id, text):
    bot = aiogram_Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.send_message(user_id, text)
    await bot.session.close()


async def send_photo(token, user_id, file_url):
    bot = aiogram_Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.send_photo(user_id, file_url)
    await bot.session.close()


async def send_video(token, user_id, file_url, filename):
    bot = aiogram_Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    file = wget.download(file_url, filename)
    video = types.FSInputFile(path=file)
    await bot.send_video(user_id, video)
    os.remove(file)
    await bot.session.close()


async def send_document(token, user_id, file_url, filename):
    bot = aiogram_Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    file = wget.download(file_url, filename)
    document = types.FSInputFile(path=file)
    await bot.send_document(user_id, document)
    os.remove(file)
    await bot.session.close()


def message_processing(request):
    # print(request)
    # print(request.query_params)
    # print(request.headers)
    # print(request.data)

    data = request.data
    logger.debug(f"Request from telegram: {data}")
    message_data = {
        "CONNECTOR": "thoth_telegram",
        "MESSAGES": [{"user": {}, "chat": {}, "message": {}}],
    }
    message_data["MESSAGES"][0]["user"]["skip_phone_validate"] = "Y"

    bot_name = data["bot_name"]

    try:
        bot = Bot.objects.get(bot_name=bot_name)
        token = bot.bot_token
        appinstance = bot.app_instance
        storage_id = bot.app_instance.storage_id
    except Bot.DoesNotExist:
        return Response(
            {"error": "Bot with given bot_name not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    message_data["LINE"] = bot.line.line_id

    message_data["MESSAGES"][0]["user"]["id"] = data["user_id"]
    message_data["MESSAGES"][0]["user"]["phone"] = data["phone"]
    message_data["MESSAGES"][0]["user"]["name"] = data["first_name"]
    message_data["MESSAGES"][0]["user"]["last_name"] = data["last_name"]

    message_data["MESSAGES"][0]["chat"]["id"] = data["user_id"]

    messages = data.get("messages", [])
    for message in messages:
        file_id = str
        message_type = message.get("type")
        if message_type == "text":
            message_data["MESSAGES"][0]["message"]["text"] = message["text"]

        elif message_type in ["image", "video", "audio", "document"]:
            media_id = message["id"]

            full_file_path = asyncio.run(get_file(token, media_id))
            file_url, file_id = upload_file_to_bitrix(media_id, full_file_path, appinstance, storage_id)

            if file_url:
                message_data["MESSAGES"][0]["message"]["files"] = [{}]
                message_data["MESSAGES"][0]["message"]["files"][0]["url"] = file_url
                message_data["MESSAGES"][0]["message"]["text"] = message["caption"]

        call_method(appinstance, "imconnector.send.messages", message_data)
        call_method(appinstance, "disk.file.delete", {"id": file_id})

    return Response({"status": "received"}, status=status.HTTP_200_OK)
