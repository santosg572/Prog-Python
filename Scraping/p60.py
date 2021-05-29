import requests
url = 'https://en.wikipedia.org/w/index.php' + \
 '?title=List_of_Game_of_Thrones_episodes&oldid=802553687'
r = requests.get(url)
print(r.text)

