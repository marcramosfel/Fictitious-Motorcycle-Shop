from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from config import config
from GLOBAL_VARIABLES import NOME_BASE_DADOS, WEB_SERVICE_URI
import os

# NOME_BASE_DADOS = 'trabkivy'

app = Flask(__name__)
conexion = MySQL(app)

@app.route("/check_general_statistics", methods=["GET"])
def check_general_statistics():
    try:
        cursor = conexion.connection.cursor()
        sql = f"""
                SELECT 
                    SUM(compra.quantidade) as quantidade_total_motos_vendidas,
                    COUNT(compra.idcompra) AS numero_de_vendas,
                    SUM(compra.quantidade * motorizada.preco) AS total_em_euros
                FROM
                    {NOME_BASE_DADOS}.compra
                        INNER JOIN
                    {NOME_BASE_DADOS}.clientes ON compra.idcliente = clientes.idcliente
                        INNER JOIN
                    {NOME_BASE_DADOS}.motorizada ON compra.idmotorizada = motorizada.idmotorizada
                """
        print(sql)
        cursor.execute(sql)
        estatisticas = cursor.fetchone()

        return jsonify({"message": "success", "estatisticas":estatisticas})

    except Exception as err:
        return jsonify({"message": err.__repr__()})

@app.route("/check_statistics_by_client", methods=["POST"])
def check_statistics_by_client():
    try:
        print(request.json)
        cursor = conexion.connection.cursor()
        sql = f"""
                    SELECT 
                        clientes.nome,
                        COUNT(compra.idcompra) AS numero_de_compras,
                        SUM(compra.quantidade * motorizada.preco) AS total
                    FROM
                        {NOME_BASE_DADOS}.compra
                            INNER JOIN
                        {NOME_BASE_DADOS}.clientes ON compra.idcliente = clientes.idcliente
                            INNER JOIN
                        {NOME_BASE_DADOS}.motorizada ON compra.idmotorizada = motorizada.idmotorizada
                    WHERE
                        clientes.nome = '{request.json['cliente']}'
                    GROUP BY clientes.nome
                """
        print(sql)
        cursor.execute(sql)
        estatisticas = cursor.fetchone()

        return jsonify({"message": "success", "estatisticas":estatisticas})

    except Exception as err:
        return jsonify({"message": err.__repr__()})


@app.route("/check_statistics_by_date", methods=["POST"])
def check_statistics_by_date():
    try:
        print(request.json)
        cursor = conexion.connection.cursor()
        sql=f"""
                SELECT 
                    count(compra.idcompra) as numero_de_vendas,
                    compra.date,
                    sum(compra.quantidade * motorizada.preco) AS total
                FROM
                    {NOME_BASE_DADOS}.compra
                INNER JOIN
                    {NOME_BASE_DADOS}.clientes ON compra.idcliente = clientes.idcliente
                INNER JOIN
                    {NOME_BASE_DADOS}.motorizada ON compra.idmotorizada = motorizada.idmotorizada
                WHERE
                    date = '{request.json["date"]}'
                GROUP BY date
                """
        print(sql)
        cursor.execute(sql)
        estatisticas = cursor.fetchone()

        return jsonify({"message": "success", "estatisticas":estatisticas})

    except Exception as err:
        return jsonify({"message": err.__repr__()})



@app.route("/importar_todos_dados_compras", methods =["GET"])
def importar_todos_dados_compras():
    try:
        cursor = conexion.connection.cursor()
        sql = f""" 
                SELECT
                    compra.idcompra,
                    compra.date,
                    clientes.nome,
                    motorizada.marca,
                    motorizada.modelo,
                    compra.quantidade,
                    motorizada.preco,
                    compra.quantidade * motorizada.preco AS total
                FROM
                    {NOME_BASE_DADOS}.compra
                        INNER JOIN
                    {NOME_BASE_DADOS}.clientes ON compra.idcliente = clientes.idcliente
                        INNER JOIN
                    {NOME_BASE_DADOS}.motorizada ON compra.idmotorizada = motorizada.idmotorizada 
                """
        cursor.execute(sql)
        resultado = cursor.fetchall()

        dados_compras = []
        for file in resultado:
            compra = {'idcompra': file[0],
                      'data': file[1],
                      'nome': file[2],
                      'marca': file[3],
                      'modelo': file[4],
                      'quantidade': file[5],
                      'preco': file[6],
                      'total': file[7]
                      }
            dados_compras.append(compra)
        # print(cliente)
        return jsonify({"compras": dados_compras, "message": "success"})
    except Exception as err:
        return jsonify({"message": err.__repr__()})


