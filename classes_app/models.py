from django.db import models
from django.contrib.auth.models import User


class GymClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    class_date = models.DateField()
    class_time = models.TimeField()
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.class_date}"


class ClassRegistration(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.username} - {self.gym_class.title}"