import requests
import allure
import pytest
from data import TestData as Data
from urls import Urls
import helpers as h

class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    def test_courier_login_success(self, new_courier):  # УДАЛЕНО: clean_courier
        with allure.step('Отправка POST запроса на авторизацию с валидными данными'):
            response = requests.post(Urls.URL_courier_login, data={
                'login': new_courier['data']['login'],
                'password': new_courier['data']['password']
            })
        
        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        assert isinstance(response_data['id'], int)
        assert response_data['id'] > 0
        
        # УДАЛЕНО: clean_courier(new_courier['data'])

    @allure.title('Проверка возврата id при успешной авторизации')
    def test_courier_login_returns_id(self, new_courier):  # УДАЛЕНО: clean_courier
        with allure.step('Отправка POST запроса на авторизацию'):
            response = requests.post(Urls.URL_courier_login, data={
                'login': new_courier['data']['login'],
                'password': new_courier['data']['password']
            })
        
        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        assert isinstance(response_data['id'], int)
        assert response_data['id'] > 0
        
        # УДАЛЕНО: clean_courier(new_courier['data'])
        