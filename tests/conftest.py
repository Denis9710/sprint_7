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
        assert create_response.status_code == 201, f"Failed to create courier: {create_response.status_code}"
    
    with allure.step('Авторизация курьера для получения id'):
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        assert login_response.status_code == 200, f"Failed to login courier: {login_response.status_code}"
        courier_id = login_response.json().get("id")
    
    result = {
        'data': courier_data,
        'id': courier_id
    }
    
    yield result
    
    with allure.step('Удаление тестового курьера'):
        requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")

@pytest.fixture
def clean_courier():
    """Фикстура для очистки данных курьера"""
    def _clean_courier(courier_data):
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        assert login_response.status_code == 200, "Failed to login for cleanup"
        courier_id = login_response.json()["id"]
        requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
    
    return _clean_courier

@pytest.fixture
def clean_order():
    """Фикстура для отмены заказа"""
    def _clean_order(track_id):
        requests.put(f"{Urls.URL_orders_cancel}?track={track_id}")
    
    return _clean_order

@pytest.fixture
def new_order(clean_order):
    """Универсальная фикстура для создания заказа"""
    order_payload = json.dumps(TestOrderData.order_data_grey)
    headers = {'Content-Type': 'application/json'}
    
    with allure.step('Создание заказа'):
        create_response = requests.post(Urls.URL_orders_create, data=order_payload, headers=headers)
        assert create_response.status_code == 201, f"Failed to create order: {create_response.status_code}"
        track_id = create_response.json().get("track")
    
    with allure.step('Получение id заказа по track номеру'):
        get_response = requests.get(f"{Urls.URL_orders_get}?t={track_id}")
        assert get_response.status_code == 200, f"Failed to get order: {get_response.status_code}"
        order_id = get_response.json().get('order', {}).get('id')
    
    result = {
        'track_id': track_id,
        'order_id': order_id
    }
    
    yield result
    
    with allure.step('Отмена тестового заказа'):
        clean_order(track_id)

@pytest.fixture
def courier_and_order(new_courier, new_order):
    """Универсальная фикстура для создания курьера и заказа"""
    result = {
        'courier': new_courier,
        'order': new_order
    }
    
    yield result

@pytest.fixture(params=[
    TestOrderData.order_data_grey,
    TestOrderData.order_data_black, 
    TestOrderData.order_data_two_colors,
    TestOrderData.order_data_no_colors
])
def order_data(request, clean_order):
    """Фикстура для параметризации данных заказа"""
    order_payload = json.dumps(request.param)
    headers = {'Content-Type': 'application/json'}
    
    with allure.step('Создание заказа для параметризованного теста'):
        create_response = requests.post(Urls.URL_orders_create, data=order_payload, headers=headers)
        assert create_response.status_code == 201, f"Failed to create parameterized order: {create_response.status_code}"
        track_id = create_response.json().get("track")
    
    result = {
        'track_id': track_id,
        'data': request.param
    }
    
    yield result
    
    with allure.step('Отмена параметризованного заказа'):
        clean_order(track_id)

        