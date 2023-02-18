from django.db import models


class m_project(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    number = models.IntegerField(null=False, unique=True)
    name = models.TextField(null=True, blank=False)
    detail = models.URLField(null=True)
    type = models.CharField(max_length=100, null=True, blank=False)
    region = models.CharField(max_length=100, null=True, blank=False)
    typology = models.CharField(max_length=100, null=True, blank=False)
    headline = models.CharField(max_length=300, null=True, blank=False)
    investment = models.FloatField(null=True)
    date = models.DateField(null=True, blank=False)
    status = models.CharField(max_length=100, null=True, blank=False)
    map = models.URLField(null=True)