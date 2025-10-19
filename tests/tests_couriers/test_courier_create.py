import requests
import allure
import pytest
from urls import Urls
import helpers as h

class TestCourierCreate:

    @allure.title('Проверка создания аккаунта курьера с валидными данными')
    def test_create_courier_account(self, new_courier, clean_courier):
        # Проверяем что курьер создан успешно
        assert new_courier['id'] is not None
        assert 'data' in new_courier
        # ДОБАВЛЕНО: проверка структуры данных
        assert 'login' in new_courier['data']
        assert 'password' in new_courier['data']
        assert 'firstName' in new_courier['data']
        
        clean_courier(new_courier['data'])

    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    def test_create_courier_account_login_conflict(self, new_courier, clean_courier):
        # Пытаемся создать второго курьера с тем же логином
        payload_conflict = {
            'login': new_courier['data']['login'],
            'password': h.create_random_password(),
            'firstName': h.create_random_firstname()
        }
        
        with allure.step('Попытка создания второго курьера с тем же логином'):
            response = requests.post(Urls.URL_courier_create, data=payload_conflict)
        
        # Проверка конфликта
        expected_message = "Этот логин уже используется. Попробуйте другой."
        assert response.status_code == 409
        response_data = response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        assert response_data["message"] == expected_message
        
        clean_courier(new_courier['data'])

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_impossibility_create_two_similar(self, clean_courier):
        payload = {
            'login': h.create_random_login(),
            'password': h.create_random_password(),
            'firstName': h.create_random_firstname()
        }
        
        with allure.step('Первое создание курьера'):
            first_response = requests.post(Urls.URL_courier_create, data=payload)
        
        with allure.step('Второе создание курьера с теми же данными'):
            second_response = requests.post(Urls.URL_courier_create, data=payload)
        
        # Проверка: первый успешен, второй возвращает ошибку
        expected_message = "Этот логин уже используется. Попробуйте другой."
        assert first_response.status_code == 201
        # ДОБАВЛЕНО: проверка текста успешного ответа
        first_response_data = first_response.json()
        assert "ok" in first_response_data
        assert first_response_data["ok"] == True
        
        assert second_response.status_code == 409
        second_response_data = second_response.json()
        assert second_response_data["message"] == expected_message
        
        clean_courier(payload)

    @allure.title('Проверка получения ошибки при создании курьера с незаполненными обязательными полями')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': h.create_random_password(), 'firstName': h.create_random_firstname()},
        {'login': h.create_random_login(), 'password': '', 'firstName': h.create_random_firstname()}
    ])
    def test_create_courier_account_with_empty_required_fields(self, empty_credentials, clean_courier):
        with allure.step('Отправка запроса с незаполненными обязательными полями'):
            response = requests.post(Urls.URL_courier_create, data=empty_credentials)
        
        # Проверка ошибки валидации
        expected_message = "Недостаточно данных для создания учетной записи"
        assert response.status_code == 400
        response_data = response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        assert response_data["message"] == expected_message
        
        if response.status_code == 201:
            clean_courier(empty_credentials)

            