from django.db.models import Count
from netbox.api.viewsets import NetBoxModelViewSet
from ..models import DHCPServer
from .serializers import DHCPServerSerializer


class DHCPServerViewSet(NetBoxModelViewSet):
    queryset = DHCPServer.objects.prefetch_related('tags')
    serializer_class =  DHCPServerSerializer
