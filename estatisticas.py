import requests
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivy.uix.scrollview import ScrollView

import GLOBAL_VARIABLES
from utils_web_service import check_statistics_by_date, check_statistics_by_client, check_general_statistics


class Estatisticas(Screen):

    def on_save(self, instance, value, date_range):
        # print(instance, value, date_range)
        value = str(value)
        # print(self.ids.date_label.text)
        response = check_statistics_by_date(value)
        if response["message"] and response["estatisticas"] != None:
            estatisticas = response["estatisticas"]
            self.adicionar_dados_estatisticas(estatisticas)
            self.popupwindow.dismiss()
        else:
            print("não há estatistiscas para esse dia!")

    # Click Cancel
    def on_cancel(self, instance, value):
        print("You Clicked Cancel")
        self.popupwindow.dismiss()

    # Click OK
    def adicionar_dados_estatisticas(self, response):
        print(response[0], response[1], response[2])
        if self.ids.box_estatisticas.cols == 0:
            self.ids.box_estatisticas.cols = 1
            geral_estatisticas = Label(
                text=f"""No dia {response[1]}\n foi realizado um total de {response[0]} venda(s) nesse dia\n totalizando um valor de {response[2]}€ """,
                halign='center',
                valign='middle', font_size='30dp', bold=True)
            self.ids.box_estatisticas.add_widget(geral_estatisticas)
        else:
            self.ids.box_estatisticas.clear_widgets()
            self.ids.box_estatisticas.cols = 1
            geral_estatisticas = Label(
                text=f"""No dia {response[1]}\n foi realizado um total de {response[0]} venda(s) nesse dia\n totalizando um valor de {response[2]}€ """,
                halign='center',
                valign='middle', font_size='30dp', bold=True)
            # data = Label(text=f"""{response[1]}""")
            # valor_total = Label(text=f"""{response[2]}""")
            # for widget in (numero_de_vendas, data, valor_total):
            self.ids.box_estatisticas.add_widget(geral_estatisticas)

    def show_popup_data(self):
        show = MDDatePicker(year=2021, month=12, day=24, pos_hint={'center_x': .8, 'center_y': .5})
        show.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        self.popupwindow = Popup(title="Escolha a Data!", content=show, size_hint=(None, None),
                                 size=(555, 450), background_color=(1, 1, 1, 1))
        self.popupwindow.open()

    def mostrar_popup_data(self):
        self.show_popup_data()

    def adicionar_dados_estatisticas_cliente(self, response):
        if self.ids.box_estatisticas.cols == 0:
            self.ids.box_estatisticas.cols = 1
            geral_estatisticas = Label(
                text=f"""O cliente {response[0]}\n realizou um total de {response[1]} compra(s) \n gastando um valor total de {response[2]}€ """,
                halign='center',
                valign='middle', font_size='30dp', bold=True)
            self.ids.box_estatisticas.add_widget(geral_estatisticas)
        else:
            self.ids.box_estatisticas.clear_widgets()
            self.ids.box_estatisticas.cols = 1
            geral_estatisticas = Label(
                text=f"""O cliente {response[0]}\n realizou um total de {response[1]} compra(s) \n gastando um valor total de {response[2]}€ """,
                halign='center',
                valign='middle', font_size='30dp', bold=True)
            self.ids.box_estatisticas.add_widget(geral_estatisticas)

    def on_click_name(self, instance):
        value = str(instance.text)
        print(value)
        response = check_statistics_by_client(value)
        if response["message"] and response["estatisticas"] != None:
            estatisticas = response["estatisticas"]
            self.adicionar_dados_estatisticas_cliente(estatisticas)
            self.popup_cliente.dismiss()
        else:
            print("não há estatistiscas para esse cliente!")

    def show_popup_cliente(self):
        box_clientes = ScrollView(do_scroll_x=False, do_scroll_y=True)
        response = requests.get(GLOBAL_VARIABLES.WEB_SERVICE_URI + 'cliente')
        resultado = response.json()['cliente']
        grid_clientes = GridLayout(cols=1, padding=20, spacing=20
                                   , size_hint_y=None
                                   , size_hint_x=None
                                   , size=(500, 100)
                                   , height=500)

        # print(resultado)
        for cliente in resultado:
            print(cliente['nome'])
            button_cliente = Button(text=f"{cliente['nome']}")
            button_cliente.bind(on_release=self.on_click_name)
            grid_clientes.add_widget(button_cliente)
        box_clientes.add_widget(grid_clientes)
        show = box_clientes
        self.popup_cliente = Popup(title="Escolha o Cliente!", content=show, size_hint=(None, None),
                                   size=(555, 450), background_color=(1, 1, 1, 1))
        self.popup_cliente.open()

    def mostrar_popup_cliente(self):
        self.show_popup_cliente()

    def adicionar_estatisticas_geral(self, response):
        print(response)
        if self.ids.box_estatisticas.cols == 0:
            self.ids.box_estatisticas.cols = 1
            geral_estatisticas = Label(
                text=f"""O Stand Motorizas da Ualg realizou um total de\n {response[0]} vendas desde o ínicio.\n
                Foram vendidas {response[1]} motos \n e o valor total faturado foi {response[2]}€""",
                halign='center',
                valign='middle', font_size='30dp', bold=True)
            self.ids.box_estatisticas.add_widget(geral_estatisticas)
        else:
            self.ids.box_estatisticas.clear_widgets()
            self.ids.box_estatisticas.cols = 1
            geral_estatisticas = Label(
                text=f"""O Stand Motorizas da Ualg realizou um total de\n {response[0]} vendas desde o ínicio.\n
                                Foram vendidas {response[1]} motos \n e o valor total faturado foi {response[2]}€""",
                halign='center',
                valign='middle', font_size='30dp', bold=True)
            self.ids.box_estatisticas.add_widget(geral_estatisticas)

    def mostrar_geral(self):
        response = check_general_statistics()
        if response["message"] and response["estatisticas"] != None:
            estatisticas = response["estatisticas"]
            self.adicionar_estatisticas_geral(estatisticas)

    def atras(self):
        if GLOBAL_VARIABLES.USER_IS_MASTER:
            self.manager.current = 'paginainicialmaster'
        else:
            self.manager.current = 'paginainicialnormal'
