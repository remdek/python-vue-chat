from django.db import models
from users.models import User
from lessons.models import Lesson


class Msg(models.Model):
    text = models.CharField("Сообщение", max_length=250)
    lesson = models.ForeignKey(Lesson, verbose_name="Предмет",
                                on_delete=models.CASCADE, related_name='%(class)s_lesson')
    user = models.ForeignKey(User, verbose_name="Владелец",
                               on_delete=models.CASCADE, related_name='%(class)s_user')
    created = models.DateTimeField("Создана", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField("Обновлена", auto_now_add=False, auto_now=True, db_index=True)