import requests
import allure
import pytest
from urls import Urls

class TestCourierDelete:

    @allure.title('Проверка успешного удаления курьера')
    def test_courier_delete_success(self, new_courier):
        if not new_courier.get('id'):
            pytest.skip("Courier not created")
            
        with allure.step('Отправка DELETE запроса на удаление курьера по id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{new_courier['id']}")
        
        # Проверка успешного удаления
        assert delete_response.status_code == 200
        response_data = delete_response.json()
        # ДОБАВЛЕНО: проверка текста ответа
        assert response_data == {"ok": True}
        assert "ok" in response_data
        assert response_data["ok"] == True

    @allure.title('Проверка ошибки при попытке удаления курьера без указания id')
    def test_courier_delete_error_without_id(self):
        with allure.step('Отправка DELETE запроса на удаление с пустым id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/")
        
        # Проверка ошибки
        assert delete_response.status_code == 404
        if delete_response.text:
            response_data = delete_response.json()
            # ДОБАВЛЕНО: проверка наличия сообщения об ошибке
            assert "message" in response_data


    @allure.title('Проверка ошибки при попытке удаления курьера с несуществующим id')
    def test_courier_delete_error_with_nonexistent_id(self):
        nonexistent_id = "1234567890"
        
        with allure.step('Отправка DELETE запроса на удаление с несуществующим id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{nonexistent_id}")
        
        # Проверка ошибки
        expected_message = "Курьера с таким id нет."
        assert delete_response.status_code == 404
        response_data = delete_response.json()
        # ДОБАВЛЕНО: проверка текста сообщения
        assert "message" in response_data
        assert response_data["message"] == expected_message

    @allure.title('Проверка неуспешного запроса на удаление курьера')
    def test_courier_delete_unsuccessful_request(self):
        invalid_id = "invalid_id_123"
        
        with allure.step('Отправка DELETE запроса на удаление с некорректным id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{invalid_id}")
        
        # Проверка ошибки сервера
        assert delete_response.status_code == 500
        if delete_response.text:
            response_data = delete_response.json()
            # ДОБАВЛЕНО: проверка наличия сообщения об ошибке
            assert "message" in response_data
