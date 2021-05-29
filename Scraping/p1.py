import requests
url = 'https://en.wikipedia.org/wiki/R_(programming_language)/'
r = requests.get(url)
print(r.text)

