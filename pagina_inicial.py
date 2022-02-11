from kivy.uix.screenmanager import Screen
import GLOBAL_VARIABLES
from compras import *


class PaginaInicialMaster(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def vai_para_clientes(self):
        self.manager.current = 'clientesmaster'

    def vai_para_motorizadas(self):
        self.manager.current = 'motorizadas'

    def vai_para_compras_master(self):
        self.manager.current = 'comprasmaster'

    def vai_para_estatisticas(self):
        self.manager.current = 'estatisticas'

    def logout(self):
        self.manager.current = 'login'
        # USER ID
        GLOBAL_VARIABLES.USER_ID = None
        # USER EMAIL
        GLOBAL_VARIABLES.USER_EMAIL = None
        # USER NAME
        GLOBAL_VARIABLES.USER_NAME = None
        # USER PASSWORD
        GLOBAL_VARIABLES.USER_PASSWORD = None
        # USER PHONE
        GLOBAL_VARIABLES.USER_PHONE = None
        # USER IS MASTER 1 TRUE, 0 FALSE
        GLOBAL_VARIABLES.USER_IS_MASTER = False


class PaginaInicialNormal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def editar_dados_proprios(self):
        self.manager.current = 'clientesnormal'

    def vai_para_motorizadas(self):
        self.manager.current = 'motorizadas'

    def ver_proprias_compras(self):
        self.manager.current = 'propriascompras'
        # ComprasNormal.mostra_compras()



    def logout(self):
        self.manager.current = 'login'
        # USER ID
        GLOBAL_VARIABLES.USER_ID = None
        # USER EMAIL
        GLOBAL_VARIABLES.USER_EMAIL = None
        # USER NAME
        GLOBAL_VARIABLES.USER_NAME = None
        # USER PASSWORD
        GLOBAL_VARIABLES.USER_PASSWORD = None
        # USER PHONE
        GLOBAL_VARIABLES.USER_PHONE = None
        # USER IS MASTER 1 TRUE, 0 FALSE
        GLOBAL_VARIABLES.USER_IS_MASTER = False

    def vai_para_compras_normal(self):
        self.manager.current = 'comprasnormal'