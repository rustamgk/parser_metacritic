import typing
from bs4 import BeautifulSoup
import time
import requests
import json

__all__ = (
    'get_json_data',
)


# main parse
def get_json_data(available="available", platform='ps4', key_search=None):
    # type: (str, str, typing.Optional[str]) -> str
    start_time = time.time()
    # template request link
    link = 'https://www.metacritic.com/browse/games/release-date/%s/%s/metascore' % (available, platform)
    # link = 'http://example.com/'
    # use headers to transfer customer information to the site
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'}
    try:
        # define list of names that we will use
        json_name_date = ['title', 'score']
        # define empty list
        json_date = []
        while True:
            # print('tick')
            response = requests.get(link, headers=headers)
            # check the correctness of the response
            # print(response.status_code)
            # print(link)
            if response.status_code != 200:
                # if not correct return json with error
                return json.dumps([dict(error='Server returned status code %s' % response.status_code)], indent=1)
            else:
                # parse
                # get body html and parse with bs4(use lxml parser - very fast)
                html_soup = BeautifulSoup(response.content, 'lxml')
                # get first record game_product
                li_products = html_soup.find_all('li', class_='product game_product first_product')
                # get middle records game_product and extend to list li_products
                li_products.extend(html_soup.find_all('li', class_='product game_product'))
                # get last records game_product and extend to list li_products
                li_products.extend(html_soup.find_all('li', class_='product game_product last_product'))

                for li_product in li_products:
                    # get game_title
                    game_title = str(li_product.find('a').next).strip()
                    # get game_score
                    game_score = str(li_product.find('div', class_='metascore_w').next).strip()
                    # if key_search = None append current to json_date
                    if not key_search:
                        json_date.append([game_title, game_score])
                    # if key_search matches append current to json_date
                    elif str(key_search).lower() and game_title.lower().find(key_search.lower()) != -1:
                        json_date.append([game_title, game_score])
                # clear link
                link = None
                # find new link attrs={'class':'action','rel':'next'}
                link = html_soup.find('a', attrs={'class': 'action', 'rel': 'next'})
                # generate next page link if need
                if link:
                    link = 'https://www.metacritic.com' + str(link['href'])
                else:
                    break
        print('parse_data finish ', time.time() - start_time)
        # generate json from json_date, use json_name_date
        return json.dumps([dict(zip(json_name_date, row)) for row in json_date], indent=1)
    # exception handling and if need generate json with error
    except requests.exceptions.ConnectionError:
        return json.dumps([dict(error='failed to establish a connection')], indent=1)
    except:
        return json.dumps([dict(error='common error')], indent=1)
