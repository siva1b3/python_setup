from django.http import JsonResponse
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


def task_list(request):
    tasks = Task.objects.all()
    data = [
        {
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        }
        for task in tasks
    ]
    return JsonResponse(data, safe=False)


def task_detail(request, task_id):
    try:
        task = Task.objects.get(task_id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    data = {
        "task_id": task.task_id,
        "title": task.title,
        "done": task.done,
    }
    return JsonResponse(data)