from django.contrib import admin
from .models import Trainer, TrainerAssignment, TrainerHour

admin.site.register(Trainer)
admin.site.register(TrainerAssignment)
admin.site.register(TrainerHour)