import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from .models import Room, Device, DeviceSort
from .serializers import RoomSerializer, DeviceSerializer, DeviceSortSerializer, UserSerializer

User = get_user_model()

# For templates
def index(request):
    rooms = Room.objects.all()
    devices = Device.objects.all()
    device_sorts = DeviceSort.objects.order_by('rank')
    users = User.objects.all()

    # Filter for user-room combinations that have at least one DeviceSort
    valid_combinations = DeviceSort.objects.values('user', 'room').distinct()

    # Create a dictionary mapping users and rooms
    user_room_combinations = {}
    for combo in valid_combinations:
        user = User.objects.get(id=combo['user'])
        room = Room.objects.get(id=combo['room'])
        if user not in user_room_combinations:
            user_room_combinations[user] = []
        user_room_combinations[user].append(room)

    if request.method == 'POST':
        if 'room' in request.POST and 'user' in request.POST and 'device' in request.POST:
            room = Room.objects.get(id=request.POST['room'])
            user = User.objects.get(id=request.POST['user'])
            device = Device.objects.get(id=request.POST['device'])
            DeviceSort.objects.create(room=room, user=user, device=device)
            return redirect('index')

    return render(request, 'index.html', {
        'rooms': rooms,
        'devices': devices,
        'device_sorts': device_sorts,
        'users': users,
        'user_room_combinations': user_room_combinations,
    })


@csrf_exempt
def update_device_sort_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        current_id = data.get('current')
        previous_id = data.get('previous')
        next_id = data.get('next')

        try:
            current = DeviceSort.objects.get(id=current_id)
            # next = DeviceSort.objects.get(id=next_id, user_id=user_id, room_id=room_id) if next_id else None
            if not previous_id:
                current.place_on_top()
            elif not next_id:
                current.place_on_bottom()
            else:
                previous = DeviceSort.objects.get(id=previous_id) if previous_id else None
                current.place_after(previous)
            return JsonResponse({'message': 'Order updated successfully!'})
        except DeviceSort.DoesNotExist:
            return JsonResponse({'error': 'Invalid sort ID(s)'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# For APIs
class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('index')  # Redirect to the index page
        return response


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('index')  # Redirect to the index page
        return response


class DeviceSortViewSet(ModelViewSet):
    queryset = DeviceSort.objects.order_by('rank')
    serializer_class = DeviceSortSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('index')  # Redirect to the index page
        return response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('index')  # Redirect to the index page
        return response
