# Generated by Django 4.1.7 on 2023-02-17 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikesantiago', '0004_remove_m_extra_api_id_m_extra_api_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_network',
            name='api_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]