import unittest
import requests

URL = "http://10.0.0.1:8080"


class ApiPerformanceTesting(unittest.TestCase):
    def test_hello_endpoint(self):
        response = requests.get(f"{URL}/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Hello World!")

    def test_fibonacci_endpoint(self):
        test_values = [0, 1, 5, 10, 20]
        expected_values = [0, 1, 5, 55, 6765]

        for i, n in enumerate(test_values):
            with self.subTest(n=n):
                response = requests.get(f"{URL}/fibonacci/{n}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.headers["Content-Type"], "application/json")
                data = response.json()
                self.assertIn("number", data)
                self.assertIn("value", data)
                self.assertEqual(data["number"], n)
                self.assertEqual(data["value"], expected_values[i])

    def test_database_endpoint(self):
        response = requests.get(f"{URL}/database")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        data = response.json()
        self.assertIn("message", data)
        self.assertIsInstance(data["message"], str)


if __name__ == '__main__':
    unittest.main()
