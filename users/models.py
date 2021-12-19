from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from lessons.models import Lesson

USER_TYPE = [
    ('user', 'Пользователь'),
    ('tutor', 'Преподаватель'),
    ('manager', 'Менеджер')
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, block=False):
        if not email:
            raise ValueError("Email required")
        if not password:
            raise ValueError("Password required")
        # if not first_name:
        #     raise ValueError("Укажите ваше имя")

        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.block = block
        user_obj.save(using=self._db)
        return user_obj
    #
    # def create_staffuser(self, email, password=None):
    #     return self.create_user(email, password=password)
    #
    # def create_superuser(self, email, password=None):
    #     return self.create_user(email, password=password)


class User(models.Model):
    email = models.EmailField("Email", unique=True, blank=True, null=True, default=None)
    password = models.CharField('Password', max_length=128, blank=True)

    f_name = models.CharField("First name", max_length=50)
    l_name = models.CharField("Last Name", max_length=50, blank=True)

    type = models.CharField("Тип пользователя", max_length=14, choices=USER_TYPE, default="user", db_index=True)
    access = models.ManyToManyField(Lesson, related_name="%(class)s_access", verbose_name="Доступ к урокам")

    created = models.DateTimeField("Создана", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField("Обновлена", auto_now_add=False, auto_now=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
