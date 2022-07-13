import requests
from bs4 import BeautifulSoup


class GHScraper:
    url = 'https://github.com/users/{}/contributions'
    
    def __init__(self, username: str) -> None:
        r = requests.get(self.url.format(username))
        soup = BeautifulSoup(r.content, 'html.parser')
        self.soup = soup

    @property
    def contributions(self) -> str:
        h2 = self.soup.find('h2')
        if h2:
            return ' '.join(h2.text.split())

    def fetch_contributions(self) -> list:
        year = []
        table = self.soup.find('svg').find('g')
        for column in table.find_all('g'):
            week = []
            for cell in column.find_all('rect'):
                week.append(
                    {
                        'count': cell['data-count'],
                        'date': cell['data-date'],
                        'level': cell['data-level']
                    }
                )
            year.append(week)
        return year
