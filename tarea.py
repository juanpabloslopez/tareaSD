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
#ciudades = ['Madrid', 'Londres', 'Los Angeles,US','Santiago,CL','Florencia,it','Berlin,DE','Tokio,jp','Roma,it','Paris,fr','Lima,pe','Buenos Aires,ar','Sao Paulo,br','Mexico,mx','Toronto,ca','Sydney,au','Hong Kong,hk','Dubai,ae','Moscu,ru','Seul,kr','Singapur,sg','Bangkok,th','Taipei,tw','Jakarta,id','Pekin,cn','Shanghai,cn','Delhi,in','Mumbai,in','Kolkata,in','Karachi,pk','Istambul,tr','Riyadh,sa','Cairo,eg','Johannesburgo,za','Lagos,ng','Kinshasa,cd','Lima,pe','Buenos Aires,ar','Sao Paulo,br','Mexico,mx','Toronto,ca','Sydney,au','Hong Kong,hk','Dubai,ae','Moscu,ru','Seul,kr','Singapur,sg','Bangkok,th','Taipei,tw','Jakarta,id','Pekin,cn','Shanghai,cn','Delhi,in','Mumbai,in','Kolkata,in','Karachi,pk','Istambul,tr','Riyadh,sa','Cairo,eg','Johannesburgo,za','Lagos,ng','Kinshasa,cd']
ciudades = ['Madrid', 'Londres', 'Los Angeles,US','Santiago,CL','Florencia,IT','Berlin,DE','Salt Lake County, US']
resultados = buscar_clima_distribuido(ciudades)

# Imprimimos los resultados
for ciudad, datos_clima in resultados.items():
    print(f'Clima en {ciudad}:')
    print('Temperatura:', datos_clima['main']['temp'],'K')
    print('Temperatura:', round(datos_clima['main']['temp']-273.15, 2),'ºC')
    print('Descripción:', datos_clima['weather'][0]['description'])
    print('Humedad:', datos_clima['main']['humidity'],'%')
    print('Presión:', datos_clima['main']['pressure'],'hPa')
    print('Viento:', datos_clima['wind']['speed'],'m/s')
    print('País:', datos_clima['sys']['country'])
    print('Coiudad:', datos_clima['name'])


    print('---')

