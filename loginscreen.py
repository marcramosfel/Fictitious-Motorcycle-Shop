from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from utils_web_service import check_login
from kivy.uix.popup import Popup
import GLOBAL_VARIABLES


class LoginScreen(Screen):
    def valida(self):
        try:
            print(GLOBAL_VARIABLES.USER_IS_MASTER)
            print(self.ids.utilizador.text, self.ids.password.text)
            response = check_login(self.ids.utilizador.text, self.ids.password.text)
            print(response)
            if response['message'] == 'success':
                GLOBAL_VARIABLES.USER_NAME = response["name"]
                GLOBAL_VARIABLES.USER_PASSWORD = response["password"]
                GLOBAL_VARIABLES.USER_PHONE = response["telefone"]
                GLOBAL_VARIABLES.USER_EMAIL = response["email"]
                GLOBAL_VARIABLES.USER_ID = response["id_account"]
                print("ok")
                GLOBAL_VARIABLES.USER_EMAIL = self.ids.utilizador.text
                if response['is_master'] == 1:
                    GLOBAL_VARIABLES.USER_IS_MASTER = 1
                    self.manager.current = "paginainicialmaster"
                else:
                    GLOBAL_VARIABLES.USER_IS_MASTER = 0
                    self.manager.current = "paginainicialnormal"
                print(GLOBAL_VARIABLES.USER_EMAIL, GLOBAL_VARIABLES.USER_IS_MASTER)
            elif response['message'] == "password_incorrect":
                self.show_popup("Password errada")
                print("Falhou: password incorreta")
            else:
                self.show_popup("Falhou: utilizador não existe")
                print('Falhou: utilizador não existe')
        except:
            self.show_popup("Falhou: utilizador não existe")
            print('Falhou: utilizador não existe')

    def registra(self):
        self.manager.current = 'registrar'

    def vai_para_motorizadas(self):
        self.manager.current = 'motorizadas'

    def change_visible_password(self):
        if self.ids.password.password:
            self.ids.password.password = False
            self.ids.eye.background_normal = 'images/eye2.png'
        else:
            self.ids.password.password = True
            self.ids.eye.background_normal = 'images/eye.png'

    def show_popup(self, anchor):
        show = PopEmail(text=anchor)
        popupwindow = Popup(title="Erro", content=show, size_hint=(None, None),
                            size=(400, 125), background_color=(0.9, 0.3, 0.1, 1))
        popupwindow.open()


class PopEmail(Label):
    pass
