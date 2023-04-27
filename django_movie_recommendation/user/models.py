from common.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCustom(AbstractUser, BaseModel):
    email = models.EmailField(
        unique=True,
    )

    def __str__(self):
        return f'{self.pk} - {self.username}:{self.email}'
