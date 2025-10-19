import requests
import allure
import pytest
from urls import Urls


class TestOrdersGetList:

    @allure.title('Проверка получения списка заказов')
    @allure.description('Проверяются код и тело ответа.')
    def test_orders_get_list(self):
        with allure.step('Отправка GET запроса для получения списка заказов'):
            response = requests.get(Urls.URL_orders_list)
        
        # Проверка успешного ответа (код 200)
        assert response.status_code == 200
        
        # Проверка структуры ответа
        response_data = response.json()
        assert 'orders' in response_data
        assert isinstance(response_data['orders'], list)
        
        # Проверка что список не пустой и содержит заказы с id
        if response_data['orders']:  # если список не пустой
            first_order = response_data['orders'][0]
            assert 'id' in first_order
            # Дополнительные проверки структуры заказа
            assert 'track' in first_order or 'status' in first_order  # проверяем обязательные поля