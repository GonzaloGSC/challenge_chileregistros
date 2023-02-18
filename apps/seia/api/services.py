from django_ratelimit.decorators import ratelimit
from django.db.utils import IntegrityError

from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from datetime import datetime
from joblib import Parallel, delayed
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from apps.log_sys.api.services import (
    create_logger, 
    manage_and_respond_exceptions
)

from ..models import (
    m_project,
)
from ..serializers import (
    s_project,
)


LOGGER = create_logger("seia.log")


def get_model_project(number:int) -> (m_project | None):
    instance = m_project.objects.filter(number=number).first()
    return instance


def get_page_response(url:str) -> (Response):
    attempts = 10
    ready = False
    while(not ready):
        try:
            response = requests.get(url, headers={'User-Agent': 'Chrome'}, timeout=300)
            ready = True
        except Exception as err:
            if ((err.__class__ == ConnectionError or err.__class__ == ConnectTimeout) and attempts > 0):
                attempts = attempts - 1
            else:
                raise err
    if response.status_code != 200:
        raise ValueError("Error en carga de sitio objetivo, por favor reintentar.")
    return response


def is_float(num:str):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_int(num:str):
    try:
        int(num)
        return True
    except ValueError:
        return False


@ratelimit(key='ip', rate='10/m')
def load_data_seia(request:Request) -> (Response):
    try:
        url = "https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php"
        response = get_page_response(url)
        webpage = response.content.strip()
        soup = BeautifulSoup(webpage, "html.parser")
        page_select = soup.find("select", attrs={"name": "pagina_offset"})
        select_options = page_select.find_all("option")
        n_jobs = 30
        with Parallel(n_jobs=n_jobs, prefer="threads", timeout=90000) as parallel:
            parallel(
                delayed(parallel_data_seia)(page) for page in range(1, len(select_options)+1)
            )
        # Response part
        response_data = {
            'success': True,
            'error': False,
            'status_code': status.HTTP_200_OK,
            'message': "Datos cargados con éxito.",
            'data': {}
        }
        return Response(response_data, status=response_data["status_code"],  content_type="application/json")
    except Exception as err:
        return manage_and_respond_exceptions(err, LOGGER)


def parallel_data_seia(page: int) -> (None):
    final_array = []
    print("page:", page)
    url = "https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php?_paginador_fila_actual="
    url = url + str(page)
    response = get_page_response(url)
    webpage = response.content.strip() 
    soup = BeautifulSoup(webpage, "html.parser")
    table = soup.find("table", attrs={"class": "tabla_datos", "summary": "datos"})
    rows_array = table.find_all("tr")
    for row in rows_array:
        count = 0
        row_data = {
            "number": None,
            "name": None,
            "detail": None,
            "type": None,
            "region": None,
            "typology": None,
            "headline": None,
            "investment": None,
            "date": None,
            "status": None,
            "map": None,
        }
        for columna in row.find_all("td"):
            if count == 0:
                row_data["number"] = int(columna.text) if is_int(columna.text) else None
            if count == 1:
                # 
                row_data["name"] = columna.text.replace("\n", "").replace("\t", "") if columna.text != "" and columna.text != None else None
                if row_data["name"][-1] == " ":
                    row_data["name"] = row_data["name"][:-1]
                row_data["detail"] = columna.a['href'] if columna.a != None else None
            if count == 2:
                row_data["type"] = columna.text if columna.text != "" and columna.text != None else None
            if count == 3:
                row_data["region"] = columna.text if columna.text != "" and columna.text != None else None
            if count == 4:
                row_data["typology"] = columna.text if columna.text != "" and columna.text != None else None
            if count == 5:
                row_data['headline'] = columna.text if columna.text != "" and columna.text != None else None
            if count == 6:
                row_data["investment"] = float(columna.text.replace(",", ".")) if is_float(columna.text.replace(",", ".")) else None
            if count == 7:
                row_data["date"] = columna.text.replace("/", "-") if columna.text != "" and columna.text != None else None
            if count == 8:
                row_data["status"] = columna.text if columna.text != "" and columna.text != None else None
            if count == 9:
                if columna != "" and columna != None:
                    row_data["status"] = columna.a["href"] if columna.a != None else None
                final_array.append(row_data.copy())
            if count >= 10:
                break
            count = count + 1
    for data in final_array:
        project_instance = get_model_project(data["number"])
        if project_instance == None:
            try:
                serializer = s_project(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as err:
                manage_parallel_error(err, serializer.data)
        else:
            try:
                serializer = s_project(instance=project_instance, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as err:
                manage_parallel_error(err, serializer.data)


def manage_parallel_error(err:Exception, data:dict) -> (None):
    exists = False
    if err.__class__ == ValidationError:
        print("Error al validar...")
        for error in err.args:
            if error.get("name") != None:
                for detail in error["name"]:
                    print("detail:", detail)
                    if detail.__dict__["code"] == "unique":
                        exists = True
    if err.__class__ == IntegrityError:
        print("Error de integridad...")
        for error in err.args:
            if error.__class__ == str:
                if "id" in error:
                    exists = True
    if exists:
        print("Objeto ya existe, buscando...")
        instance = m_project.objects.filter(number=data["number"]).first()
        if instance != None:
            serializer = s_project(instance=instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise err
    else:
        raise err
