# [Librerias
import requests
import random
import redis
import json
import time
import matplotlib.pyplot as plt
# Librerias]

# Inicio de tiempo
Itime = time.time()

# [Se crean las instancias del docker redis, con puertos personalizados y a nivel local
r1 = redis.Redis(host='localhost', port=6381, decode_responses=True)
r2 = redis.Redis(host='localhost', port=6382, decode_responses=True)
r3 = redis.Redis(host='localhost', port=6383, decode_responses=True)
# Se crean las instancias del docker redis, con puertos personalizados y a nivel local]

# [Leer los códigos de barras del archivo de texto codigos.txt
with open("codigos.txt", "r") as f:
    barcodes = [line.strip() for line in f.readlines()]
# Leer los códigos de barras del archivo de texto codigos.txt]

# Los 5 primeros códigos de barras son más populares, por lo que tienen una mayor probabilidad de ser elegidos
popular_barcodes = barcodes[:5]

# [Seleccionar 5 códigos de barras aleatorios de la lista, dando prioridad a los códigos populares
random_barcodes = random.choices(popular_barcodes, weights=[0.3, 0.3, 0.2, 0.1, 0.1], k=5) + \
                 random.sample(barcodes[5:], k=5)
# Seleccionar 5 códigos de barras aleatorios de la lista, dando prioridad a los códigos populares]

# Recorre todos los codigos de barra dentro del arreglo de random_barcodes
for barcode in random_barcodes:
    # [Comprueba primeramente la existencia de los codigos dentro de los servidores de redis
    if r1.exists(barcode) == 1:
        print(barcode)
        print(r1.get(barcode))

    elif r2.exists(barcode) == 1:
        print(barcode)
        print(r2.get(barcode))

    elif r3.exists(barcode) == 1:
        print(barcode)
        print(r3.get(barcode))
    # Comprueba primeramente la existencia de los codigos dentro de los servidores de redis]
    
    # [En caso de no existir dentro de los servidores, procede a hacer la consulta dentro de la API
    else:
        # [Variables de consulta
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(url)
        # Variables de consulta]

        # Comprueba si existe el producto dentro de la API
        if response.status_code == 200:
            # Guarda la información de la consulta dentro de la variable data en formato json
            data = response.json()
            if "product" in data:
                product = data["product"]
                name = product.get("product_name", "unknown")
                brand = product.get("brands", "unknown")
                quantity = product.get("quantity", "unknown")
                category = product.get("categories", "unknown")
                ingredients = product.get("ingredients_text", "unknown")

                print("product name:", name)
                print("brand:", brand)
                print("quantity:", quantity)
                print("category:", category)
                print("ingredients:", ingredients)
                print("=" * 50)

                # [Convertir el resultado a un diccionario y almacenarlo en redis
                result = {
                    "product_name": name,
                    "brand": brand,
                    "quantity": quantity,
                    "category": category,
                    "ingredients": ingredients
                }
                # Convertir el resultado a un diccionario y almacenarlo en redis]

                # Convertir a string en formato json
                result_json = json.dumps(result)  
                
                # [Aqui se distribuye los codigos de barra entre los tres codigos de redis en funcion
                # de aplicarle módulo 3 de cada código de barra para que sea de manera equitativa
                if int(barcode[-1]) % 3 == 0:
                    r1.set(barcode, result_json)
                elif int(barcode[-1]) % 3 == 1:
                    r2.set(barcode, result_json)
                else:
                    r3.set(barcode, result_json)
                # Aqui se distribuye los codigos de barra entre los tres codigos de redis en funcion
                # de aplicarle módulo 3 de cada código de barra para que sea de manera equitativa]
            
            # En caso de no encontrar el producto:
            else:
                print(f"product not found for barcode: {barcode}")
        # En caso de conectar con la API
        else:
            print(f"Error making request for barcode: {barcode}, error code: {response.status_code}")
    # En caso de no existir dentro de los servidores, procede a hacer la consulta dentro de la API]

# Final de tiempo
Ftime = time.time()

# [Tiempo total y su impresión
Ttotal = Ftime-Itime
print("Tiempo total: ", Ttotal)
# Tiempo total y su impresión]

# [Escritura dentro del archivo tiempos.txt todos los tiempos que va tomando a medida que se
# ejecuta el código
f = open ('tiempos.txt','a')
f.write(str(Ttotal))
f.write("\n")
f.close()
# Escritura dentro del archivo tiempos.txt todos los tiempos que va tomando a medida que se
# ejecuta el código]
