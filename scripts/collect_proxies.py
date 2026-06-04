import requests
import json
import concurrent.futures

SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
]

def check_proxy(proxy):
    try:
        response = requests.get("https://google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return proxy
    except:
        return None

def update_proxies():
    all_proxies = []
    for source in SOURCES:
        try:
            res = requests.get(source)
            all_proxies.extend(res.text.strip().split('\n'))
        except: continue
    
    print(f"Found {len(all_proxies)} potential proxies. Validating...")
    valid_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_proxy, list(set(all_proxies)))
        valid_proxies = [r for r in results if r]

    with open('configs/proxies.json', 'w') as f:
        json.dump({"active_proxies": valid_proxies}, f)
    print(f"Saved {len(valid_proxies)} active proxies.")

if __name__ == "__main__":
    update_proxies()