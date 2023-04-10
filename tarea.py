import requests
from concurrent.futures import ThreadPoolExecutor

# Clave de API de OpenWeather
API_KEY = '2b1fd2d7f77ccf1b7de9b441571b39b8'

# URL base de la API de OpenWeather
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'


def buscar_clima(ciudad):
    """
    Función que realiza la búsqueda del clima en una ciudad dada utilizando la API de OpenWeather.

    :param ciudad: Nombre de la ciudad para la búsqueda del clima.
    :return: Diccionario con los datos del clima de la ciudad.
    """
    parametros = {
        'q': ciudad,
        'appid': API_KEY
    }
    respuesta = requests.get(BASE_URL, params=parametros)
    datos_clima = respuesta.json()
    return datos_clima


def buscar_clima_distribuido(ciudades):
    """
    Función que realiza la búsqueda del clima en varias ciudades de forma distribuida.

    :param ciudades: Lista de nombres de ciudades para la búsqueda del clima.
    :return: Diccionario con los datos del clima de todas las ciudades.
    """
    resultados = {}
    with ThreadPoolExecutor() as executor:
        # Utilizamos un ThreadPoolExecutor para manejar las consultas de múltiples usuarios simultáneamente
        # en hilos separados
        futures = [executor.submit(buscar_clima, ciudad) for ciudad in ciudades]

        # Esperamos a que todas las consultas finalicen y obtenemos los resultados
        for ciudad, futuro in zip(ciudades, futures):
            try:
                datos_clima = futuro.result()
                resultados[ciudad] = datos_clima
            except Exception as e:
                print(f'Error al buscar clima en {ciudad}: {e}')

    return resultados


# Ejemplo de uso
ciudades = ['Madrid', 'Londres', 'Nueva York']
resultados = buscar_clima_distribuido(ciudades)

# Imprimimos los resultados
for ciudad, datos_clima in resultados.items():
    print(f'Clima en {ciudad}:')
    print('Temperatura:', datos_clima['main']['temp'])
    print('Temperatura:', int(datos_clima['main']['temp']-273.15),'ºC')
    print('---')

