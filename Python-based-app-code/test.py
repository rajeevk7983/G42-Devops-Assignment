import requests

# print(requests.post('http://<exposed LB externl IP of the flask-app>:5000/population/Melbourne', json={"population": 20}).text)
# print(requests.put('http://<exposed LB externl IP of the flask-app>:5000/population/Melbourne', json={"population": 20}).text)
# print(requests.get('http://<exposed LB externl IP of the flask-app>:5000/population/Melbourne').text)
print(requests.get('http://<exposed LB externl IP of the flask-app>:5000/health').text)

`we can run it via postman or via python command "python3 test.py"
