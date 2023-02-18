from django_filters.rest_framework import DjangoFilterBackend # imports de filtros para realizar busquedas.

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import OrderingFilter, SearchFilter # imports para ordenar la busqueda.
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from .services import (
    load_data_seia,
)
from ..models import (
    m_project,
)
from ..serializers import (
    s_project_only_read,
)


class v_seia_data(ListCreateAPIView): # Carga de datos, Listado para busquedas general
    permission_classes = (IsAuthenticated,)
    serializer_class = s_project_only_read
    queryset = m_project.objects.all()
    pagination_class = LimitOffsetPagination
    limit = 100
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, )
    data= (
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
    filter_fields = data # Campos por los que filtra los datos.
    ordering_fields = data  # Campos por los que ordena los datos.
    ordering = ('name',) # Prioridad de orden por defecto.
    search_fields = data # Busqueda general de toda la vida en los campos indicados.
    def post(self, request, *args, **kwargs):
        response = load_data_seia(request)
        renderers = self.get_renderers()
        media_type = self.request.accepted_media_type or self.renderer_classes[0].media_type
        context = self.get_renderer_context()
        context["response"] = response
        content = renderers[1].render(response.data, media_type, context)
        response.content = content
        return response