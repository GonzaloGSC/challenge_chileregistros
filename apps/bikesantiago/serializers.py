from rest_framework import serializers
from .models import (
    m_extra,
    m_payment,
    m_station,
    m_company,
    m_network,
)

class s_extra(serializers.ModelSerializer):
    class Meta:
        model = m_extra
        read_only_fields = ('id',)
        fields = (
            'id',
            'payments',
            'address',
            'altitude',
            'ebikes',
            'has_ebikes',
            'last_updated',
            'normal_bikes',
            'payment_terminal',
            'post_code',
            'renting',
            'returning',
            'slots',
            'api_uid',
        )


class s_payment(serializers.ModelSerializer):
    class Meta:
        model = m_payment
        read_only_fields = ('id',)
        fields = (
            'id',
            'payment_code',
        )


class s_station(serializers.ModelSerializer):
    class Meta:
        model = m_station
        read_only_fields = ('id',)
        fields = (
            'id',
            'extra',
            'empty_slots',
            'free_bikes',
            'api_id',
            'latitude',
            'longitude',
            'name',
            'timestamp',
        )


class s_company(serializers.ModelSerializer):
    class Meta:
        model = m_company
        read_only_fields = ('id',)
        fields = (
            'id',
            'company_code',
        )


class s_network(serializers.ModelSerializer):
    class Meta:
        model = m_network
        read_only_fields = ('id',)
        fields = (
            'id',
            'companys',
            'stations',
            'gbfs_href',
            'href',
            'api_id',
            'location_city',
            'location_country',
            'location_latitude',
            'location_longitude',
            'name',
        )


class s_extra_all_data(serializers.ModelSerializer):
    payments = s_payment(many=True, read_only=True)
    class Meta:
        model = m_extra
        fields = (
            'id',
            'payments',
            'address',
            'altitude',
            'ebikes',
            'has_ebikes',
            'last_updated',
            'normal_bikes',
            'payment_terminal',
            'post_code',
            'renting',
            'returning',
            'slots',
            'api_uid',
        )
        read_only_fields = fields



class s_station_all_data(serializers.ModelSerializer):
    extra = s_extra_all_data(read_only=True)
    class Meta:
        model = m_station
        fields = (
            'id',
            'extra',
            'empty_slots',
            'free_bikes',
            'api_id',
            'latitude',
            'longitude',
            'name',
            'timestamp',
        )
        read_only_fields = fields



class s_get_all_data_from_networks(serializers.ModelSerializer):
    companys = s_company(many=True, read_only=True)
    stations = s_station_all_data(many=True, read_only=True)
    class Meta:
        model = m_network
        fields = (
            'id',
            'companys',
            'stations',
            'gbfs_href',
            'href',
            'api_id',
            'location_city',
            'location_country',
            'location_latitude',
            'location_longitude',
            'name',
        )
        read_only_fields = fields