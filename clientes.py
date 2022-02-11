import requests
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

import GLOBAL_VARIABLES
from utils_web_service import atualiza_utilizador, check_login_by_id


# sm.add_widget(ClienteMaster(name="clientesmaster"))


class ClienteMaster(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label_email1 = Label(text='Email')
        self.label_nif1 = Label(text='NIF')
        self.label_telefone1 = Label(text='Telefone')
        self.label_nome1 = Label(text='Nome')
        self.label_id1 = Label(text='ID')
        self.erro = Label(text='Cliente não existe!')

        self.uri = 'http://127.0.0.1:5000/cliente'

    def ver_todos_clientes(self):
        response = requests.get(self.uri)
        resultado = response.json()['cliente']
        print(resultado)

        if self.ids.grid_informacao.cols == 0:
            self.ids.grid_informacao.cols = 5
            # self.ids.grid_informacao.size_hint = (1, 1)
            for widget in (self.label_id1, self.label_nome1, self.label_telefone1, self.label_nif1, self.label_email1):
                self.ids.grid_informacao.add_widget(widget)

            for i in range(len(resultado)):
                botao_id = Button()
                botao_id.bind(on_release=self.mostra)
                label_nome = Label()
                label_telefone = Label()
                label_nif = Label()
                label_email = Label(font_size="15dp")
                botao_id.text = str(resultado[i]['idcliente'])
                label_nome.text = resultado[i]['nome']
                label_telefone.text = str(resultado[i]['telefone'])
                label_nif.text = str(resultado[i]['nif'])
                label_email.text = resultado[i]['email']
                for widget in (botao_id, label_nome, label_telefone, label_nif, label_email):
                    self.ids.grid_informacao.add_widget(widget)
        else:
            self.ids.grid_informacao.clear_widgets()
            self.ids.grid_informacao.size_hint = (None, None)
            self.ids.grid_informacao.cols = 0
            self.ids.grid_informacao.padding = 20
            self.ids.grid_informacao.spacing = 5

    def mostra(self, instance):
        self.ids.grid_informacao.clear_widgets()
        self.ids.grid_informacao.cols = 4
        id_cliente = instance.text
        print('botao pressionado', instance)
        response = requests.get(self.uri + f'/{id_cliente}').json()  # uso o json para transformar em dicionario!
        if response['message'] == 'Everything went well!':
            resultado = response['cliente']
            print(type(resultado), resultado)
            self.ids.grid_informacao.size_hint = (1, 1)
            self.ids.grid_informacao.cols = 5

            for widget in (self.label_id1, self.label_nome1, self.label_telefone1, self.label_nif1, self.label_email1):
                self.ids.grid_informacao.add_widget(widget)

            botao_id = Button(text=str(resultado['idcliente']))
            label_nome = Label(text=resultado['nome'])
            label_telefone = Label(text=str(resultado['telefone']))
            label_nif = Label(text=str(resultado['nif']))
            label_email = Label(text=(resultado['email']))
            for widget in (botao_id, label_nome, label_telefone, label_nif, label_email):
                self.ids.grid_informacao.add_widget(widget)
        else:
            self.ids.grid_informacao.clear_widgets()
            self.ids.grid_informacao.cols = 1
            self.ids.grid_informacao.add_widget(self.erro)
            self.ids.clientes_sem_widget.size_hint = 1, 1

    def ver_cliente_especifico(self):
        if self.ids.grid_informacao.cols == 0:
            input_informacao = Label(text='Insira o numero do cliente a pesquisar')
            id_input = TextInput(multiline=False, text="")

            self.ids.grid_informacao.size = (self.width, 200)
            self.ids.grid_informacao.cols = 2

            id_input.bind(on_text_validate=self.on_press_enter)

            self.ids.grid_informacao.add_widget(input_informacao)
            self.ids.grid_informacao.add_widget(id_input)
        else:
            self.ids.grid_informacao.clear_widgets()
            # self.ids.grid_informacao.size_hint = (0.2, 0.2)
            self.ids.grid_informacao.cols = 0

    def on_press_enter(self, instance):
        print('User pressed enter in', instance)
        id_cliente = instance.text

        response = requests.get(self.uri + f'/{id_cliente}').json()  # uso o json para transformar em dicionario!
        if response['message'] == 'Everything went well!':
            resultado = response['cliente']
            print(type(resultado), resultado)

            self.ids.grid_informacao.clear_widgets()

            self.ids.grid_informacao.size_hint = (1, 1)
            self.ids.grid_informacao.cols = 5

            for widget in (self.label_id1, self.label_nome1, self.label_telefone1, self.label_nif1, self.label_email1):
                self.ids.grid_informacao.add_widget(widget)

            self.botao_id = Button(text=str(resultado['idcliente']))
            label_nome = Label(text=resultado['nome'])
            label_telefone = Label(text=str(resultado['telefone']))
            label_nif = Label(text=str(resultado['nif']))
            label_email = Label(text=(resultado['email']))
            self.ids.grid_informacao.add_widget(self.botao_id)
            self.ids.grid_informacao.add_widget(label_nome)
            self.ids.grid_informacao.add_widget(label_telefone)
            self.ids.grid_informacao.add_widget(label_nif)
            self.ids.grid_informacao.add_widget(label_email)
        else:
            self.ids.grid_informacao.clear_widgets()
            self.ids.grid_informacao.cols = 1
            self.ids.grid_informacao.add_widget(self.erro)

    def atras(self):
        if GLOBAL_VARIABLES.USER_IS_MASTER:
            self.manager.current = 'paginainicialmaster'
        else:
            self.manager.current = 'paginainicialnormal'

    def inserir_novo_cliente(self):
        self.manager.current = 'registrarmaster'


    def alterar_dados_cliente(self, response):
        print(response)

        GLOBAL_VARIABLES.USER_NAME = response['nome']
        GLOBAL_VARIABLES.USER_EMAIL = response['email']
        GLOBAL_VARIABLES.USER_PASSWORD = response['password']
        GLOBAL_VARIABLES.USER_IS_MASTER = response['ismaster']
        GLOBAL_VARIABLES.USER_PHONE = response['telefone']
        self.manager.current = 'clientesnormal'

    def on_click_name(self, instance):
        value = str(instance.text)
        print(value)
        value = value.replace(' ', '%20')
        print(value)
        response = requests.get(self.uri + f'/"{value}"').json()  # uso o json para transformar em dicionario!
        if response['message'] == 'Everything went well!':
            response = response["cliente"]
            self.alterar_dados_cliente(response)
            self.popup_cliente.dismiss()
        else:
            print("não é possivel realizar!")

    def alterar_dados(self):
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


# sm.add_widget(ClienteNormal(name="clientesnormal"))
class ClienteNormal(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.codigo_master = '000'

        self.show = PopEmail()
        self.popupWindow = Popup(title="Erro", content=self.show, size_hint=(None, None),
                                 size=(400, 125), background_color=(0.9, 0.3, 0.1, 1))

        self.ids.check_master_cliente.bind(active=self.on_checkbox_active)

    def carregar(self):
        self.ids.nome_cliente.text = GLOBAL_VARIABLES.USER_NAME
        self.ids.email_cliente.text = GLOBAL_VARIABLES.USER_EMAIL
        self.ids.password_cliente.text = GLOBAL_VARIABLES.USER_PASSWORD
        self.ids.check_master_cliente.active = GLOBAL_VARIABLES.USER_IS_MASTER
        self.ids.telefone_cliente.text = GLOBAL_VARIABLES.USER_PHONE
        self.ids.confirmar_password_cliente.text = GLOBAL_VARIABLES.USER_PASSWORD

    def on_checkbox_active(self, checkbox, value):
        if value:
            print(self.ids.check_master_cliente.active)
            print('The checkbox', checkbox, 'is active', value)
            self.ids.codigomaster.disabled = False
        else:
            print(self.ids.check_master_cliente.active)
            self.ids.codigomaster.disabled = True
            print('The checkbox', checkbox, 'is inactive', value)

    def salvar(self):
        if self.ids.check_master_cliente.active:
            if self.ids.codigomaster.text == self.codigo_master:
                self.mostrar_popup()
            else:
                self.show.text = 'Código Master Errado'
                self.show.color = (1, 0, 0, 1)
                self.popupWindow.title = "Erro"
                self.popupWindow.background_color = (0.9, 0.3, 0.1, 1)
                self.show_popup()
        else:
            self.mostrar_popup()

    def mostrar_popup(self):
        print(GLOBAL_VARIABLES.USER_ID, GLOBAL_VARIABLES.USER_NAME)
        value = GLOBAL_VARIABLES.USER_NAME.replace(' ', '%20')
        resposta = requests.get(GLOBAL_VARIABLES.WEB_SERVICE_URI + f'cliente/"{value}"').json()
        print(resposta)
        idaccount = resposta['cliente']['idcliente']
        # idaccount = 1
        nome = self.ids.nome_cliente.text
        email = self.ids.email_cliente.text
        password = self.ids.password_cliente.text
        telefone = self.ids.telefone_cliente.text
        if telefone == '':
            telefone = 'Null'
        print(idaccount, type(nome), email, password, telefone, self.ids.check_master_cliente.active)
        if nome != '':
            if self.ids.password_cliente.text == self.ids.confirmar_password_cliente.text:
                response = atualiza_utilizador(idaccount, nome, password, email, self.ids.check_master_cliente.active, telefone)
                if response == 'Os dados do utilizador foram atualiazados!':
                    self.show.text = "Os dados do utilizador foram atualiazados!"
                    self.show.color = (0, 0, 1, 1)
                    self.popupWindow.title = "Sucesso"
                    self.popupWindow.background_color = (0.1, 0.3, 0.9, 1)
                    self.show_popup()
                    self.manager.current = 'login'
                elif response == 'O email não é válido!!':
                    self.show.text = "O email não é válido!!'"
                    self.show.color = (1, 0, 0, 1)
                    self.popupWindow.title = "Erro"
                    self.popupWindow.background_color = (0.9, 0.3, 0.1, 1)
                    self.show_popup()

            else:
                self.show.text = 'Passwords Incompativeis'
                self.show.color = (1, 0, 0, 1)
                self.popupWindow.title = "Erro"
                self.popupWindow.background_color = (0.9, 0.3, 0.1, 1)
                self.show_popup()
        else:
            self.show.text = 'Digite o seu novo nome'
            self.show.color = (1, 0, 0, 1)
            self.popupWindow.title = "Erro"
            self.popupWindow.background_color = (0.9, 0.3, 0.1, 1)
            self.show_popup()

    def atras(self):
        print(GLOBAL_VARIABLES.USER_ID)
        response = check_login_by_id(GLOBAL_VARIABLES.USER_ID)
        print(response)
        if response['message'] == 'success':
            GLOBAL_VARIABLES.USER_NAME = response["name"]
            GLOBAL_VARIABLES.USER_PASSWORD = response["password"]
            GLOBAL_VARIABLES.USER_PHONE = response["telefone"]
            GLOBAL_VARIABLES.USER_EMAIL = response["email"]
            GLOBAL_VARIABLES.USER_ID = response["id_account"]
            GLOBAL_VARIABLES.USER_IS_MASTER = response["is_master"]
        if GLOBAL_VARIABLES.USER_IS_MASTER:
            self.manager.current = 'paginainicialmaster'
        else:
            self.manager.current = 'paginainicialnormal'

    def show_popup(self):
        self.popupWindow.open()


class PopEmail(Label):
    pass
