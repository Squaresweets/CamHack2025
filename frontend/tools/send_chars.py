import requests
import time
import random

BASE_URL = "http://127.0.0.1:5000/newchar"  # change if Flask runs elsewhere
CHARS = list("ABCDEFGHIJK]")  # the characters to send

def send_random_char():
    char = random.choice(CHARS)
    url = f"{BASE_URL}/{char}"
    try:
        res = requests.get(url)
        if res.ok:
            print(f"Sent char: {char}")
        else:
            print(f"Failed to send {char}: {res.status_code}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    print("Starting character sender...")
    while True:
        send_random_char()
        time.sleep(0.5)  # send every 3 seconds
