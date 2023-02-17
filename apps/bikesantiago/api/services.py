from django_ratelimit.decorators import ratelimit

import requests
from datetime import datetime
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from apps.log_sys.api.services import (
    create_logger, 
    manage_and_respond_exceptions
)
from ..models import (
    m_station,
    m_extra,
    m_payment,
    m_company,
    m_network,
)
from ..serializers import (
    s_station,
    s_extra,
    s_payment,
    s_company,
    s_network,
    s_get_all_data_from_networks,
)


LOGGER = create_logger("bikesantiago.log")


def get_model_company(code:str) -> (m_company | None):
    company_instance = m_company.objects.filter(company_code=code).first()
    return company_instance


def get_model_payment(code:str) -> (m_payment | None):
    payment_instance = m_payment.objects.filter(payment_code=code).first()
    return payment_instance


def get_model_network(api_id:int) -> (m_network | None):
    network_instance = m_network.objects.filter(api_id=api_id).first()
    return network_instance


def get_model_extra(api_uid:str) -> (m_extra | None):
    extra_instance = m_extra.objects.filter(api_uid=api_uid).first()
    return extra_instance


def get_model_station(api_id:str) -> (m_station | None):
    station_instance = m_station.objects.filter(api_id=api_id).first()
    return station_instance


@ratelimit(key='ip', rate='10/m')
def load_data_bikesantiago(request:Request) -> (Response):
    try:
        # Load the data from the API
        request_response = requests.get("http://api.citybik.es/v2/networks/bikesantiago")
        if request_response.status_code != 200:
            raise ValueError("Error de respuesta en API:" + str(request_response.status_code))
        request_data = request_response.json()
        network_data = {
            "companys": [],
            "stations": [],
            "gbfs_href": request_data["network"].get("gbfs_href", None),
            "href": request_data["network"].get("href", None),
            "api_id": request_data["network"]["id"],
            "location_city": request_data["network"]["location"].get("city", None) if request_data["network"].get("location", None) != None else None,
            "location_country": request_data["network"]["location"].get("country", None) if request_data["network"].get("location", None) != None else None,
            "location_latitude": request_data["network"]["location"].get("latitude", None) if request_data["network"].get("location", None) != None else None,
            "location_longitude": request_data["network"]["location"].get("longitude", None) if request_data["network"].get("location", None) != None else None,
            "name": request_data["network"]["name"] if request_data["network"].get("location", None) != None else None,
        }
        network_data_companys = []
        network_data_stations = []
        # companys save, create or update. Add id to "network_data_companys" array.
        for company_code in request_data["network"].get("company", []):
            company_instance = get_model_company(company_code)
            if company_instance == None:
                serializer = s_company(data={"company_code": company_code})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                network_data_companys.append(serializer.data["id"])
            else:
                network_data_companys.append(company_instance.id)
        # stations save, create or update. Add id to "network_data_stations" array.
        for station_data in request_data["network"].get("stations", []):
            # payments save, create or update. Add id to "network_data_payments" array.
            station_extra = None
            if station_data.get("extra", None) != None:
                network_data_payments = []
                for payment_code in station_data["extra"].get("payment", []):
                    payment_instance = get_model_payment(payment_code)
                    if payment_instance == None:
                        serializer = s_payment(data={"payment_code": payment_code})
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        network_data_payments.append(serializer.data["id"])
                    else:
                        network_data_payments.append(payment_instance.id)
                # extra data save, create or update.
                extra_data = {
                    "payments": network_data_payments,
                    "address": station_data["extra"].get("address", None),
                    "altitude": station_data["extra"].get("altitude", None),
                    "ebikes": station_data["extra"].get("ebikes", None),
                    "has_ebikes": station_data["extra"].get("has_ebikes", None),
                    "last_updated": datetime.fromtimestamp(float(station_data["extra"]["last_updated"])) if station_data["extra"].get("last_updated", None) != None else None, # transform date from fromtimestamp format to datetime
                    "normal_bikes": station_data["extra"].get("normal_bikes", None),
                    "payment_terminal": station_data["extra"].get("payment-terminal", None),
                    "post_code": station_data["extra"].get("post_code", None),
                    "renting": station_data["extra"].get("renting", None),
                    "returning": station_data["extra"].get("returning", None),
                    "slots": station_data["extra"].get("slots", None),
                    "api_uid": station_data["extra"].get("uid", None),
                }
                extra_instance = get_model_extra(extra_data["api_uid"])
                if extra_instance == None:
                    serializer = s_extra(data=extra_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                else:
                    serializer = s_extra(instance=extra_instance, data=extra_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                station_extra = serializer.data["id"]
            # station data save, create or update.
            station_new_data = {
                "extra": station_extra,
                "empty_slots": station_data.get("empty_slots", None),
                "free_bikes": station_data.get("free_bikes", None),
                "api_id": station_data["id"],
                "latitude": station_data.get("latitude", None),
                "longitude": station_data.get("longitude", None),
                "name": station_data.get("name", None),
                "timestamp": station_data.get("timestamp", None),
            }
            station_instance = get_model_station(station_new_data["api_id"])
            if station_instance == None:
                serializer = s_station(data=station_new_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = s_station(instance=station_instance, data=station_new_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            network_data_stations.append(serializer.data["id"])
        # network save, create or update
        network_data["companys"] = network_data_companys
        network_data["stations"] = network_data_stations
        network_instance = get_model_network(network_data["api_id"])
        if network_instance == None:
            serializer = s_network(data=network_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = s_network(instance=network_instance, data=network_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
