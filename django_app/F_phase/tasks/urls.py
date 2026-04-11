from django.urls import path
from tasks.views import task_list, task_detail, task_create

urlpatterns = [
    path("", task_list),
    path("", task_create),
    path("<int:task_id>/", task_detail),
]