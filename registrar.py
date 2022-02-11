from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
import GLOBAL_VARIABLES
from utils_web_service import coloca_utilizador


class Registrar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.codigo_master = '000'

        self.show = PopEmail()
        self.popupWindow = Popup(title="Erro", content=self.show, size_hint=(None, None),
                                 size=(400, 125), background_color=(1, 0.3, 0.1, 1))

        self.ids.check_master.bind(active=self.on_checkbox_active)

    def inserir_novo_cliente(self):
        if GLOBAL_VARIABLES.USER_IS_MASTER:
            self.manager.current = 'registrar'
        else:
            pass

    def on_checkbox_active(self, checkbox, value):
        if value:
            print(self.ids.check_master.active)
            print('The checkbox', checkbox, 'is active', value)
            self.ids.codigomaster.disabled = False
        else:
            print(self.ids.check_master.active)
            self.ids.codigomaster.disabled = True
            print('The checkbox', checkbox, 'is inactive', value)

    def criar_utilizador(self):
        if self.ids.check_master.active:
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
        nome = self.ids.criar_nome.text
        email = self.ids.criar_email.text
        password = self.ids.criar_password.text
        nif = self.ids.criar_nif.text
        telefone = self.ids.criar_telefone.text

        print(nome, email, password, nif, telefone, self.ids.check_master.active)
        if self.ids.criar_password.text == self.ids.confirmar_password.text:
            response = coloca_utilizador(nome, password, nif, email, self.ids.check_master.active, telefone)
            if nif != '':
                if response == 'Ja existe um nif associado!':
                    self.show.text = 'Ja existe um nif associado'
                    self.show.color = (1, 0, 0, 1)
                    self.popupWindow.title = "Erro"
                    self.popupWindow.background_color = (0.9, 0.3, 0.1, 1)
                    self.show_popup()
                elif response == 'Ja existe um email associado!':
                    self.show.text = 'Ja existe um email associado'
                    self.show.color = (1, 0, 0, 1)
                    self.popupWindow.title = "Erro"
                    self.popupWindow.background_color = (0.9, 0.3, 0.1, 1)
                    self.show_popup()
                elif response == 'O email não é válido!!':
                    self.show.text = 'O email não é válido!!'
                    self.show.color = (1, 0, 0, 1)
                    self.popupWindow.title = "Erro"
                    self.popupWindow.background_color = (0.9, 0.3, 0.1, 1)
                    self.show_popup()
                elif response == 'O utilizador foi criado!!':
                    self.show.text = "O utilizador foi criado!!"
                    self.show.color = (0, 0, 1, 1)
                    self.popupWindow.title = "Sucesso"
                    self.popupWindow.background_color = (0.1, 0.3, 0.9, 1)
                    self.show_popup()
                    if GLOBAL_VARIABLES.USER_IS_MASTER:
                        self.manager.current = "clientesmaster"
                    else:
                        self.manager.current = "login"
            else:
                self.show.text = 'Nif não pode ser nulo!'
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

    def atras(self):
        if self.manager.current == 'registrarmaster':
            self.manager.current = 'clientesmaster'
        else:
            self.manager.current = 'login'

    def show_popup(self):
        self.popupWindow.open()


registrarmaster = Registrar
registrar = Registrar


class PopEmail(Label):
    pass
