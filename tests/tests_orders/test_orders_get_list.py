import requests
import allure
from urls import Urls

class TestOrdersGetList:

    @allure.title('Проверка получения списка заказов')
    def test_orders_get_list(self):
        with allure.step('Отправка GET запроса для получения списка заказов'):
            response = requests.get(Urls.URL_orders_list)
        
        # Проверка успешного ответа
        assert response.status_code == 200
        
        response_data = response.json()
        # ДОБАВЛЕНО: проверка структуры ответа
        assert 'orders' in response_data
        assert isinstance(response_data['orders'], list)
        
        # Проверка что список не пустой и содержит заказы с правильной структурой
        if response_data['orders']:
            first_order = response_data['orders'][0]
            # Проверяем обязательные поля заказа
            assert 'id' in first_order
            assert 'track' in first_order
            assert 'status' in first_order
            # ДОБАВЛЕНО: проверка типов данных
            assert isinstance(first_order['id'], int)
            assert isinstance(first_order['track'], int)

            