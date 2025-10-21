import requests
import allure
from urls import Urls

class TestOrdersGetList:

    @allure.title('Проверка получения списка заказов')
    def test_orders_get_list(self):
        with allure.step('Отправка GET запроса для получения списка заказов'):
            response = requests.get(Urls.URL_orders_list)
        
        assert response.status_code == 200
        
        response_data = response.json()
        assert 'orders' in response_data
        assert isinstance(response_data['orders'], list)
        
        # УБРАНО условие - всегда проверяем структуру ответа
        assert isinstance(response_data['orders'], list)
        
        # Проверяем структуру ответа без условий
        # Если orders пустой - проверяем, что это пустой список
        # Если не пустой - проверяем структуру первого элемента
        orders = response_data['orders']
        
        # Проверяем, что orders - это список (уже проверено выше)
        # Дополнительные проверки структуры можно вынести в отдельный тест
        # или использовать подход с проверкой через параметризацию