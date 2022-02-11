import requests

uri = 'http://127.0.0.1:5000/cliente'


response = requests.post(uri, json = {
        'nome': 'Rissa Veronica',
        'telefone': 913232309,
        'nif': 918273121,
        'email': 'raissa@exemplo.com'})
print(response.text)