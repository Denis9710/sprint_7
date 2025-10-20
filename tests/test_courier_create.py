import requests
import allure
import pytest
from urls import Urls
import helpers as h

class TestCourierCreate:

    @allure.title('Проверка создания аккаунта курьера с валидными данными')
    def test_create_courier_account(self, new_courier):  # УДАЛЕНО: clean_courier
        # Проверяем что курьер создан успешно
        assert new_courier['id'] is not None
        assert 'data' in new_courier
        assert 'login' in new_courier['data']
        assert 'password' in new_courier['data']
        assert 'firstName' in new_courier['data']
        
        # УДАЛЕНО: clean_courier(new_courier['data'])

    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    def test_create_courier_account_login_conflict(self, new_courier):  # УДАЛЕНО: clean_courier
        payload_conflict = {
            'login': new_courier['data']['login'],
            'password': h.create_random_password(),
            'firstName': h.create_random_firstname()
        }
        
        with allure.step('Попытка создания второго курьера с тем же логином'):
            response = requests.post(Urls.URL_courier_create, data=payload_conflict)
        
        expected_message = "Этот логин уже используется. Попробуйте другой."
        assert response.status_code == 409
        response_data = response.json()
        assert "message" in response_data
        assert response_data["message"] == expected_message
        
   
   