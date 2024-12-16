import uuid
from django_lexorank.models import RankedModel
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

def default_room_name():
    return "Room " + uuid.uuid4().hex

def default_device_name():
    return "Device " + uuid.uuid4().hex

def default_sort_name():
    return "Sorting " + uuid.uuid4().hex


class Room(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, default=default_room_name)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Device(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, default=default_device_name)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DeviceSort(RankedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    order_with_respect_to = ["user", "room"]

    def __str__(self):
        return f"{self.device.name} ({self.rank}"

# class Role(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey("content_type", "object_id")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


# class SortTree(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     sort_key = models.UUIDField(default=uuid.uuid4, db_index=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=255, null=True, blank=True, default=default_sort_name)
