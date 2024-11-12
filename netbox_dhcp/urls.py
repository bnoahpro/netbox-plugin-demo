from django.urls import path
from .views import DHCPReservationRecreateView, MacAddressCreateView, MacAddressEditView, MacAddressDeleteView, MacAddressView, SynchronizeDHCP

urlpatterns = [
    path(route='<int:ip_address_id>/recreate',
         view=DHCPReservationRecreateView.as_view(),
         name='reservation_recreate'),
    path(route='<int:prefix_id>/synchonize',
         view=SynchronizeDHCP.as_view(),
         name='synchonize_dhcp'),
    path(route='mac-address/<int:pk>',
         view=MacAddressView.as_view(),
         name='mac_address_create'),
    path(route='mac-address/create/',
         view=MacAddressCreateView.as_view(),
         name='mac_address_create'),
    path(route='mac-address/<int:pk>/edit',
         view=MacAddressEditView.as_view(),
         name='mac_address_edit'),
    path(route='mac-address/<int:pk>/delete',
         view=MacAddressDeleteView.as_view(),
         name='mac_address_delete'),
]
