from flask import Flask
import requests

app = Flask(__name__)

# Pipedrive API info
API_TOKEN = "7f1dec3f4a486b427cedac03293c65053def753b"
API_URL = "https://api.pipedrive.com/v1"

def pipedrive_workflow():
    # Meklē klientu pēc e-pasta
    email = "raivis.zvejnieks@gmail.com"
    search_person = requests.get(f"{API_URL}/persons/search", params={
        "term": email,
        "fields": "email",
        "api_token": API_TOKEN
    }).json()

    if search_person['data'] and search_person['data']['items']:
        person = min(search_person['data']['items'], key=lambda x: x['item']['id'])
        person_id = person['item']['id']
        print(f"Klients atrasts ar ID: {person_id}")
    else:
        print("Klients nav atrasts!")
        return

    # Ģenerē dinamiski jaunu deal nosaukumu testsXX
    i = 1
    while True:
        deal_name = f"tests{str(i).zfill(2)}"
        deal_check = requests.get(f"{API_URL}/deals/search", params={
            "term": deal_name,
            "api_token": API_TOKEN
        }).json()
        if not deal_check['data'] or deal_check['data']['items'] == []:
            break
        i += 1

    # Izveido deal
    create_deal = requests.post(f"{API_URL}/deals", params={"api_token": API_TOKEN}, json={
        "title": deal_name,
        "person_id": person_id
    }).json()
    deal_id = create_deal['data']['id']
    print(f"Deal izveidots ar ID: {deal_id}")

    # Meklē produktu pēc produkta koda
    product_code = "testa11"
    product_search = requests.get(f"{API_URL}/products/search", params={
        "term": product_code,
        "fields": "code",
        "api_token": API_TOKEN
    }).json()
    if product_search['data'] and product_search['data']['items']:
        product_id = product_search['data']['items'][0]['item']['id']
        print(f"Produkts atrasts ar ID: {product_id}")
    else:
        print("Produkts nav atrasts!")
        return

    # Pievieno produktu darījumam
    add_product = requests.post(f"{API_URL}/deals/{deal_id}/products", params={"api_token": API_TOKEN}, json={
        "product_id": product_id,
        "item_price": 2.00,
        "quantity": 1
    }).json()
    print(f"Produkts pievienots darījumam: {add_product}")

@app.route("/")
def trigger_job():
    pipedrive_workflow()
    return "Pipedrive process completed!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
