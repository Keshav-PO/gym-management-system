from django.db import models
from classes_app.models import GymClass


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class TrainerAssignment(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainer.name} - {self.gym_class.title}"


class TrainerHour(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    work_date = models.DateField()

    def __str__(self):
        return f"{self.trainer.name} - {self.hours_worked} hours"