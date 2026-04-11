import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def task_list(request):
    if request.method == "GET":
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

    if request.method == "POST":
        body = json.loads(request.body)
        task = Task.objects.create(
            title=body["title"],
            done=body.get("done", False),
        )
        return JsonResponse(
            {"task_id": task.task_id, "title": task.title, "done": task.done},
            status=201,
        )


@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(task_id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    if request.method == "PUT":
        body = json.loads(request.body)
        task.title = body.get("title", task.title)
        task.done = body.get("done", task.done)
        task.save()
        return JsonResponse({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({}, status=204)
    

@csrf_exempt
def task_create(request):
    body = json.loads(request.body)
    task = Task.objects.create(
        title=body["title"],
        done=body.get("done", False),
    )
    data = {
        "task_id": task.task_id,
        "title": task.title,
        "done": task.done,
    }
    return JsonResponse(data, status=201)