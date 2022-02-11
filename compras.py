from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from utils_web_service import importar_dados_compras, importar_dados_compras_especifico, importar_todos_dados_compras
import GLOBAL_VARIABLES


class ComprasNormal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mostra_compras(self):
        if self.ids.scroll_compras.cols == 0:
            self.ids.scroll_compras.cols = 6
            print(GLOBAL_VARIABLES.USER_ID)
            idclient = GLOBAL_VARIABLES.USER_ID
            response = importar_dados_compras(idclient).json()
            print(type(response))
            print(response["message"])
            if response["message"] == "success":
                compras = response["dados"]
                for compra in compras:
                    numero_de_compra = Button(text=f"""Numero de\nCompra:\n\n{compra["idcompra"]}""", bold=True)
                    numero_de_compra.bind(on_release=self.mostra_compra_especifica)
                    data_de_compra = Label(text=f"""Data:\n\n{compra["data"]}""", bold=True)
                    moto = Label(text=f"""Moto:\n\n{compra["marca"]}\n{compra["modelo"]}""", bold=True)
                    preco = Label(text=f"""Preço:\n\n{compra["preco"]}€""", bold=True)
                    quantidade = Label(text=f"""Quantidade:\n\n{compra["quantidade"]}""", bold=True)
                    total = Label(text=f"""Total:\n\n{compra["total"]}€""", bold=True)
                    for labels in (numero_de_compra, data_de_compra, moto, preco, quantidade, total):
                        self.ids.scroll_compras.add_widget(labels)
        else:
            self.ids.scroll_compras.clear_widgets()
            self.ids.scroll_compras.cols = 0
            self.ids.scroll_compras.size_hint = (None, None)

    def mostra_compra_especifica(self, instance):
        print("botao apertado")
        self.ids.scroll_compras.clear_widgets()
        self.ids.scroll_compras.cols = 6
        self.ids.scroll_compras.size_hint = (1, 1)
        temp_string = instance.text
        number = [int(temp) for temp in temp_string.split() if temp.isdigit()]
        print(type(number), number[0])
        response = importar_dados_compras_especifico(number[0]).json()
        print(response)
        if response["message"] == "success":
            compra = response["compra"]
            print(compra)
            self.ids.scroll_compras.cols = len(compra)

            numero_de_compra = Button(text=f"""Numero de\nCompra:\n\n{compra["idcompra"]}""", bold=True)
            data_de_compra = Label(text=f"""Data da Compra:\n\n{compra["data"]}""", bold=True)
            moto = Label(text=f"""Moto:\n\n{compra["marca"]}""", bold=True)
            preco = Label(text=f"""Preço:\n\n{compra["preco"]}€""", bold=True)
            quantidade = Label(text=f"""Quantidade:\n{compra["quantidade"]}""", bold=True)
            total = Label(text=f"""Total:\n\n{compra["total"]}€""", bold=True)
            for labels in (numero_de_compra, data_de_compra, moto, preco, quantidade, total):
                self.ids.scroll_compras.add_widget(labels)

    def comprar_normal(self):
        pass

    def atras(self):
        if GLOBAL_VARIABLES.USER_IS_MASTER:
            self.manager.current = 'paginainicialmaster'
        else:
            self.manager.current = 'paginainicialnormal'


