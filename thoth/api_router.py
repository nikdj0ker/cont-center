from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from bitrix.api.views import PortalViewSet
from waba.api.views import WabaWebhook
# from olx.api.views import OlxAccountViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("bitrix", PortalViewSet)
router.register("waba", WabaWebhook)
# router.register("olx", OlxAccountViewSet)


app_name = "api"
urlpatterns = router.urls
