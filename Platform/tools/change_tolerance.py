import requests
import sys
password = 'leubzezeh97869UYVD'

url = 'https://home.plawn-inc.science/face/ch_tolerance'

r = requests.post(url, data={'password':password, 'tolerance':float(sys.argv[1])})

print(r)
print(r.text)