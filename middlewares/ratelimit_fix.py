from django.utils.deprecation import MiddlewareMixin

"""
Este middleware se encarga de manejar la cabecera X-Forwarded-For, que es utilizada para especificar 
la dirección IP original del cliente cuando la solicitud ha pasado por un proxy o balanceador de carga.
(corrección de problema generado por guinicorn).
"""
class XForwardedForMiddleware(MiddlewareMixin):
    """
    Sets REMOTE_ADDR correctly to the client's ip, if django is run on a domain socket server.
    
    - ref 1: https://stackoverflow.com/a/34254843/1031191
    - ref 2: https://github.com/python-web-sig/wsgi-ng/issues/11
    """
    def process_request(self, request):
        if "HTTP_X_FORWARDED_FOR" in request.META:
            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(",", 1)
            request.META["REMOTE_ADDR"] = parts[0]