# Generated by Django 4.1.7 on 2023-02-17 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikesantiago', '0002_remove_m_extra_payment_m_extra_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='m_company',
            fields=[
                ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('company_code', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='m_extra',
            name='payment',
        ),
        migrations.AddField(
            model_name='m_extra',
            name='payments',
            field=models.ManyToManyField(default=None, null=True, related_name='extra_payments', to='bikesantiago.m_payment'),
        ),
        migrations.CreateModel(
            name='m_network',
            fields=[
                ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('gbfs_href', models.URLField(null=True)),
                ('href', models.CharField(max_length=500, null=True)),
                ('api_id', models.IntegerField(editable=False, unique=True)),
                ('location_city', models.CharField(max_length=300, null=True)),
                ('location_country', models.CharField(max_length=300, null=True)),
                ('location_latitude', models.FloatField(null=True)),
                ('location_longitude', models.FloatField(null=True)),
                ('name', models.CharField(max_length=300, null=True)),
                ('companys', models.ManyToManyField(default=None, null=True, related_name='network_companys', to='bikesantiago.m_company')),
                ('stations', models.ManyToManyField(default=None, null=True, related_name='network_stations', to='bikesantiago.m_station')),
            ],
        ),
    ]