@app.route("/importar_dados_compras_especifico/<id_compra>", methods =["GET"])
def importar_dados_compras_especifico(id_compra):
    try:

        cursor = conexion.connection.cursor()
        sql = f"""SELECT 
                    compra.idcompra,
                    compra.date,
                    clientes.nome,
                    motorizada.marca,
                    motorizada.modelo,
                    compra.quantidade,
                    motorizada.preco,
                    compra.quantidade * motorizada.preco AS total
                FROM
                    {NOME_BASE_DADOS}.compra
                        INNER JOIN
                    {NOME_BASE_DADOS}.clientes ON compra.idcliente = clientes.idcliente
                        INNER JOIN
                    {NOME_BASE_DADOS}.motorizada ON compra.idmotorizada = motorizada.idmotorizada
                WHERE
                    compra.idcompra = {id_compra}"""
        cursor.execute(sql)
        resultado = cursor.fetchone()
        if resultado != None:
            compra = {'idcompra': resultado[0],
                       'data': resultado[1],
                       'nome': resultado[2],
                       'marca': resultado[3],
                       'modelo': resultado[4],
                       'quantidade': resultado[5],
                       'preco': resultado[6],
                       'total': resultado[7]
                      }
            return jsonify({"compra": compra, "message": "success"})
        else:
            return jsonify({"message": "compra nao encontrada"})
    except Exception as err:
        return jsonify({"message": err.__repr__()})


@app.route("/importar_dados_compras/<id_account>", methods=['GET'])
def importar_dados_compras(id_account):
    try:
        id_account = str(id_account)
        print(NOME_BASE_DADOS)
        cursor = conexion.connection.cursor()
        sql = f"""SELECT 
                    compra.idcompra,
                    compra.date,
                    clientes.nome,
                    motorizada.marca,
                    motorizada.modelo,
                    compra.quantidade,
                    motorizada.preco,
                    compra.quantidade * motorizada.preco AS total
                FROM
                    {NOME_BASE_DADOS}.compra
                        INNER JOIN
                    {NOME_BASE_DADOS}.clientes ON compra.idcliente = clientes.idcliente
                        INNER JOIN
                    {NOME_BASE_DADOS}.motorizada ON compra.idmotorizada = motorizada.idmotorizada
                WHERE
                    compra.idcliente = {id_account}"""
        print(sql)
        cursor.execute(sql)
        resultado = cursor.fetchall()
        dados = []
        for file in resultado:
            dados_compras = {'idcompra': file[0],
                       'data': file[1],
                       'nomecliente': file[2],
                       'marca': file[3],
                       'modelo': file[4],
                       'quantidade': file[5],
                       'preco': file[6],
                       'total': file[7]}
            dados.append(dados_compras)
        return jsonify({"message": "success", "dados": dados})
    except Exception as err:
        return jsonify({"message": err.__repr__()})


# FAZ UPDATE DO UTILIZADOR RETURN ERRO CASO JÁ EXISTA EMAIL
@app.route("/update_account/<id_account>", methods=['PUT'])
def update_account(id_account):
    try:
        id_account = str(id_account)
        print(NOME_BASE_DADOS)
        cursor = conexion.connection.cursor()
        sql = f"""UPDATE {NOME_BASE_DADOS}.clientes 
                SET nome = "{request.json["nome"]}", telefone = {request.json["telefone"]}, email = "{request.json["email"]}", 
                is_master = {request.json["is_master"]}, password = "{request.json["password"]}"
                WHERE idcliente = {id_account}"""
        print(sql)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"message": "success"})
    except Exception as err:
        return jsonify({"message": err.__repr__()})


# REGISTA UTILIZADOR RETURN ERRO CASO JÁ EXISTA EMAIL
@app.route("/register_account", methods=['POST'])
def register_account():
    try:
        print(NOME_BASE_DADOS)
        cursor = conexion.connection.cursor()
        sql_check = f"SELECT * FROM {NOME_BASE_DADOS}.clientes WHERE nif={request.json['nif']}"
        print(sql_check)
        cursor.execute(sql_check)
        if len(cursor.fetchall()) > 0:
            raise Exception("error_nif_exists")

        sql_check = f"""SELECT * FROM {NOME_BASE_DADOS}.clientes WHERE email = '{request.json['email']}' """
        print(sql_check)
        cursor.execute(sql_check)
        if len(cursor.fetchall()) > 0:
            raise Exception("error_email_exists")

        sql = f'INSERT INTO {NOME_BASE_DADOS}.clientes VALUES(DEFAULT, "{request.json["nome"]}", "{request.json["telefone"]}", {request.json["nif"]}, "{request.json["email"]}",{request.json["is_master"]}, "{request.json["password"]}")'
        print(sql)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"message": "success"})
    except Exception as err:
        return jsonify({"message": err.__repr__()})


