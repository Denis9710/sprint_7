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
        # Убраны ассерты из фикстуры
        if create_response.status_code != 201:
            pytest.fail(f"Failed to create courier: {create_response.status_code}")
    
    with allure.step('Авторизация курьера для получения id'):
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        if login_response.status_code != 200:
            pytest.fail(f"Failed to login courier: {login_response.status_code}")
        courier_id = login_response.json()["id"]
    
    yield {
        'data': courier_data,
        'id': courier_id
    }
    
    # Очистка тестовых данных после выполнения теста
    with allure.step('Удаление тестового курьера'):
        delete_response = requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
        # Можно добавить логирование результата удаления при необходимости


@pytest.fixture
def clean_courier():
    """Фикстура для очистки данных курьера"""
    def _clean_courier(courier_data):
        # Авторизация для получения id
        login_response = requests.post(Urls.URL_courier_login, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            # Удаление курьера
            requests.delete(f"{Urls.URL_courier_delete}/{courier_id}")
    
    return _clean_courier


@pytest.fixture
def new_order():
    """Универсальная фикстура для создания заказа"""
    order_payload = json.dumps(TestOrderData.order_data_grey)
    headers = {'Content-Type': 'application/json'}
    
    with allure.step('Создание заказа'):
        create_response = requests.post(Urls.URL_orders_create, data=order_payload, headers=headers)
        # Убраны ассерты из фикстуры
        if create_response.status_code != 201:
            pytest.fail(f"Failed to create order: {create_response.status_code}")
        track_id = create_response.json()["track"]
    
    with allure.step('Получение id заказа по track номеру'):
        get_response = requests.get(f"{Urls.URL_orders_get}?t={track_id}")
        if get_response.status_code != 200:
            pytest.fail(f"Failed to get order by track: {get_response.status_code}")
        order_id = get_response.json()['order']['id']
    
    return {
        'track_id': track_id,
        'order_id': order_id
    }


@pytest.fixture
def courier_and_order(new_courier, new_order):
    """Универсальная фикстура для создания курьера и заказа"""
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