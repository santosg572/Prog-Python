import requests
from bs4 import BeautifulSoup
url = 'https://en.wikipedia.org/w/index.php' + \
 '?title=List_of_Game_of_Thrones_episodes&oldid=802553687'
r = requests.get(url)
html_contents = r.text
html_soup = BeautifulSoup(html_contents, features="lxml")

for found in html_soup.find_all(['h1', 'h2']):
   print(found)



