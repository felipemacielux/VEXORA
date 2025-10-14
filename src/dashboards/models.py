from django.db import models


class Dashboard(models.Model):
    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Panel(models.Model):
    dashboard = models.ForeignKey('Dashboard', on_delete=models.CASCADE, related_name='panels')
    title = models.CharField(max_length=120)
    row = models.IntegerField()
    col = models.IntegerField()
    width = models.IntegerField(default=4)  # em colunas de 1 a 12
    height = models.IntegerField(default=6)  # em unidades de altura
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Query(models.Model):
    panel = models.ForeignKey('Panel', on_delete=models.CASCADE, related_name='queries')
    datasource = models.ForeignKey('datasources.DataSource', on_delete=models.CASCADE)
    text = models.TextField(help_text="Consulta SQL ou URL para HTTP")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query for {self.panel.title}"