from django.db import models


class m_payment(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    payment_code = models.CharField(max_length=100, null=False, blank=False, unique=True)
    def __str__(self) -> str:
        return self.payment_code


class m_extra(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    payments = models.ManyToManyField(m_payment, default=[], related_name="extra_payments")
    address = models.CharField(max_length=500, null=True, blank=False)
    altitude = models.FloatField(null=True)
    ebikes = models.IntegerField(null=True)
    has_ebikes = models.BooleanField(null=False)
    last_updated = models.DateTimeField(null=True, blank=False, default=None)
    normal_bikes = models.IntegerField(null=True)
    payment_terminal = models.BooleanField(null=False)
    post_code = models.CharField(max_length=300, null=True, blank=False)
    renting = models.IntegerField(null=True)
    returning = models.IntegerField(null=True)
    slots = models.IntegerField(null=True)
    api_uid = models.CharField(max_length=300, null=False, blank=False, unique=True)
    def __str__(self) -> str:
        return self.api_uid

class m_station(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    extra = models.ForeignKey(m_extra, on_delete=models.SET_NULL, null=True, default=None, related_name="station_extra")
    empty_slots = models.IntegerField(null=True)
    free_bikes = models.IntegerField(null=True)
    api_id = models.CharField(max_length=300, null=False, blank=False, unique=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    name = models.CharField(max_length=300, null=True, blank=False)
    timestamp = models.CharField(max_length=300, null=True, blank=False)
    def __str__(self) -> str:
        return self.name

class m_company(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    company_code = models.CharField(max_length=100, null=False, blank=False, unique=True)
    def __str__(self) -> str:
        return self.company_code

class m_network(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    companys = models.ManyToManyField(m_company, default=[], related_name="network_companys")
    stations = models.ManyToManyField(m_station, default=[], related_name="network_stations")
    gbfs_href = models.URLField(null=True, blank=False)
    href = models.CharField(max_length=500, null=True, blank=False)
    api_id = models.CharField(max_length=300, null=False, blank=False, unique=True)
    location_city = models.CharField(max_length=300, null=True, blank=False)
    location_country = models.CharField(max_length=300, null=True, blank=False)
    location_latitude = models.FloatField(null=True)
    location_longitude = models.FloatField(null=True)
    name = models.CharField(max_length=300, null=True, blank=False)
    def __str__(self) -> str:
        return self.name