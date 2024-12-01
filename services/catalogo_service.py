import requests
from tenacity import retry, stop_after_attempt, wait_random
from flask import current_app

class CatalogoService:
    
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def obtener_producto(self, id):
        producto = requests.get(current_app.config['CATALOGO_URL'] + f'{id}')
        return producto