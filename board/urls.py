from django.urls import path
from board.views import task_list, board_api

urlpatterns = [
    path('', task_list, name='task_list'),
    path('board-api/', board_api, name='board_api')
]