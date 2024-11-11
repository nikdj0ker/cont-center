import logging

import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.views import APIView

from thoth.olx.models import OlxApp
from thoth.olx.models import OlxUser

from .serializers import OlxAuthorizationSerializer

logger = logging.getLogger("olx")


class OlxAuthorizationAPIView(LoginRequiredMixin, APIView):
    serializer_class = OlxAuthorizationSerializer

    login_url = "/accounts/login/"

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        if not serializer.is_valid():
            for field, error in serializer.errors.items():
                messages.error(request, f"{field.capitalize()}: {error[0]}")
            return redirect("olx-accounts")

        code = serializer.validated_data["code"]
        state = serializer.validated_data["state"]

        account = get_object_or_404(OlxApp, id=state)

        if not account:
            messages.error(request, "Account not found")
            return redirect("olx-accounts")

        token_url = f"https://www.{account.client_domain}/api/open/oauth/token"
        payload = {
            "grant_type": "authorization_code",
            "scope": "v2 read write",
            "code": code,
            "client_id": account.client_id,
            "client_secret": account.client_secret,
        }

        response = requests.post(token_url, json=payload)
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")

            # Запрос данных пользователя
            user_info_url = f"https://www.{account.client_domain}/api/partner/users/me"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Version": "2.0",
            }

            user_info_response = requests.get(user_info_url, headers=headers)
            if user_info_response.status_code == 200:
                user_data = user_info_response.json().get("data", {})

                olx_id = str(user_data["id"])
                olx_user = OlxUser.objects.filter(olx_id=olx_id, olxapp=account).first()

                if olx_user:
                    # Проверка, что текущий пользователь является владельцем olx_user
                    if olx_user.owner != request.user:
                        messages.error(
                            request,
                            f"You do not have permission to update this OLX account ({olx_user.email})",
                        )
                        return redirect("olx-accounts")

                    # Обновление токенов для существующего пользователя
                    olx_user.access_token = access_token
                    olx_user.refresh_token = refresh_token
                    olx_user.save()
                    messages.success(request, "OLX Tokens successfully updated")
                else:
                    # Создание нового пользователя с указанием владельца
                    OlxUser.objects.create(
                        olxapp=account,
                        olx_id=olx_id,
                        email=user_data["email"],
                        name=user_data["name"],
                        phone=user_data["phone"],
                        access_token=access_token,
                        refresh_token=refresh_token,
                        owner=request.user,
                    )
                    messages.success(request, "OLX Account successfully added")

                return redirect("olx-accounts")

            else:
                logger.error(response.json())
                messages.error(request, "Failed to retrieve user information")
                return redirect("olx-accounts")

        else:
            logger.error(f"Failed to obtain tokens: {response.json()}")
            messages.error(request, f"Failed to obtain tokens: {response.json()}")
            return redirect("olx-accounts")
