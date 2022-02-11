import json
import re
import requests
import GLOBAL_VARIABLES


def check_general_statistics():
    response = requests.get(GLOBAL_VARIABLES.WEB_SERVICE_URI + f'check_general_statistics')
    return response.json()


def check_statistics_by_client(cliente):
    response = requests.post(GLOBAL_VARIABLES.WEB_SERVICE_URI + 'check_statistics_by_client', json={
        "cliente": cliente
    })
    return json.loads(response.text)


def check_statistics_by_date(data):
    response = requests.post(GLOBAL_VARIABLES.WEB_SERVICE_URI + 'check_statistics_by_date', json={
        "date": data
    })
    return json.loads(response.text)


def importar_todos_dados_compras():
    response = requests.get(GLOBAL_VARIABLES.WEB_SERVICE_URI + f'importar_todos_dados_compras')
    return response


def importar_dados_compras_especifico(id_compra):
    response = requests.get(GLOBAL_VARIABLES.WEB_SERVICE_URI + f'importar_dados_compras_especifico/{id_compra}')
    return response


def importar_dados_compras(idcliente):
    response = requests.get(GLOBAL_VARIABLES.WEB_SERVICE_URI + f'importar_dados_compras/{idcliente}')
    return response


def check_login(user, psw):
    response = requests.post(GLOBAL_VARIABLES.WEB_SERVICE_URI + 'checking_account', json={
        "email": user,
        "password": psw})
    return json.loads(response.text)


def check_login_by_id(id_account):
    response = requests.post(GLOBAL_VARIABLES.WEB_SERVICE_URI + 'check_login_by_id', json={
        "idaccount":id_account})
    return json.loads(response.text)


def coloca_utilizador(nome, psw, nif, email, is_master, telefone):
    valid = re.search(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}$', email)
    if valid:
        response = requests.post(GLOBAL_VARIABLES.WEB_SERVICE_URI + 'register_account', json={
            "email": email,
            "password": psw,
            "nome": nome,
            "nif": nif,
            "is_master": is_master,
            "telefone": telefone})
        response = json.loads(response.text)
        if response["message"] == "Exception('error_nif_exists')":
            return 'Ja existe um nif associado!'
        elif response["message"] == "Exception('error_email_exists')":
            return 'Ja existe um email associado!'
        elif response["message"] == "success":
            return 'O utilizador foi criado!!'
        elif response["message"] == """IntegrityError(1062, "Duplicate entry \'2147483647\' for key \'nif_UNIQUE\'")""":
            return 'Ja existe um nif associado!'
    else:
        return 'O email não é válido!!'


def atualiza_utilizador(idaccount, nome, psw, email, is_master, telefone):
    valid = re.search(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}$', email)
    if valid:
        response = requests.put(GLOBAL_VARIABLES.WEB_SERVICE_URI + f'update_account/{idaccount}', json={
            "idaccount": idaccount,
            "email": email,
            "password": psw,
            "nome": nome,
            "is_master": is_master,
            "telefone": telefone})
        response = json.loads(response.text)
        if response["message"] == "success":
            return 'Os dados do utilizador foram atualiazados!'
    else:
        return 'O email não é válido!!'

print(check_login_by_id(1))