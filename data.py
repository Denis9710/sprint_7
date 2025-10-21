class TestData:
 
    correct_login = "Denis06101997"
    correct_password = "qweasdzxc123" 
    correct_first_name = "Denis"
    valid_courier_credentials = {"login": "Denis06101997", "password": "qweasdzxc123", "firstName": "Denis"}
    courier_without_firstname = {"login": "Denis06101997", "password": "1234"}
    courier_wrong_password = {"login": "Denis06101997", "password": "invalid"}


class TestOrderData:
    order_data_grey = {
        "firstName": "Денис",
        "lastName": "Балашов",
        "address": "Графская, 11",
        "metroStation": 7,
        "phone": "+7 920 954 19 98",
        "rentTime": 2,
        "deliveryDate": "2025-10-18",
        "comment": "Дай бог нам выжить?!",
        "color": [
            "GREY"
        ]
    }

    order_data_black = {
        "firstName": "Иван",
        "lastName": "Пупкин",
        "address": "Москва, улица Петровский, 78",
        "metroStation": 10,
        "phone": "+7 927 827 10 11",
        "rentTime": 4,
        "deliveryDate": "2025-10-18",
        "comment": "Погнали",
        "color": [
            "BLACK"
        ]
    }

    order_data_two_colors = {
        "firstName": "Сергей",
        "lastName": "Балашов",
        "address": "Москва, ул. Восстания, 99",
        "metroStation": 25,
        "phone": "+7 999 999 99 99",
        "rentTime": 1,
        "deliveryDate": "2025-10-17",
        'comment': "Аминь!",
        "color": [
            "BLACK", "GREY"
        ]
    }

    order_data_no_colors = {
        "firstName": "Denis",
        "lastName": "Balashov",
        "address": "Санкт-Петербург, Сенная, 1",
        "metroStation": 20,
        "phone": "+7 999 001 55 99",
        "rentTime": 3,
        "deliveryDate": "2025-10-18",
        "comment": "Примите пожалуйста проект, я больше не могу!",
        "color": []
    }