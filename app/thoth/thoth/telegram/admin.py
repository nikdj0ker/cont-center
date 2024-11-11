from django.contrib import admin
from django.contrib import messages

from thoth.bitrix.crest import call_method
from thoth.bitrix.models import Line
from thoth.bitrix.utils import messageservice_add

from .models import Bot, UserBot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ("bot_name", "bot_token", "owner", "line", "sms_service")
    search_fields = ("bot_name",)
    fields = (
        "app_instance",
        "bot_name",
        "bot_token",
        "owner",
        "line",
        # "sms_service",
    )
    readonly_fields = (
        "line", )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # создание открытой линии
        if not obj.line:
            line_data = {
                "PARAMS": {
                    "LINE_NAME": obj.bot_name,
                },
            }

            create_line = call_method(
                obj.app_instance, "imopenlines.config.add", line_data
            )

            # активация открытой линии
            if "result" in create_line:
                line = Line.objects.create(
                    line_id=create_line["result"],
                    app_instance=obj.app_instance,
                )
                obj.line = line
                obj.save()

                payload = {
                    "CONNECTOR": "thoth_telegram",
                    "LINE": line.line_id,
                    "ACTIVE": 1,
                }

                call_method(obj.app_instance, "imconnector.activate", payload)


        # Регистрация SMS-провайдера
        if obj.sms_service and not obj.old_sms_service:
            # Проверка наличия объекта auth_token
            owner = obj.line.app_instance.app.owner
            if not hasattr(owner, 'auth_token'):
                obj.sms_service = False
                obj.save()
                messages.error(request, f"API key not found for user {owner}. Operation aborted.")
                return

            api_key = owner.auth_token.key
            resp = messageservice_add(obj.app_instance, obj.bot_name, obj.line.line_id, api_key, 'telegram')
            if 'error' in resp:
                obj.sms_service = False
                obj.save()
                messages.error(request, resp)

        elif not obj.sms_service and obj.old_sms_service:
            name = ''.join(filter(str.isalnum, obj.bot_name))
            resp = call_method(
                obj.app_instance,
                "messageservice.sender.delete",
                {"CODE": f"THOTH_{name}_{obj.line.line_id}"},
            )
            if 'error' in resp:
                messages.error(request, resp)

        obj.old_sms_service = obj.sms_service
        obj.save()


@admin.register(UserBot)
class UserBotAdmin(admin.ModelAdmin):
    list_display = ("userbot_name", "api_id", "api_hash", "owner", "line", "sms_service")
    search_fields = ("userbot_name",)
    fields = (
        "app_instance",
        "userbot_name",
        "api_id",
        "api_hash",
        "owner",
        "line",
        # "sms_service",
    )
    readonly_fields = (
        "line", )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # создание открытой линии
        if not obj.line:
            line_data = {
                "PARAMS": {
                    "LINE_NAME": obj.userbot_name,
                },
            }

            create_line = call_method(
                obj.app_instance, "imopenlines.config.add", line_data
            )

            # активация открытой линии
            if "result" in create_line:
                line = Line.objects.create(
                    line_id=create_line["result"],
                    app_instance=obj.app_instance,
                )
                obj.line = line
                obj.save()

                payload = {
                    "CONNECTOR": "thoth_telegram",
                    "LINE": line.line_id,
                    "ACTIVE": 1,
                }

                call_method(obj.app_instance, "imconnector.activate", payload)


        # Регистрация SMS-провайдера
        if obj.sms_service and not obj.old_sms_service:
            # Проверка наличия объекта auth_token
            owner = obj.line.app_instance.app.owner
            if not hasattr(owner, 'auth_token'):
                obj.sms_service = False
                obj.save()
                messages.error(request, f"API key not found for user {owner}. Operation aborted.")
                return

            api_key = owner.auth_token.key
            resp = messageservice_add(obj.app_instance, obj.userbot_name, obj.line.line_id, api_key, 'telegram')
            if 'error' in resp:
                obj.sms_service = False
                obj.save()
                messages.error(request, resp)

        elif not obj.sms_service and obj.old_sms_service:
            name = ''.join(filter(str.isalnum, obj.userbot_name))
            resp = call_method(
                obj.app_instance,
                "messageservice.sender.delete",
                {"CODE": f"THOTH_{name}_{obj.line.line_id}"},
            )
            if 'error' in resp:
                messages.error(request, resp)

        obj.old_sms_service = obj.sms_service
        obj.save()
