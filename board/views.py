from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
import json
from .models import Task, Board

@csrf_exempt
def task_list(request):
    boards = Board.objects.prefetch_related("tasks").all()  # Load boards and tasks efficiently
    if request.method == "POST":
        # Create a new task
        task_name = request.POST.get("name")
        board_id = request.POST.get("board_id")
        if task_name and board_id:
            board = Board.objects.get(pk=board_id)
            Task.objects.create(name=task_name, board=board)
        return redirect("task_list")

    elif request.method == "PUT":
        # Handle reordering tasks
        data = json.loads(request.body)
        current_id = data.get("current_id")
        previous_id = data.get("previous_id")
        next_id = data.get("next_id")
        board_id = data.get("board_id")
        print(data)
        if not current_id or not board_id:
            return JsonResponse({"error": "Invalid data"}, status=400)

        current_task = Task.objects.get(pk=current_id, board_id=board_id)

        if not previous_id:
            # Move to the top
            try:
                current_task.place_on_top()
            except Exception:
                current_task.rebalance()
                current_task.place_on_top()
        elif not next_id:
            # Move to the bottom
            # previous_task = Task.objects.get(pk=previous_id, board_id=board_id)
            current_task.place_on_bottom()
        else:
            # Move between previous and next
            previous_task = Task.objects.get(pk=previous_id, board_id=board_id)
            current_task.place_after(previous_task)

        return JsonResponse({"status": "success"})

    return render(request, "task_list.html", {"boards": boards})


@csrf_exempt
def board_api(request):
    if request.method == "POST":
        # Create a new board
        print(request.POST)
        data = request.POST
        board_name = data.get("name")
        if board_name:
            Board.objects.create(name=board_name)
        return redirect("task_list")

    elif request.method == "GET":
        # List all boards
        boards = Board.objects.all().values("id", "name")
        return JsonResponse({"boards": list(boards)}, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)