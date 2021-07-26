import requests
import unittest


class BNPOrderTest(unittest.TestCase):
    def test_correct_pin_order(self):
        with open('example_base64_img.txt') as base64_file:
            files = {'media': base64_file}
            url = 'http://127.0.0.1:5000/'

            result = requests.post(url, files=files).json()
            self.assertEqual(result, {'order': [9, 7, 1, 4, 6, 2]})


if __name__ == '__main__':
    unittest.main()
