from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import index, update_device_sort_order, RoomViewSet, DeviceViewSet, DeviceSortViewSet, UserViewSet

# API Router
router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'device-sorts', DeviceSortViewSet, basename='device_sort')
router.register(r'users', UserViewSet, basename='user')

# URLs
urlpatterns = [
    path('', index, name='index'),
    path('update-device-sort-order/', update_device_sort_order, name='update_device_sort_order'),
    path('api/', include(router.urls)),
    path('add-room/', RoomViewSet.as_view({'post': 'create'}), name='add_room'),
    path('add-user/', UserViewSet.as_view({'post': 'create'}), name='add_user'),
    path('add-device/', DeviceViewSet.as_view({'post': 'create'}), name='add_device'),
    path('add-device-sort/', DeviceSortViewSet.as_view({'post': 'create'}), name='add_device_sort'),
]