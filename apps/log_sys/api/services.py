from django.http import HttpResponse

import json, platform, logging
from functools import wraps
from xmlrpc.client import Boolean
from backend.settings import BASE_DIR

from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def create_logger(file_name:str = "logs.log", level: int | str = 40) -> (logging.Logger):
    """
    Create a logger with a name and level.\n
    Logger lavel can be:
        logging.CRITICAL: 50
        logging.FATAL: "CRITICAL"
        logging.ERROR: 40
        logging.WARNING: 30
        logging.WARN: "WARNING"
        logging.INFO: 20
        logging.DEBUG: 10
        logging.NOTSET: 0
    """
    # create a logger object
    logger = logging.getLogger(file_name)
    logger.setLevel(level)
    # create a file to store all the logged exceptions
    slicer = "\\"
    if not platform.system() == "Windows":
        slicer = "/"
    logfile = logging.FileHandler("apps" + slicer + "log_sys" + slicer + "logs" + slicer + file_name)
    fmt = '************************************************************************\n%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)
    return logger

# @exception_decorator(LOGGER) // Function that is used as a decorator to return exceptions without try: except:
def exception_decorator(logger: logging.Logger):
    def decorator(func):
        @wraps(func)
        def wrapper (*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                issue = "exception in"+func.__name__+"\n"
                issue = issue+"===================\n"
                logger.error(issue)
                raise
        return wrapper
    return decorator

def manage_and_respond_exceptions(excep: Exception, logger_var: logging.Logger, http_response: Boolean = False, send_mail: Boolean = False) -> (Response | HttpResponse):
    """
    Función encargada de manejar la mayor parte de las excepciones producidas en el proyecto, 
    su versatilidad es muy amplia, ya que está enfocada en hacer un uso automático de las 
    excepciones de validación de django y serializers. Además, retorna un objeto Response con 
    status_code según corresponda, esto es, errores 400 o 500 u otros. Puede adaptarse fácilmente 
    para envió de errores por email en tiempo real.
    """
    text: str = 'Processing error. If the problem persists, contact an administrator.'
    error: Boolean = True
    status_var: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    if excep.__class__ == ValidationError:
        error = False
        status_var = status.HTTP_400_BAD_REQUEST
        response = exception_handler(excep, "Validation error")
        text = ""
        for key in response.data:
            text = text + key +": "+ response.data[key][0] + "\n"
    elif excep.__class__ == ValueError:
        error = False
        status_var = status.HTTP_400_BAD_REQUEST
        text = str(excep)
    else:
        logger_var.exception(excep)
    print(text)
    slicer = "\\"
    if not platform.system() == "Windows":
        slicer = "/"
    if status_var in range(500, 600): # Send mail when is an internal error (deactivated)
        file_path = str(BASE_DIR) + slicer + "apps" + slicer + "log_sys" + slicer + "logs" + slicer + logger_var.name
        with open(file_path) as file:
            lines = file.readlines()
            lines_error: list[str] = []
            for index, element in reversed(list(enumerate(lines))):
                if element == '************************************************************************\n':
                    lines_error = lines[index + 1:len(lines)]
                    break
            # send_error_mail(lines_error, file_path)
            file.close()
    data = {
        'success': False,
        'error': error,
        'status_code': status_var,
        'message': text,
        'data':{}
    }
    if http_response:
        return HttpResponse(json.dumps(data), status = data['status_code'],  content_type="application/json")
    else:
        return Response(data, status = data['status_code'],  content_type="application/json")


