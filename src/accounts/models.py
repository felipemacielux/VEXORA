from django.contrib.auth.models import AbstractUser
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="accounts_user_set",  # ← Adicionar related_name único
        related_query_name="accounts_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="accounts_user_set",  # ← Adicionar related_name único
        related_query_name="accounts_user",
    )
    
    organizations = models.ManyToManyField(Organization, through='Membership')
    
    def __str__(self):
        return self.username

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, default="viewer")  # admin, editor, viewer

    class Meta:
        unique_together = ("user", "organization")
    
    def __str__(self):
        return f"{self.user} - {self.organization} - ({self.role})"