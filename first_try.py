import requests

barcode = "5449000000996"
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
    else:
        print("Product not found")
else:
    print("Error making request: ", response.status_code)
