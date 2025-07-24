import requests
import re

url = "https://s3.amazonaws.com/capitalbikeshare-data/"
resp = requests.get(url)
print(resp.status_code)
print(resp.text[:500])  # فقط اولش برای دیدن ساختار

matches = re.findall(r"<Key>([^<]+\.zip)</Key>", resp.text)
print("Found ZIPs:", matches)