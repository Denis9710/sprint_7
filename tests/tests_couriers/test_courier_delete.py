import requests
import allure
from urls import Urls


class TestCourierDelete:

    @allure.title('Проверка успешного удаления курьера')
    def test_courier_delete_success(self, new_courier):
        # Пропускаем тест если курьер не создан
        if not new_courier.get('id'):
            pytest.skip("Courier not created")
            
        with allure.step('Отправка DELETE запроса на удаление курьера по id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{new_courier['id']}")
        
        # Проверка успешного удаления (код 200 и тело ответа {"ok": true})
        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}

    @allure.title('Проверка ошибки при попытке удаления курьера без указания id')
    def test_courier_delete_error_without_id(self):
        with allure.step('Отправка DELETE запроса на удаление с пустым id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/")
        
        # Проверка ошибки (код 404 и сообщение)
        assert delete_response.status_code == 404
        # Дополнительная проверка текста ошибки, если API возвращает сообщение
        if delete_response.text:  # если есть тело ответа
            response_data = delete_response.json()
            assert "message" in response_data  # проверяем наличие сообщения

    @allure.title('Проверка ошибки при попытке удаления курьера с несуществующим id')
    def test_courier_delete_error_with_nonexistent_id(self):
        # Создание несуществующего id курьера
        nonexistent_id = "1234567890"
        
        with allure.step('Отправка DELETE запроса на удаление с несуществующим id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{nonexistent_id}")
        
        # Проверка ошибки (код 404 и сообщение)
        expected_message = "Курьера с таким id нет."
        assert delete_response.status_code == 404
        assert delete_response.json()["message"] == expected_message

    @allure.title('Проверка неуспешного запроса на удаление курьера')
    def test_courier_delete_unsuccessful_request(self):
        # Отправка запроса на удаление с некорректным id
        invalid_id = "invalid_id_123"
        
        with allure.step('Отправка DELETE запроса на удаление с некорректным id'):
            delete_response = requests.delete(f"{Urls.URL_courier_delete}/{invalid_id}")
        
        # Проверка ошибки сервера (код 500 и сообщение)
        assert delete_response.status_code == 500
        if delete_response.text:  # если API возвращает сообщение об ошибке
            response_data = delete_response.json()
            assert "message" in response_data