from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin


# class Role(models.TextChoices):
#     USER = 'user', 'Ordinary user'
#     ADMIN = 'admin', 'Admin user'


# class CustomUser(AbstractUser):
#     MAX_USERNAME_LENGTH = 160
#     MAX_ROLE_LENGTH = 50

#     email = models.EmailField()
#     username = models.CharField(
#         null=True,
#         max_length=MAX_USERNAME_LENGTH,
#         unique=True,
#         blank=True,
#     )
#     role = models.CharField(
#         default=Role.USER,
#         max_length=MAX_ROLE_LENGTH,
#         auto_created=True,
#         choices=Role.choices,
#     )

#     # USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['username', ]

#     objects = UserManager()

#     @property
#     def is_admin(self):
#         return (
#             (self.role == Role.ADMIN) or
#             self.is_superuser
#         )

#     class Meta(AbstractUser.Meta):
#         managed = True

#     def __str__(self):
#         return self.email