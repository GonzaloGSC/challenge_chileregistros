from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .services import (
    load_data_bikesantiago,
)

class v_load_data_bikesantiago(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwards):
        return load_data_bikesantiago(request)