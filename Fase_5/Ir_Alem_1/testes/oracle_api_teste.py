import requests
from tabulate import tabulate
import random

# Base URL of the API
BASE_URL = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/"

# Headers to ensure JSON responses
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Function to test GET all records
def test_get_all_records(pretty_print=False):
    print("Testing GET all records...")
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        print("Success! Response:")
        if pretty_print:
            pretty_print_json(response.json())
        else:
            print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
    print("\n")

# Function to test GET a specific record
def test_get_specific_record(record_id):
    print(f"Testing GET record with ID {record_id}...")
    url = f"{BASE_URL}{record_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print("Success! Response:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
    print("\n")

# Function to test POST a new record
def test_post_new_record():
    print("Testing POST a new record...")
    data = {
      "data_leitura": "2025-02-27T13:16:36.333Z",
      "sensor": random.choice(["UMIDADE", "TEMPERATURA", "LUZ"]),
      "valor": round(random.uniform(1, 100), 2)
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=data)
    if response.status_code == 201:
        print("Success! Response:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
    print("\n")

# Function to pretty print JSON
def pretty_print_json(json_data):
    table = []
    for item in json_data['items']:
      table.append([item['id'], item['data_leitura'], item['sensor'], item['valor']])
    print(tabulate(table, headers=["ID", "Data Leitura", "Sensor", "Valor"], tablefmt="pretty"))

# Main function to test all endpoints
def main():
    # Test GET all records
    test_get_all_records()

    # Test GET a specific record (replace 1 with an existing record ID)
    test_get_specific_record(1)

    # Test POST a new record
    test_post_new_record()

    # Test GET all records again to check if the new record was added
    test_get_all_records(pretty_print=True)

if __name__ == "__main__":
    main()
