import bs4
import urllib.request

def download_html(url):
    req = urllib.request.Request(url=url, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    handler = urllib.request.urlopen(req)
    return handler.read().decode()

# def get_hip_hop():
#     soup = bs4.BeautifulSoup(download_html(f'https://concert.ua/uk/catalog/kyiv/all-categories/style=hip-hop'), features="html5lib")
#     print(soup.find(class_="event-info__name").get_text())
#
# get_hip_hop()

def get_steam_nickname(steam_name):
    soup = bs4.BeautifulSoup(download_html(f'https://steamcommunity.com/id/{steam_name}'), features="html5lib")
    print(soup.find(class_="actual_persona_name").get_text())

get_steam_nickname('asdfuji')
