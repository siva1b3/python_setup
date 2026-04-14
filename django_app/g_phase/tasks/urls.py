from django.urls import path
from tasks.views import task_list, task_detail

urlpatterns = [
    path("", task_list),
    path("<int:task_id>/", task_detail),
]