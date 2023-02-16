from django.db import models


class m_payment(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    payment_code = models.CharField(max_length=100, null=False, blank=False, unique=True)


class m_extra(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    address = models.CharField(max_length=500, null=True, blank=False)
    altitude = models.FloatField(null=True)
    ebikes = models.IntegerField(null=True)
    has_ebikes = models.BooleanField(null=False)
    last_updated = models.DateTimeField(null=True, blank=False, default=None)
    normal_bikes = models.IntegerField(null=True)
    payment = models.ForeignKey(m_payment, on_delete=models.SET_NULL, null=True, default=None, related_name="extra_payment")
    payment_terminal = models.BooleanField(null=False)
    post_code = models.CharField(max_length=300, null=True, blank=False)
    renting = models.IntegerField(null=True)
    returning = models.IntegerField(null=True)
    slots = models.IntegerField(null=True)
    api_id = models.IntegerField(null=False, unique=True, editable=False)


class m_station(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    empty_slots = models.IntegerField(null=True)
    extra = models.ForeignKey(m_extra, on_delete=models.SET_NULL, null=True, default=None, related_name="station_extra")
    free_bikes = models.IntegerField(null=True)
    api_id = models.CharField(max_length=300, null=False, blank=False, unique=True, editable=False)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    name = models.CharField(max_length=300, null=True, blank=False)
    timestamp = models.CharField(max_length=300, null=True, blank=False)

