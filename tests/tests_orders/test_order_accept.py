import requests
import allure
import pytest
from urls import Urls

class TestOrderAccept:

    @allure.title('Проверка успешного принятия заказа курьером')
    def test_order_accept_success(self, courier_and_order, clean_courier):
        courier_id = courier_and_order['courier']['id']
        order_id = courier_and_order['order']['order_id']
        
        with allure.step('Принятие заказа курьером'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{order_id}?courierId={courier_id}")
        
        # Проверка успешного принятия заказа
        assert accept_response.status_code == 200
        response_data = accept_response.json()
        # ДОБАВЛЕНО: проверка текста ответа
        assert response_data == {"ok": True}
        assert "ok" in response_data
        assert response_data["ok"] == True
        
        clean_courier(courier_and_order['courier']['data'])

    @allure.title('Проверка ошибки при принятии заказа без id курьера')
    def test_order_accept_error_without_courier_id(self, new_order):
        if not new_order.get('order_id'):
            pytest.skip("Order not created")
            
        with allure.step('Попытка принять заказ без указания id курьера'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{new_order['order_id']}")
        
        # Проверка ошибки
        assert accept_response.status_code == 400
        response_data = accept_response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        expected_message = "Недостаточно данных для поиска"
        assert response_data["message"] == expected_message

    @allure.title('Проверка ошибки при принятии заказа с неверным id курьера')
    def test_order_accept_error_with_wrong_courier_id(self, new_order):
        if not new_order.get('order_id'):
            pytest.skip("Order not created")
            
        wrong_courier_id = "999999999"
        
        with allure.step('Попытка принять заказ с несуществующим id курьера'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{new_order['order_id']}?courierId={wrong_courier_id}")
        
        # Проверка ошибки "курьер не найден"
        assert accept_response.status_code == 404
        response_data = accept_response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        expected_message = "Курьера с таким id не существует"
        assert response_data["message"] == expected_message

    @allure.title('Проверка ошибки при принятии заказа без id заказа')
    def test_order_accept_error_without_order_id(self, new_courier, clean_courier):
        if not new_courier.get('id'):
            pytest.skip("Courier not created")
            
        with allure.step('Попытка принять заказ без указания id заказа'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/?courierId={new_courier['id']}")
        
        # Проверка ошибки
        assert accept_response.status_code == 404
        if accept_response.text:
            response_data = accept_response.json()
            # ДОБАВЛЕНО: проверка наличия сообщения
            assert "message" in response_data
        
        clean_courier(new_courier['data'])

    @allure.title('Проверка ошибки при принятии заказа с неверным id заказа')
    def test_order_accept_error_with_wrong_order_id(self, new_courier, clean_courier):
        if not new_courier.get('id'):
            pytest.skip("Courier not created")
            
        wrong_order_id = "888888888"
        
        with allure.step('Попытка принять заказ с несуществующим id заказа'):
            accept_response = requests.put(f"{Urls.URL_orders_accept}/{wrong_order_id}?courierId={new_courier['id']}")
        
        # Проверка ошибки "заказ не найден"
        assert accept_response.status_code == 404
        response_data = accept_response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        expected_message = "Заказа с таким id не существует"
        assert response_data["message"] == expected_message
        
        clean_courier(new_courier['data'])

        