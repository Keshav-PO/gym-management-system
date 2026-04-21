from django.db import models
from django.contrib.auth.models import User


class MemberProfile(models.Model):
    FITNESS_GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('general_fitness', 'General Fitness'),
        ('strength_training', 'Strength Training'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('body_toning', 'Body Toning'),
    ]

    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fitness_goal = models.CharField(
        max_length=50,
        choices=FITNESS_GOAL_CHOICES
    )

    experience_level = models.CharField(
        max_length=50,
        choices=EXPERIENCE_CHOICES
    )

    def __str__(self):
        return self.user.username