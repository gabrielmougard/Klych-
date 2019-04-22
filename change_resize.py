import requests
import sys
password = 'leubzezeh97869UYVD'
url = 'https://home.plawn-inc.science/face/set_resize'

r = requests.post(url, data={'password':password, 'using_resize':sys.argv[1]})
print(r)
print(r.text)