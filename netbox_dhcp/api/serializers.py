from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import DHCPReservation, DHCPServer

class DHCPReservationSerializer(NetBoxModelSerializer):
    class Meta:
        model = DHCPReservation
        fields = (
            'id',
            'display',
            'mac_address',
            'ip_address_id',
            'tags',
            'created',
            'last_updated',
        )

class DHCPServerSerializer(NetBoxModelSerializer):
    class Meta:
        model = DHCPServer
        fields = (
            'id',
            'name',
            'display',
            'api_token',
            'api_url',
            'tags',
            'created',
            'last_updated',
        )
