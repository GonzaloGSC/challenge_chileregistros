# Generated by Django 4.1.7 on 2023-02-18 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='m_project',
            fields=[
                ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=500, null=True, unique=True)),
                ('detail', models.URLField(null=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('region', models.CharField(max_length=100, null=True)),
                ('typology', models.CharField(max_length=100, null=True)),
                ('headline', models.CharField(max_length=300, null=True)),
                ('investment', models.FloatField(null=True)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('map', models.URLField(null=True)),
            ],
        ),
    ]