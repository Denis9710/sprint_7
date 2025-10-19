import requests
import allure
import pytest
import json
from data import TestOrderData
from urls import Urls
import helpers as h


class TestOrderAccept:

    @allure.title('Проверка успешного принятия заказа курьером')
    def test_order_accept_success(self, courier_and_order):
        courier_id = courier_and_order['courier']['id']
        order_id = courier_and_order['order']['order_id']
        
        with allure.step('Принятие заказа курьером'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{order_id}?courierId={courier_id}")
        
        # Проверка успешного принятия заказа (код 200 и тело ответа {"ok": true})
        assert accept_response.status_code == 200
        assert accept_response.json() == {"ok": True}

    @allure.title('Проверка ошибки при принятии заказа без id курьера')
    def test_order_accept_error_without_courier_id(self, new_order):
        if not new_order.get('order_id'):
            pytest.skip("Order not created")
            
        with allure.step('Попытка принять заказ без указания id курьера'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{new_order['order_id']}")
        
        # Проверка ошибки (код 400 и сообщение)
        assert accept_response.status_code == 400
        response_data = accept_response.json()
        assert "message" in response_data
        # Проверяем конкретное сообщение, если известно ожидаемое значение
        expected_message = "Недостаточно данных для поиска"
        assert response_data["message"] == expected_message

    @allure.title('Проверка ошибки при принятии заказа с неверным id курьера')
    def test_order_accept_error_with_wrong_courier_id(self, new_order):
        if not new_order.get('order_id'):
            pytest.skip("Order not created")
            
        # Использование несуществующего id курьера
        wrong_courier_id = "999999999"
        
        with allure.step('Попытка принять заказ с несуществующим id курьера'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{new_order['order_id']}?courierId={wrong_courier_id}")
        
        # Проверка ошибки "курьер не найден" (код 404 и сообщение)
        assert accept_response.status_code == 404
        response_data = accept_response.json()
        assert "message" in response_data
        expected_message = "Курьера с таким id не существует"
        assert response_data["message"] == expected_message

    @allure.title('Проверка ошибки при принятии заказа без id заказа')
    def test_order_accept_error_without_order_id(self, new_courier):
        if not new_courier.get('id'):
            pytest.skip("Courier not created")
            
        with allure.step('Попытка принять заказ без указания id заказа'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/?courierId={new_courier['id']}")
        
        # Проверка ошибки (код 404 и сообщение)
        assert accept_response.status_code == 404
        if accept_response.text:  # если есть тело ответа
            response_data = accept_response.json()
            assert "message" in response_data

    @allure.title('Проверка ошибки при принятии заказа с неверным id заказа')
    def test_order_accept_error_with_wrong_order_id(self, new_courier):
        if not new_courier.get('id'):
            pytest.skip("Courier not created")
            
        # Использование несуществующего id заказа
        wrong_order_id = "888888888"
        
        with allure.step('Попытка принять заказ с несуществующим id заказа'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{wrong_order_id}?courierId={new_courier['id']}")
        
        # Проверка ошибки "заказ не найден" (код 404 и сообщение)
        assert accept_response.status_code == 404
        response_data = accept_response.json()
        assert "message" in response_data
        expected_message = "Заказа с таким id не существует"
        assert response_data["message"] == expected_message