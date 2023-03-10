# Generated by Django 4.1.7 on 2023-02-16 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='m_extra',
            fields=[
                ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=500, null=True)),
                ('altitude', models.FloatField(null=True)),
                ('ebikes', models.IntegerField(null=True)),
                ('has_ebikes', models.BooleanField()),
                ('last_updated', models.DateTimeField(default=None, null=True)),
                ('normal_bikes', models.IntegerField(null=True)),
                ('payment_terminal', models.BooleanField()),
                ('post_code', models.CharField(max_length=300, null=True)),
                ('renting', models.IntegerField(null=True)),
                ('returning', models.IntegerField(null=True)),
                ('slots', models.IntegerField(null=True)),
                ('api_id', models.IntegerField(editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='m_payment',
            fields=[
                ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('payment_code', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='m_station',
            fields=[
                ('id', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('empty_slots', models.IntegerField(null=True)),
                ('free_bikes', models.IntegerField(null=True)),
                ('api_id', models.CharField(editable=False, max_length=300, unique=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('name', models.CharField(max_length=300, null=True)),
                ('timestamp', models.CharField(max_length=300, null=True)),
                ('extra', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station_extra', to='bikesantiago.m_extra')),
            ],
        ),
        migrations.AddField(
            model_name='m_extra',
            name='payment',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra_payment', to='bikesantiago.m_payment'),
        ),
    ]
