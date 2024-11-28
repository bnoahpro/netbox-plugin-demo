from django.urls import path

from netbox_dhcp.views import DHCPReservationRecreateView, DHCPReservationCreateView, DHCPReservationEditView, DHCPReservationDeleteView, SynchronizeDHCP, DHCPServerListView, DHCPServerView, DHCPServerEditView, DHCPServerDeleteView, DHCPReservationCreateViewIPAddress
from netbox_dhcp.models import DHCPServer, DHCPReservation
from netbox.views.generic import ObjectChangeLogView

urlpatterns = [
    ##### DHCPReservation #####
    path(route='<int:ip_address_id>/recreate',
         view=DHCPReservationRecreateView.as_view(),
         name='dhcpreservation_recreate'),
    path(route='<int:ip_address_id>/create',
         view=DHCPReservationCreateViewIPAddress.as_view(),
         name='dhcpreservation_create_ipaddress'),
    path(route='dhcpreservation/create',
         view=DHCPReservationCreateView.as_view(),
         name='dhcpreservation_create'),
    path(route='dhcpreservation/<int:pk>/edit',
         view=DHCPReservationEditView.as_view(),
         name='dhcpreservation_edit'),
    path(route='dhcpreservation/<int:pk>/delete',
         view=DHCPReservationDeleteView.as_view(),
         name='dhcpreservation_delete'),
    path(route='dhcpreservation/<int:pk>/changelog/',
         view=ObjectChangeLogView.as_view(),
         name='dhcpreservation_changelog',
         kwargs={'model': DHCPReservation}),

    ##### DHCPServer #####
    path(route='dhcpserver/<int:pk>',
         view=DHCPServerView.as_view(),
         name='dhcpserver'),
    path(route='dhcpserver/',
         view=DHCPServerListView.as_view(),
         name='dhcpserver_list'),
    path(route='dhcpserver/<int:pk>/edit',
         view=DHCPServerEditView.as_view(),
         name='dhcpserver_edit'),
    path(route='dhcpserver/add',
         view=DHCPServerEditView.as_view(),
         name='dhcpserver_add'),
    path(route='dhcpserver/<int:pk>/delete',
         view=DHCPServerDeleteView.as_view(),
         name='dhcpserver_delete'),
    path(route='dhcpserver/<int:pk>/changelog/',
         view=ObjectChangeLogView.as_view(),
         name='dhcpserver_changelog',
         kwargs={'model': DHCPServer}),

    ##### Synchronization
    path(route='dhcpserver/<int:pk>/synchonize',
         view=SynchronizeDHCP.as_view(),
         name='dhcpserver_synchronize'),
]


