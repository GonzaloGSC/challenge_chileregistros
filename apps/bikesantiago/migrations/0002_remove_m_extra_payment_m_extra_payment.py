# Generated by Django 4.1.7 on 2023-02-17 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikesantiago', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='m_extra',
            name='payment',
        ),
        migrations.AddField(
            model_name='m_extra',
            name='payment',
            field=models.ManyToManyField(default=None, null=True, related_name='extra_payment', to='bikesantiago.m_payment'),
        ),
    ]
