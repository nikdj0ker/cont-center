from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from thoth.bitrix.api.views import PortalViewSet
from thoth.users.api.views import UserViewSet
from thoth.waba.api.views import WabaWebhook
from thoth.telegram.api.views import BotWebhook, UserBotWebhook

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("bitrix", PortalViewSet)
router.register("waba", WabaWebhook)
router.register("telegram/bot", BotWebhook)
router.register("telegram/userbot", UserBotWebhook)


app_name = "api"
urlpatterns = router.urls
