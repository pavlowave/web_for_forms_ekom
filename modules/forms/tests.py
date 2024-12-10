import unittest
from rest_framework.test import APIClient
from tinydb import TinyDB

class FormMatchingViewTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Настройка для тестов
        """
        cls.db = TinyDB('database/test_tinydb_database.json')
        cls.db.insert({
            "name": "Order Form",
            "fields": {
                "email": "email",
                "phone": "phone",
                "order_date": "date"
            }
        })
        cls.db.insert({
            "name": "User Registration",
            "fields": {
                "email": "email",
                "user_name": "text",
                "birth_date": "date"
            }
        })
        cls.db.insert({
            "name": "Contact Form",
            "fields": {
                "user_name": "text",
                "lead_email": "email",
                "phone": "phone"
            }
        })

        cls.client = APIClient()

    def test_valid_template_found(self):
        """
        Тест для случая, когда шаблон формы найден.
        """
        data = {
            "fields": {
                "email": "test@example.com",
                "phone": "+7 999 999 99 99",
                "order_date": "2024-12-09"
            }
        }

        response = self.client.post('/get_form/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"template_name": "Order Form"})

    def test_template_found_with_valid_fields(self):
        """
        Тест для случая, когда все поля правильные, и найден подходящий шаблон.
        """
        data = {
            "fields": {
                "email": "test@mail.ru",
                "phone": "+79999999999",
                "order_date": "2024-12-09",
                "user_name": "ExtraUser"
            }
        }

        response = self.client.post('/get_form/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["template_name"], "Order Form")

    def test_invalid_email(self):
        """
        Тест для случая, когда в поле email передан неверный формат email.
        """
        data = {
            "fields": {
                "email": "invalid-email",
                "phone": "+7 999 999 99 99",
                "order_date": "2024-12-09"
            }
        }

        response = self.client.post('/get_form/', data, format='json')

        self.assertIn("email", response.data, "Ответ не содержит ключ 'email'")
        self.assertIn("phone", response.data, "Ответ не содержит ключ 'phone'")
        self.assertIn("order_date", response.data, "Ответ не содержит ключ 'order_date'")

        self.assertEqual(response.data["email"], "text")
        self.assertEqual(response.data["phone"], "phone")
        self.assertEqual(response.data["order_date"], "date")

    def test_invalid_phone(self):
        """
        Тест для случая, когда в поле phone передан неверный формат номера телефона.
        """
        data = {
            "fields": {
                "email": "test@example.com",
                "phone": "12345",
                "order_date": "2024-12-09"
            }
        }

        response = self.client.post('/get_form/', data, format='json')

        self.assertIn("email", response.data)
        self.assertIn("phone", response.data)
        self.assertIn("order_date", response.data)

        self.assertEqual(response.data["email"], "email")
        self.assertEqual(response.data["phone"], "text")
        self.assertEqual(response.data["order_date"], "date")

    def test_missing_required_field(self):
        """
        Тест для случая, когда в данных отсутствует обязательное поле.
        """
        data = {
            "fields": {
                "email": "test@example.com",
                "phone": "+7 999 999 99 99"
            }
        }

        response = self.client.post('/get_form/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data.get("template_name"))

        self.assertIn("email", response.data)
        self.assertIn("phone", response.data)
        self.assertEqual(response.data["email"], "email")
        self.assertEqual(response.data["phone"], "phone")

    def test_template_not_found(self):
        """
        Тест для случая, когда не найден шаблон для формы.
        """
        data = {
            "fields": {
                "email": "test@example.com",
                "phone": "+7 999 999 99 99",
                "nonexistent_field": "something"
            }
        }

        response = self.client.post('/get_form/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data.get("template_name"))

        self.assertIn("email", response.data)
        self.assertIn("phone", response.data)
        self.assertIn("nonexistent_field", response.data)
        self.assertEqual(response.data["email"], "email")
        self.assertEqual(response.data["phone"], "phone")
        self.assertEqual(response.data["nonexistent_field"], "text")

    @classmethod
    def tearDownClass(cls):
        """
        Очистка после тестов
        """
        cls.db.truncate()

if __name__ == '__main__':
    unittest.main()
