from rest_framework import serializers
from .models import (
    m_extra,
    m_payment,
    m_station,
)

class s_extra(serializers.ModelSerializer):
    class Meta:
        model = m_extra
        read_only_fields = ('id',)
        fields = (
            'id',
            'address',
            'altitude',
            'ebikes',
            'has_ebikes',
            'last_updated',
            'normal_bikes',
            'payment',
            'payment_terminal',
            'post_code',
            'renting',
            'returning',
            'slots',
            'api_id',
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
            'empty_slots',
            'extra',
            'free_bikes',
            'api_id',
            'latitude',
            'longitude',
            'name',
            'timestamp',
        )

