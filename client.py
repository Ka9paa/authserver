import requests

API_URL = "http://127.0.0.1:5000/api/generate"  # change to your Render URL if deployed
AUTH_HEADER = "d4c1195eb55ef46a58fdf440b17af44625e5be0d9efb43fb11f3fa6133eac72f"

def request_license_key():
    headers = {
        "Authorization": AUTH_HEADER
    }

    try:
        response = requests.post(API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            key = data.get("key")
            print(f"🔑 License key received: {key}")
        else:
            print(f"❌ Failed to generate key. Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    request_license_key()
