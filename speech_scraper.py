
import os
import requests
from bs4 import BeautifulSoup

params = {

    'pages': 37,
    'root': 'https://millercenter.org',
    'speeches_page': 'https://millercenter.org/the-presidency/presidential-speeches',
    'page_url': '?field_speech_date_value%5Bmin%5D=&field_speech_date_value%5Bmax%5D=&field_full_node_value=&page='

    }

def save_speeches(speech_links):

    for link in speech_links:
        for l in link:
            
            url = params['root']+''.join(l)
            request = requests.get(url)
            request = BeautifulSoup(request.content, 'html.parser')

            text = []

            for i in request.find_all('p'):

                text.append(i.get_text())

            pres_name = '-'.join(''.join(text[1:2]).replace('.', '').split(' ')).lower()
            dos = '-'.join(''.join(text[2:3]).replace(',', '').split(' ')).lower()

            print(f'Speech on Date: {dos} given by {pres_name}')

            try:

                os.mkdir(pres_name)
                print(f'Directory Made: {pres_name}')
            except FileExistsError:

                print(f'Speech {dos} by {pres_name} saved...')
                with open(f'{pres_name}/{dos}.txt', 'w') as f:
                    for t in text[3:-2]:
                        f.write(f'{t}\n')

    return None

def fetch_speeches():

    speech_links = []

    for page in range(params['pages'] + 1):

        url = params['speeches_page']
        page_url = params['page_url']
        print(f'Page {page} Gathered...')
        speeches = f'{url}{page_url}{page}'

        request = requests.get(speeches)
        request = BeautifulSoup(request.content, 'html.parser')

        links = []

        for link in request.find_all('a', href=True):

            links.append(link['href'])
        
        speech_links.append(links[165:177])

    save_speeches(speech_links)


if __name__ == '__main__':

    fetch_speeches()



