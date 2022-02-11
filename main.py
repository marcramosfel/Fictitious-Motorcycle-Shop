from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivymd.app import MDApp

from estatisticas import *
from clientes import *
from loginscreen import LoginScreen
from registrar import *
from pagina_inicial import *
from motorizadas import Motorizadas
from compras import *


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ClienteMaster(name="clientesmaster"))
        sm.add_widget(ClienteNormal(name="clientesnormal"))
        sm.add_widget(registrarmaster(name='registrarmaster'))
        sm.add_widget(registrar(name='registrar'))
        sm.add_widget(PaginaInicialMaster(name='paginainicialmaster'))
        sm.add_widget(PaginaInicialNormal(name='paginainicialnormal'))
        sm.add_widget(Motorizadas(name="motorizadas"))
        sm.add_widget(ComprasMaster(name="comprasmaster"))
        sm.add_widget(ComprasNormal(name="comprasnormal"))
        sm.add_widget(Estatisticas(name="estatisticas"))
        return sm


MainApp().run()
