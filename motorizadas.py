import GLOBAL_VARIABLES
import requests
import json

from utils import find_child_by_name

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from Motorizadas_API import Motorizadas_API
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput

class Search(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_text_validate=self.search)

    def search_web_service(instance,text):
        response = requests.post(GLOBAL_VARIABLES.WEB_SERVICE_URI+"search_motos", json={"search":text})
        return json.loads(response.text)

    def search(instance,value):
        for i in instance.parent.parent.children:
            try:
                if i.name == 'gridLayout_list':
                    for o in i.children:
                        try:
                            if o.name == 'scroll':
                                o.children[0].clear_widgets()
                                for p in instance.search_web_service(value.text):
                                    row = Row(p[0],cols=7, size_hint = (1, None), size = ('200dp','50dp'))
                                    for q in p:
                                        row.add_widget(Label(text=str(q)))
                                    o.children[0].add_widget(row)
                        except:
                            pass
            except:
                pass


class ImageMoto(AsyncImage):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.source=GLOBAL_VARIABLES.WEB_SERVICE_URI+'static/images/17.png'
        self.name= "image_moto"


class Row(ButtonBehavior,GridLayout):
    def __init__(self, id,**kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.select)
        self.id = id

    def select(instance, value):
        for i in instance.parent.children:
            for o in i.children:
                o.color = (1,1,1,1)
        for i in instance.children:
            i.color = (0.4,0.9,0.1,1)

        find_child_by_name(instance.parent.parent.parent, "image_moto").source = GLOBAL_VARIABLES.WEB_SERVICE_URI+"static/images/"+str(instance.id)+".png"




class StackLayoutTable(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        response = Motorizadas_API.lista_todas_motorizadas()
        for num,i in enumerate(response):
            table = Row(i[0],cols=7, size_hint = (1, None), size = ('200dp','50dp'))
            for value in i:
                table.add_widget(Label(text=str(value)))
            self.add_widget(table)

class Motorizadas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self):
        search_widget = find_child_by_name(self,'search')
        search_widget.search(value=search_widget)
    def atras(self):
        self.manager.current = 'paginainicial'



