from django.db import models

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    class Meta:
        db_table = "tasks"

    def __str__(self):
        return self.title