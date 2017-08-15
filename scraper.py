import requests
from bs4 import BeautifulSoup
import csv
from proxies_scraper import get_proxies, get_user_agents
from time import sleep
from random import choice, uniform
import random
from multiprocessing import Pool


start_urls = ['https://github.com/search?l=Python&p=1&q=location%3A%22Hong+Kong%22+repos%3A%3E4+language%3APython&ref=advsearch&type=Users&utf8=%E2%9C%93',
              'https://github.com/search?l=Python&p=1&q=location%3A%22Singapore%22+repos%3A%3E4+language%3APython&ref=advsearch&type=Users&utf8=%E2%9C%93',
              'https://github.com/search?l=Python&p=1&q=location%3A%22Taiwan%22+repos%3A%3E4+language%3APython&ref=advsearch&type=Users&utf8=%E2%9C%93']



def get_html(url):
    useragents = get_user_agents()
    proxies = get_proxies()
    sleep(uniform(5, 7))
    session_req = requests.session()
    try:
        r = session_req.get(url, headers={'User-Agent': random.choice(useragents)},
                            proxies={'http': 'http://' + random.choice(proxies)}, timeout=10)
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        return None

    return r.text

def get_data(url):
    write_file = open('output2.csv', 'a')
    writer = csv.writer(write_file)
    soup = BeautifulSoup(get_html(url), 'html5lib')
    try: name = soup.find('span', class_ = 'p-name vcard-fullname d-block').text
    except: name = ' '
    try: descr = soup.find('div', class_ = 'p-note user-profile-bio').text
    except: descr = ' '
    profile = url
    try:location = soup.find('li', itemprop = 'homeLocation').find('span', class_ = 'p-label').text
    except: location = ' '

    email = ' '
    try: webs = soup.find('li', itemprop = 'url').find('a').get('href')
    except: webs = ' '
    try: numb_rep = soup.find('div', class_ = 'user-profile-nav js-sticky top-0').findNext('span', class_ = 'Counter').text.strip()
    except: numb_rep = ' '
    #try: stars = soup.find('div', class_ = 'user-profile-nav js-sticky top-0').findNext('span', class_ = '')
    try: contrib = soup.find('div', class_ = 'js-contribution-graph').find('h2').text.strip().split(' ')[0]
    except: contrib = ' '
    langs = []
    try:
        for i in  soup.findAll('p', class_ = 'mb-0 f6 text-gray'):
            langs.append(i.text.strip().split('\n')[0])
    except:
        langs=[]
    lang = ''
    for k in langs:
        k = k.strip()
        lang = lang + k + '/ '

    info_list = [name, descr, profile, location,email, webs, numb_rep, contrib, lang]
    writer.writerow(info_list)

def collect_user_links(page_link):

    soup = BeautifulSoup(get_html(page_link), 'html5lib')
    for i in soup.findAll('div', class_='user-list-info ml-2'):
        for k in i.findAll('a'):
            a = 'https://github.com' + k.get('href')
            with open("user_links.csv", 'a') as ap:
                writer = csv.writer(ap)
                writer.writerow([a])

def collect_page_links(start_urls):
    list_of_links = []
    base1 = start_urls[0].split('p=1')[0]
    base2 = start_urls[0].split('p=1')[1]
    for i in range(1, 22):
        list_of_links.append(base1+'p='+str(i)+base2)
    base1 = start_urls[1].split('p=1')[0]
    base2 = start_urls[1].split('p=1')[1]
    for i in range(1, 46):
        list_of_links.append(base1+'p='+str(i)+base2)
    base1 = start_urls[2].split('p=1')[0]
    base2 = start_urls[2].split('p=1')[1]
    for i in range(1, 53):
        list_of_links.append(base1+'p='+str(i)+base2)
    # for link in list_of_links:
    #     with open('links.csv', 'a') as a:
    #         writer = csv.writer(a)
    #         writer.writerow([link])
    return list_of_links

def main():
    reader = open('user_links.csv', 'r')
    users = []
    for row in reader:
        users.append(row)
    reader.close()
    for i in users[1023:1067]:
        get_data(i.strip())

if __name__ == '__main__':
    main()