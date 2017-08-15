from requests.auth import HTTPBasicAuth
import requests
from bs4 import BeautifulSoup


def main():
    try:
        session = requests.session()
        data = {'login':'7zwei',
                'password': '1dreamer!!'}
        session.post('https://github.com/login',data=data)
        r = session.get('https://github.com/search?l=Python&p=1&q=location%3A%22Hong+Kong%22+repos%3A%3E4+language%3APython&ref=advsearch&type=Users&utf8=%E2%9C%93')
        soup = BeautifulSoup(r.text, 'html5lib')
        for i in soup.findAll('div', class_='user-list-info ml-2'):
            for k in i.findAll('a'):
                print(k.get('href'))
    except:
        print('gabella')
if __name__ == '__main__':
    main()