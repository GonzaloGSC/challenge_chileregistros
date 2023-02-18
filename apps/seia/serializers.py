from rest_framework import serializers

from .models import (
    m_project,
)

class s_project(serializers.ModelSerializer):
    class Meta:
        model = m_project
        read_only_fields = ('id',)
        fields = (
            'id',
            'number',
            'name',
            'detail',
            'type',
            'region',
            'typology',
            'headline',
            'investment',
            'date',
            'status',
            'map',
        )


class s_project_only_read(serializers.ModelSerializer):
    class Meta:
        model = m_project
        fields = (
            'id',
            'number',
            'name',
            'detail',
            'type',
            'region',
            'typology',
            'headline',
            'investment',
            'date',
            'status',
            'map',
        )
        read_only_fields = fields