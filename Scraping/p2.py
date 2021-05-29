import requests
url = 'https://en.wikipedia.org/wiki/?query= r lenguage'
r = requests.get(url)
print(r.text)

