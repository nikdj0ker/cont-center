from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet

from thoth.bitrix.models import Bitrix

from ..utils import event_processor
from ..utils import process_placement
from ..utils import sms_processor
from .serializers import PortalSerializer


class PortalViewSet(CreateModelMixin, GenericViewSet, ListModelMixin):
    queryset = Bitrix.objects.all()
    serializer_class = PortalSerializer

    def create(self, request, *args, **kwargs):
        return event_processor(request)


class PlacementOptionsViewSet(GenericViewSet, CreateModelMixin):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return Bitrix.objects.none()

    def create(self, request, *args, **kwargs):
        return process_placement(request)


class SmsViewSet(GenericViewSet, CreateModelMixin):
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return Bitrix.objects.none()

    def create(self, request, *args, **kwargs):
        return sms_processor(request)