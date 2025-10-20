import requests
import allure
import pytest
from data import TestData as Data
from urls import Urls
import helpers as h

class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    def test_courier_login_success(self, new_courier, clean_courier):
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
        
        clean_courier(new_courier['data'])

    @allure.title('Проверка получения ошибки аутентификации при вводе невалидных данных')
    @pytest.mark.parametrize('nonexistent_credentials', [
        {'login': h.create_random_login(), 'password': h.create_random_password()},
        {'login': Data.correct_login, 'password': h.create_random_password()}
    ])
    def test_courier_login_nonexistent_data_not_found(self, nonexistent_credentials):
        with allure.step('Отправка POST запроса на авторизацию с невалидными данными'):
            response = requests.post(Urls.URL_courier_login, data=nonexistent_credentials)
        
        expected_response = {'code': 404, 'message': 'Учетная запись не найдена'}
        assert response.status_code == 404
        response_data = response.json()
        assert response_data == expected_response
        assert response_data['code'] == 404
        assert response_data['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка получения ошибки аутентификации с пустым полем логина или пароля')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': h.create_random_password()},
        {'login': Data.correct_login, 'password': ''}
    ])
    def test_courier_login_empty_credentials_bad_request(self, empty_credentials):
        with allure.step('Отправка POST запроса на авторизацию с пустыми полями'):
            response = requests.post(Urls.URL_courier_login, data=empty_credentials)
        
        expected_response = {'code': 400, 'message': 'Недостаточно данных для входа'}
        assert response.status_code == 400
        response_data = response.json()
        assert response_data == expected_response
        assert response_data['code'] == 400
        assert response_data['message'] == 'Недостаточно данных для входа'

    @allure.title('Проверка возврата id при успешной авторизации')
    def test_courier_login_returns_id(self, new_courier, clean_courier):
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
        
        clean_courier(new_courier['data'])

        