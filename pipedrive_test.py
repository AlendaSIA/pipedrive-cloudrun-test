import requests

API_TOKEN = "7f1dec3f4a486b427cedac03293c65053def753b"
BASE_URL = "https://api.pipedrive.com/v1"

# Meklē klientu pēc e-pasta
email = "raivis.zvejnieks@gmail.com"
person_resp = requests.get(f"{BASE_URL}/persons/search", params={"term": email, "api_token": API_TOKEN})
person_data = person_resp.json()

if person_data.get("data") and person_data["data"].get("items"):
    # Izvēlamies vecāko (ar mazāko ID)
    sorted_persons = sorted(person_data["data"]["items"], key=lambda x: x["item"]["id"])
    person_id = sorted_persons[0]["item"]["id"]
    print(f"Klients atrasts ar ID: {person_id}")

    # Pārbaudām vai jau eksistē deals ar nosaukumu "tests" un pievienojam ciparu, ja vajag
    base_title = "tests"
    deal_title = base_title
    index = 1

    while True:
        deal_check = requests.get(f"{BASE_URL}/deals/search", params={"term": deal_title, "api_token": API_TOKEN})
        deal_check_data = deal_check.json()
        if deal_check_data.get("data") and deal_check_data["data"].get("items"):
            index += 1
            deal_title = f"{base_title}{index:02}"
        else:
            break

    # Izveidojam deal
    deal_resp = requests.post(f"{BASE_URL}/deals", params={"api_token": API_TOKEN}, json={
        "title": deal_title,
        "person_id": person_id,
        "value": 2.00,
        "currency": "EUR"
    })
    deal_data = deal_resp.json()
    deal_id = deal_data["data"]["id"]
    print(f"Deal izveidots ar ID: {deal_id} un nosaukumu: {deal_title}")

    # Meklējam produktu pēc produkta koda
    product_code = "testa11"
    prod_resp = requests.get(f"{BASE_URL}/products/search", params={"term": product_code, "api_token": API_TOKEN})
    prod_data = prod_resp.json()

    if prod_data.get("data") and prod_data["data"].get("items"):
        product_id = prod_data["data"]["items"][0]["item"]["id"]
        print(f"Produkts atrasts ar ID: {product_id}")

        # Pievienojam produktu dealam
        add_prod_resp = requests.post(f"{BASE_URL}/deals/{deal_id}/products", params={"api_token": API_TOKEN}, json={
            "product_id": product_id,
            "item_price": 2.00,
            "quantity": 1,
            "discount": 0,
            "tax": 0
        })
        print("Produkts pievienots darījumam:", add_prod_resp.json())
    else:
        print("Produkts netika atrasts!")
else:
    print("Klients netika atrasts!")

