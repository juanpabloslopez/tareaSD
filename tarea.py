import requests
import random
import redis
import json

r1 = redis.Redis(host='localhost', port=6381, decode_responses=True)
r2 = redis.Redis(host='localhost', port=6382, decode_responses=True)
r3 = redis.Redis(host='localhost', port=6383, decode_responses=True)

# Leer los códigos de barras del archivo de texto codigos.txt
with open("codigos.txt", "r") as f:
    barcodes = [line.strip() for line in f.readlines()]

# Los 5 primeros códigos de barras son más populares, por lo que tienen una mayor probabilidad de ser elegidos
popular_barcodes = barcodes[:5]

# Seleccionar 5 códigos de barras aleatorios de la lista, dando prioridad a los códigos populares
random_barcodes = random.choices(popular_barcodes, weights=[0.3, 0.3, 0.2, 0.1, 0.1], k=5) + \
                 random.sample(barcodes[5:], k=5)

# Hacer una solicitud GET para cada uno de los códigos de barras seleccionados aleatoriamente
for barcode in random_barcodes:

    if r1.exists(barcode) == 1:
        print(barcode)
        print(r1.get(barcode))

    elif r2.exists(barcode) == 1:
        print(barcode)
        print(r2.get(barcode))

    elif r3.exists(barcode) == 1:
        print(barcode)
        print(r3.get(barcode))

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "product" in data:
            product = data["product"]
            name = product.get("product_name", "Unknown")
            brand = product.get("brands", "Unknown")
            quantity = product.get("quantity", "Unknown")
            category = product.get("categories", "Unknown")
            ingredients = product.get("ingredients_text", "Unknown")

            print("Product Name:", name)
            print("Brand:", brand)
            print("Quantity:", quantity)
            print("Category:", category)
            print("Ingredients:", ingredients)
            print("=" * 50)

            # Convertir el resultado a un diccionario y almacenarlo en Redis
            result = {
                "product_name": name,
                "brand": brand,
                "quantity": quantity,
                "category": category,
                "ingredients": ingredients
            }
            result_json = json.dumps(result)  # Convertir a string en formato JSON
            if int(barcode[-1]) % 3 == 0:
                r1.set(barcode, result_json)
            elif int(barcode[-1]) % 3 == 1:
                r2.set(barcode, result_json)
            else:
                r3.set(barcode, result_json)

        else:
            print(f"Product not found for barcode: {barcode}")
    else:
        print(f"Error making request for barcode: {barcode}, error code: {response.status_code}")

