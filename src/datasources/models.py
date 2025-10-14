from django.db import models


class DataSource(models.Model):
    TYPE_CHOICES = [
        ("postgres", "PostgreSQL"),
        ("http", "HTTP API"),
        ("mock", "Mock"),
    ]
    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    # Para Postgres
    host = models.CharField(max_length=200, blank=True)
    port = models.IntegerField(default=5432)
    database = models.CharField(max_length=120, blank=True)
    username = models.CharField(max_length=120, blank=True)
    password = models.CharField(max_length=120, blank=True)
    # Para HTTP
    base_url = models.URLField(blank=True)
    auth_token = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("organization", "name")
    
    def __str__(self):
        return self.name
