import requests

class Motorizadas_API:
    uri = "http://127.0.0.1:5000/"

    @classmethod
    def lista_todas_motorizadas(cls):
        response = requests.get(cls.uri+"/motorizadas")
        return response.json()


