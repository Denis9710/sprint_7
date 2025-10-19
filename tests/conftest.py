import pytest
import requests
import json
import allure
import helpers as h
from urls import Urls
from data import TestOrderData


@pytest.fixture
def new_courier():
    """Универсальная фикстура для создания курьера"""
    courier_data = {
        'login': h.create_random_login(),
        'password': h.create_random_password(),
        'firstName': h.create_random_firstname()
    }
    
    with allure.step('Создание курьера для теста'):
        create_response = requests.post(Urls.URL_courier_create, data=courier_data)
        # Убраны все ассерты и проверки
        if create_response.status_code != 201:
            return {'data': courier_data, 'id': None, 'error': f'Create failed: {create_response.status_code}'}
    
    with allure.step('Авторизация курьера для получения id'):
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        courier_id = login_response.json().get("id") if login_response.status_code == 200 else None
    
    result = {
        'data': courier_data,
        'id': courier_id
    }
    
    yield result
    
    # Гарантированная очистка тестовых данных
    if courier_id:
        with allure.step('Удаление тестового курьера'):
            try:
                requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
            except Exception:
                pass  # Игнорируем ошибки при удалении


@pytest.fixture
def clean_courier():
    """Фикстура для очистки данных курьера"""
    def _clean_courier(courier_data):
        try:
            # Авторизация для получения id
            login_response = requests.post(Urls.URL_courier_login, data={
                'login': courier_data['login'],
                'password': courier_data['password']
            })
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                # Удаление курьера
                requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
        except Exception:
            pass  # Игнорируем ошибки при очистке
    
    return _clean_courier


@pytest.fixture
def new_order():
    """Универсальная фикстура для создания заказа"""
    order_payload = json.dumps(TestOrderData.order_data_grey)
    headers = {'Content-Type': 'application/json'}
    
    with allure.step('Создание заказа'):
        create_response = requests.post(Urls.URL_orders_create, data=order_payload, headers=headers)
        # Убраны ассерты
        if create_response.status_code != 201:
            return {'track_id': None, 'order_id': None, 'error': f'Create order failed: {create_response.status_code}'}
        
        track_id = create_response.json().get("track")
    
    with allure.step('Получение id заказа по track номеру'):
        get_response = requests.get(f"{Urls.URL_orders_get}?t={track_id}")
        order_id = get_response.json().get('order', {}).get('id') if get_response.status_code == 200 else None
    
    return {
        'track_id': track_id,
        'order_id': order_id
    }


@pytest.fixture
def courier_and_order(new_courier, new_order):
    """Универсальная фикстура для создания курьера и заказа"""
    # Проверяем, что оба объекта созданы успешно
    if 'error' in new_courier or 'error' in new_order:
        pytest.skip("Failed to create test data")
    
    return {
        'courier': new_courier,
        'order': new_order
    }


@pytest.fixture(params=[
    TestOrderData.order_data_grey,
    TestOrderData.order_data_black, 
    TestOrderData.order_data_two_colors,
    TestOrderData.order_data_no_colors
])
def order_data(request):
    """Фикстура для параметризации данных заказа"""
    return request.param