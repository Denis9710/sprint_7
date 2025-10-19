import requests
import allure
from urls import Urls

class TestOrderGetByTrack:

    @allure.title('Проверка успешного получения заказа по номеру')
    def test_order_get_by_track_success(self, new_order):
        with allure.step('Получение заказа по track номеру'):
            get_response = requests.get(f"{Urls.URL_orders_get}?t={new_order['track_id']}")
        
        # Проверка успешного получения заказа
        assert get_response.status_code == 200
        response_data = get_response.json()
        # ДОБАВЛЕНО: проверка структуры ответа
        assert 'order' in response_data
        order_data = response_data['order']
        # Проверяем основные поля заказа
        assert 'id' in order_data
        assert 'track' in order_data
        assert order_data['track'] == new_order['track_id']

    @allure.title('Проверка ошибки при получении заказа без номера')
    def test_order_get_by_track_error_without_track(self):
        with allure.step('Попытка получить заказ без указания track номера'):
            get_response = requests.get(f"{Urls.URL_orders_get}")
        
        # Проверка ошибки
        expected_message = "Недостаточно данных для поиска"
        assert get_response.status_code == 400
        response_data = get_response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        assert response_data["message"] == expected_message

    @allure.title('Проверка ошибки при получении заказа с несуществующим номером')
    def test_order_get_by_track_error_with_wrong_track(self):
        wrong_track_id = "999999999"
        
        with allure.step('Попытка получить заказ с несуществующим track номером'):
            get_response = requests.get(f"{Urls.URL_orders_get}?t={wrong_track_id}")
        
        # Проверка ошибки "заказ не найден"
        expected_message = "Заказ не найден"
        assert get_response.status_code == 404
        response_data = get_response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        assert response_data["message"] == expected_message

        