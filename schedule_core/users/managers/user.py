from django.contrib.auth.base_user import BaseUserManager
from django.db.transaction import atomic


class UserManager(BaseUserManager):
    def _create_user(
            self, email, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        if email:
            email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    @atomic
    def create_user(
            self, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_blocked", False)
        extra_fields.setdefault("is_verified", False)
        return self._create_user(
            email, password, **extra_fields
        )

    @atomic
    def create_superuser(
            self, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_blocked", False)
        extra_fields.setdefault("is_verified", True)
        return self._create_user(
            email, password, **extra_fields
        )