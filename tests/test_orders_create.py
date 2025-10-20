import requests
import allure
import json
from urls import Urls

class TestOrderCreate:

    @allure.title('Проверка создания заказа с разными параметрами цвета')
    def test_order_create_color_parametrize_success(self, order_data, clean_order):
        order_data_json = json.dumps(order_data['data'])
        headers = {'Content-Type': 'application/json'}
        
        with allure.step('Отправка POST запроса на создание заказа'):
            response = requests.post(Urls.URL_orders_create, data=order_data_json, headers=headers, timeout=5)
        
        # Проверка успешного создания заказа
        assert response.status_code == 201
        response_data = response.json()
        # ДОБАВЛЕНО: проверка структуры ответа
        assert 'track' in response_data
        assert isinstance(response_data['track'], int)
        assert response_data['track'] > 0
        
        # Очистка заказа выполняется в фикстуре order_data


        