class ComprasMaster(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mostra_compras(self):
        if self.ids.scroll_compras_master.cols == 0:
            self.ids.scroll_compras_master.cols = 6
            print(GLOBAL_VARIABLES.USER_ID)
            idclient = GLOBAL_VARIABLES.USER_ID
            response = importar_dados_compras(idclient).json()
            print(type(response))
            print(response["message"])
            if response["message"] == "success":
                compras = response["dados"]
                for compra in compras:
                    numero_de_compra = Button(text=f"""Numero de\nCompra:\n\n{compra["idcompra"]}""", bold=True)
                    numero_de_compra.bind(on_release=self.mostra_compra_especifica)
                    data_de_compra = Label(text=f"""Data:\n\n{compra["data"]}""", bold=True)
                    moto = Label(text=f"""Moto:\n\n{compra["marca"]}\n{compra["modelo"]}""", bold=True)
                    preco = Label(text=f"""Preço:\n\n{compra["preco"]}€""", bold=True)
                    quantidade = Label(text=f"""Quantidade:\n\n{compra["quantidade"]}""", bold=True)
                    total = Label(text=f"""Total:\n\n{compra["total"]}€""", bold=True)
                    for labels in (numero_de_compra, data_de_compra, moto, preco, quantidade, total):
                        self.ids.scroll_compras_master.add_widget(labels)
        else:
            self.ids.scroll_compras_master.clear_widgets()
            self.ids.scroll_compras_master.cols = 0
            self.ids.scroll_compras_master.size_hint = (None, None)
            
    def mostra_compras_master(self):
        if self.ids.scroll_compras_master.cols == 0:
            self.ids.scroll_compras_master.cols = 6
            response = importar_todos_dados_compras().json()
            print(response)
            if response["message"] == "success":
                compras = response["compras"]
                print(compras)
                for compra in compras:
                    print(compra)
                    numero_de_compra = Button(text=f"""Numero de\nCompra:\n\n{compra["idcompra"]}""", bold=True)
                    numero_de_compra.bind(on_release=self.mostra_compra_especifica)
                    data_de_compra = Label(text=f"""Data:\n\n{compra["data"]}""", bold=True)
                    moto = Label(text=f"""Moto:\n\n{compra["marca"]}\n{compra["modelo"]}""", bold=True)
                    preco = Label(text=f"""Preço:\n\n{compra["preco"]}€""", bold=True)
                    quantidade = Label(text=f"""Quantidade:\n\n{compra["quantidade"]}""", bold=True)
                    total = Label(text=f"""Total:\n\n{compra["total"]}€""", bold=True)
                    for labels in (numero_de_compra, data_de_compra, moto, preco, quantidade, total):
                        self.ids.scroll_compras_master.add_widget(labels)
        else:
            self.ids.scroll_compras_master.clear_widgets()
            self.ids.scroll_compras_master.cols = 0
            self.ids.scroll_compras_master.size_hint = (None, None)

    def mostra_compra_especifica(self, instance):
        print("botao apertado")
        self.ids.scroll_compras_master.clear_widgets()
        self.ids.scroll_compras_master.cols = 6
        self.ids.scroll_compras_master.size_hint = (1, 1)
        temp_string = instance.text
        number = [int(temp) for temp in temp_string.split() if temp.isdigit()]
        print(type(number), number[0])
        response = importar_dados_compras_especifico(number[0]).json()
        print(response)
        if response["message"] == "success":
            compra = response["compra"]
            print(compra)
            self.ids.scroll_compras_master.cols = len(compra)

            numero_de_compra = Button(text=f"""Numero de\nCompra:\n\n{compra["idcompra"]}""", bold=True)
            data_de_compra = Label(text=f"""Data da Compra:\n\n{compra["data"]}""", bold=True)
            moto = Label(text=f"""Moto:\n\n{compra["marca"]}""", bold=True)
            preco = Label(text=f"""Preço:\n\n{compra["preco"]}€""", bold=True)
            quantidade = Label(text=f"""Quantidade:\n{compra["quantidade"]}""", bold=True)
            total = Label(text=f"""Total:\n\n{compra["total"]}€""", bold=True)
            for labels in (numero_de_compra, data_de_compra, moto, preco, quantidade, total):
                self.ids.scroll_compras_master.add_widget(labels)

    def atras(self):
        if GLOBAL_VARIABLES.USER_IS_MASTER:
            self.manager.current = 'paginainicialmaster'
        else:
            self.manager.current = 'paginainicialnormal'