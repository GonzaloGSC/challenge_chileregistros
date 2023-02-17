from django.contrib import admin
from .models import (
    m_extra,
    m_payment,
    m_station,
    m_company,
    m_network,
)

admin.site.register(m_extra)
admin.site.register(m_payment)
admin.site.register(m_station)
admin.site.register(m_company)
admin.site.register(m_network)
