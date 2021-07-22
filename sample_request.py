import requests

with open('example_base64_img.txt') as base64_file:
    files = {'media': base64_file}
    url = 'http://127.0.0.1:5000/'

    r = requests.post(url, files=files)
    print(r.json())