@app.route('/check_login_by_id', methods=['POST'])
def check_login_by_id():
    print(request.json)
    try:
        cursor = conexion.connection.cursor()
        sql = f'SELECT * FROM {NOME_BASE_DADOS}.clientes WHERE idcliente="{request.json["idaccount"]}"'
        cursor.execute(sql)
        result = cursor.fetchall()
        passw = result[0][6]  # nao funciona direto da erro de list out of index (-_-)
        print(passw)
        return jsonify({"message": "success", "is_master": result[0][5], "email": result[0][4], "name": result[0][1],
             "telefone": result[0][2], "password": passw, "id_account": result[0][0]})
    except Exception as err:
        return jsonify({"message": "Something went bad!", 'error': err.__repr__()})


# ROTA RECEBE UM JSON COM EMAIL E PASSWORD E VERIFICA SE COICIDE SE COICIDIR RETORNA TRUE
@app.route('/checking_account', methods=['POST'])
def checking_account():
    print(request.json)
    try:
        cursor = conexion.connection.cursor()
        sql = f'SELECT * FROM {NOME_BASE_DADOS}.clientes WHERE email="{request.json["email"]}"'
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(type(result))
        # print(len(result))
        passw = result[0][6]  # nao funciona direto da erro de list out of index (-_-)
        print(passw)
        if result[0][0] == 0:
            raise Exception('Email não registado!')
        if result[0][6] == request.json['password']:
            return jsonify(
                {"message": "success", "is_master": result[0][5], "email": result[0][4], "name": result[0][1],
                 "telefone": result[0][2], "password": passw, "id_account": result[0][0]})
        else:
            return jsonify({"message": "password_incorrect"})

    except Exception as err:
        return jsonify({"message": "Something went bad!", 'error': err.__repr__()})


# Motorizadas
@app.route('/search_motos', methods=['POST'])
def search_motos():
    cursor = conexion.connection.cursor()
    search = request.json['search']
    sql = f"""SELECT * FROM {NOME_BASE_DADOS}.motorizada WHERE 
    idmotorizada LIKE '%{search}%' or
    marca LIKE '%{search}%' or
    modelo LIKE '%{search}%' or
    matricula LIKE '%{search}%' or
    cilindrada LIKE '%{search}%' or
    stock LIKE '%{search}%' or
    preco LIKE '%{search}%'"""
    cursor.execute(sql)
    return jsonify(cursor.fetchall())


@app.route('/motorizadas', methods=['GET'])
def listar_motorizadas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM " + NOME_BASE_DADOS + ".motorizada"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as err:
        return jsonify({"message": "Something went bad!", 'error': err.__repr__()})


# Clientes
@app.route('/cliente')
def listar_cliente():
    try:
        cursor = conexion.connection.cursor()
        sql = f"SELECT * FROM {NOME_BASE_DADOS}.clientes"
        cursor.execute(sql)
        resultado = cursor.fetchall()

        clientes = []
        for file in resultado:
            cliente = {'idcliente': file[0],
                       'nome': file[1],
                       'telefone': file[2],
                       'nif': file[3],
                       'email': file[4],
                       'ismaster': file[5],
                       'password': file[6]}
            clientes.append(cliente)
        # print(cliente)
        return jsonify({"cliente": clientes, "message": "Everything went well!"})
    except Exception as ex:
        return jsonify({"message": "Something went bad!"}, ex)


@app.route('/cliente/<idcliente>', methods=['GET'])
def ler_cliente_especifico(idcliente):
    try:
        idcliente = str(idcliente)
        cursor = conexion.connection.cursor()
        sql = f"""SELECT * FROM {NOME_BASE_DADOS}.clientes WHERE idcliente = {idcliente} or nome ={idcliente}"""
        cursor.execute(sql)
        resultado = cursor.fetchone()
        if resultado != None:
            cliente = {'idcliente': resultado[0],
                       'nome': resultado[1],
                       'telefone': resultado[2],
                       'nif': resultado[3],
                       'email': resultado[4],
                       'ismaster': resultado[5],
                       'password': resultado[6]}


            return jsonify({"cliente": cliente, "message": "Everything went well!"})
        else:
            return jsonify({"message": "cliente nao encontrado"})
    except Exception as ex:
        return jsonify({"message": "Something went bad!"})


@app.route('/cliente', methods=['POST'])
def inserir_cliente():
    try:
        print(request.json['nome'], request.json['telefone'], request.json['nif'], request.json['email'])
        cursor = conexion.connection.cursor()
        sql = f"""INSERT INTO {NOME_BASE_DADOS}.clientes (idcliente, nome, telefone, nif, email)  
                           VALUES (
                           DEFAULT,
                           '{request.json['nome']}',
                           {request.json['telefone']},
                           {request.json['nif']},
                           '{request.json['email']}') """
        print(sql)
        cursor.execute(sql)
        print(sql)
        conexion.connection.commit()  # insere na base de dados

        return jsonify({"message": "cliente Criado!"})

    except Exception as ex:
        return jsonify({"message": "Something went bad!"})


def pagina_nao_encontrada(error):
    return "<h1> A Página não foi encontrada!!!... </h1>", 404


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run()
