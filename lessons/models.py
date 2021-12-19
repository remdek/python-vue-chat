from django.db import models

# Create your models here.

class Lesson(models.Model):
    name = models.CharField("Наименование урока", max_length=255)

