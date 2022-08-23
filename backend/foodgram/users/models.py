from asyncio import constants
from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class FoodgramUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text= 'Может начинаться с символов @.+- и содержать цифры и буквы',
        validators= [
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Недопустимые символы',
            ),
        ]
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
    
    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'following'],
                name = 'unique_follow'
            ),
        )
    
    def __str__(self):
        return f'{self.user_id} подписан на {self.author_id}' 
