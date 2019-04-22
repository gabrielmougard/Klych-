import requests
import sys

files = {'file':open(sys.argv[1], 'rb')}
url = 'http://localhost:5001/find'
r = requests.post(url, files=files)

print(r.text)