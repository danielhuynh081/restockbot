import requests
import os
import json

STATE_FILE = "state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"bought": False}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def send_discord_message(hook, msg):
    payload = {"content": msg}
    requests.post(hook, json=payload)

def purchase(hook):
    # Placeholder for your purchase logic
    send_discord_message(hook, "Purchasing the item...")
    # buying logic



def ippodo():
    url = "https://ippodotea.com/products/sayaka-no-mukashi.js"
    ippodo_channel = "https://discord.com/api/webhooks/1404587748727328779/moIUDkcxMnA9HYTZT0KOW-w18-YIjgq5lY1j5fiOnNUX1Qxxtevk18MCn99YWjnJQwlt"
    
    state = load_state()
    
    if state.get("bought"):
        send_discord_message(ippodo_channel, "Already bought. Skipping restock check. @everyone")
        return
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve data from the API.")
        return

    data = response.json()
    variants = data.get('variants', [])

    for variant in variants:
        inventory = variant.get("inventory_quantity", 0)
        if inventory > 0:
            send_discord_message(ippodo_channel, "Ippodo Restock! @everyone")
            purchase(ippodo_channel)  # Call the purchase placeholder function
            state["bought"] = True
            save_state(state)
            break  # Stop after successful purchase
        else:
            print(f"Sakaya no Mukashi is not available. Inventory: {inventory}")

def main():
    ippodo()

if __name__ == "__main__":
    main()
