import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from . import services as srv
from .schemas import Services

load_dotenv()

API_TOKEN = os.getenv('COMMON_TOKEN')
router = APIRouter()
api_key_header = APIKeyHeader(name='X-API-Key')


def verify_api_key(api_key: str = Depends(api_key_header)):
    """Проверка соответствия токена"""
    if api_key != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


@router.post(
        '/api/check-imei', dependencies=[Depends(verify_api_key)],
        response_model=Services
)
def check_imei(imei: str):
    """Проверка доступных услуг"""
    balance = srv.check_balance()
    services = srv.check_services(imei)
    return Services(services=services, balance=balance['balance'])


@router.post('/api/purchase', dependencies=[Depends(verify_api_key)])
def purchase_service(imei: str, service_id: int):
    """Получение услуги"""
    purchased = srv.get_service(imei, service_id)
    return purchased
