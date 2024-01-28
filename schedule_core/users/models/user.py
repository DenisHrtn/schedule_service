from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.conf import settings

from users.managers.user import UserManager


class User(AbstractBaseUser):
    id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name="ID пользователя",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="email пользователя",
    )
    username = models.CharField(
        null=True,
        blank=True,
        max_length=25,
        verbose_name="Username пользователя",
    )
    code = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Код подтверждения пользователя",
    )
    code_created_at = models.DateTimeField(
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name="Дата создания кода подтверждения",
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата присоединения к сервису"
    )

    is_active = models.BooleanField(default=False, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Стафф")
    is_superuser = models.BooleanField(default=False, verbose_name="Супер-пользователь")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")
    is_verified = models.BooleanField(default=False, verbose_name="Верефицированный")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['password',]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def update_fields(self, **kwargs):
        for field, value in kwargs.items():
            if field == 'password':
                self.set_password(value)
            else:
                setattr(self, field, value)

        self.save()

    CONFIRMATION_CODE_TIME = settings.CONFIRMATION_TIME

    def validate_confirmation_code(self, code):
        """
        Method to validate confirmation code
        :param code:
        :return: None
        """
        expiry_time = timezone.make_aware(datetime.now() - timedelta(minutes=self.CONFIRMATION_CODE_TIME))
        if self.code_created_at < expiry_time:
            user = User.objects.get(code=self.code)
            if not user.is_active:
                user.delete()
        else:
            current_time = timezone.now()
            self.code_created_at = current_time
            self.save(update_fields=['code_created_at'])
            return True